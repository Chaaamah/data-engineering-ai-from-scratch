"""Exercise 9.2: an idempotent consumer that ignores events it has already processed.

Kafka delivers at least once, so after a crash or a rebalance some events arrive twice.
Remembering processed event IDs makes the totals correct anyway.
"""
import json
import os
from collections import defaultdict

from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092"),
    "group.id": "payment-monitor-idempotent",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["payments"])

seen_event_ids: set[str] = set()
revenue_per_minute = defaultdict(float)
duplicates = 0

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        event = json.loads(msg.value())

        if event["event_id"] in seen_event_ids:
            duplicates += 1
            print(f"skipped duplicate {event['event_id']} (total skipped: {duplicates})")
            continue
        seen_event_ids.add(event["event_id"])

        minute = event["occurred_at"][:16]
        revenue_per_minute[minute] += event["amount"]
        print(minute, round(revenue_per_minute[minute], 2))
except KeyboardInterrupt:
    pass
finally:
    consumer.close()

# In production the set lives in a database, not in memory, so it survives restarts:
#   CREATE TABLE processed_events (event_id UUID PRIMARY KEY, processed_at TIMESTAMPTZ DEFAULT now());
#   INSERT INTO processed_events (event_id) VALUES (%s) ON CONFLICT DO NOTHING;
# If the insert affected 0 rows, the event was a duplicate. Do the insert and the
# business update in the same transaction, so both happen or neither does.
