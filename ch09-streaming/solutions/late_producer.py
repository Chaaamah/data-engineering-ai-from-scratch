"""Exercise 9.3: a producer where 20% of events arrive five minutes late."""
import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")})

try:
    while True:
        occurred = datetime.now(timezone.utc)
        late = random.random() < 0.2
        if late:
            occurred -= timedelta(minutes=5)    # e.g. a phone that lost signal
        event = {
            "event_id": str(uuid.uuid4()),
            "type": "payment_succeeded",
            "order_id": random.randint(1000, 1100),
            "amount": round(random.uniform(20, 2000), 2),
            "occurred_at": occurred.isoformat(),
        }
        producer.produce("payments", key=str(event["order_id"]), value=json.dumps(event))
        producer.poll(0)
        print("LATE " if late else "     ", event["occurred_at"][:19])
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    producer.flush()
