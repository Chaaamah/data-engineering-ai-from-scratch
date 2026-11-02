"""Chapter 9: send fake payment events to Kafka, two per second."""
import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")})

try:
    while True:
        order_id = random.randint(1000, 1100)
        event = {
            "event_id": str(uuid.uuid4()),
            "type": "payment_succeeded",
            "order_id": order_id,
            "amount": round(random.uniform(20, 2000), 2),
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        }
        producer.produce("payments", key=str(order_id), value=json.dumps(event))
        producer.poll(0)        # serve delivery callbacks
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    producer.flush()            # deliver anything still buffered
