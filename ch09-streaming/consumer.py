"""Chapter 9: running revenue per minute, with an alert on large payments."""
import json
import os
from collections import defaultdict

from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092"),
    "group.id": "payment-monitor",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["payments"])

revenue_per_minute = defaultdict(float)

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error())
            continue

        event = json.loads(msg.value())
        minute = event["occurred_at"][:16]          # e.g. 2026-03-12T14:03
        revenue_per_minute[minute] += event["amount"]

        if event["amount"] > 1800:
            print(f"ALERT large payment {event['amount']} MAD on order {event['order_id']}")
        print(minute, round(revenue_per_minute[minute], 2))
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
