#!/usr/bin/env bash
# Create the payments topic with 3 partitions (exercise 9.1 needs more than one).
set -euo pipefail

docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic payments \
  --partitions 3 \
  --replication-factor 1

docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --describe --topic payments
