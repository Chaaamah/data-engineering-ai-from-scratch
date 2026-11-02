# Chapter 9 — Streaming data

```bash
docker compose --profile streaming up -d
bash ch09-streaming/create_topic.sh     # payments topic with 3 partitions

python ch09-streaming/producer.py       # terminal 1
python ch09-streaming/consumer.py       # terminal 2
```

Stop the consumer with Ctrl+C, wait a minute, start it again: it resumes from its last committed offset.

## Solutions

### Exercise 1 — Two consumers in the same group

Start a second `consumer.py` in a third terminal. Kafka **rebalances**: the 3 partitions are split between the two consumers, for example 2 and 1. Each event is now processed by exactly one of them. Stop one consumer and its partitions move back to the other within seconds.

A consequence: each consumer only sees part of the traffic, so its per-minute totals are partial. To get global totals, either use one consumer, or write partial results to a shared store and add them up there.

### Exercise 2 — Idempotent consumer

See `solutions/consumer_idempotent.py`, including the database version for production.

### Exercise 3 — Late events

Run `solutions/late_producer.py` with the normal consumer. Late events add revenue to a minute that was printed five minutes earlier, so **totals already shown change after the fact**. A dashboard built on those numbers would quietly be wrong.

Grouping by processing time would hide the problem by putting late money in the wrong minute. The real fix is event-time windows with a **watermark**: keep each window open for an allowed lateness, say 10 minutes, emit the result when the watermark passes, and send events that are even later to a separate correction path. Stream processors such as Flink and Spark Structured Streaming do this for you.
