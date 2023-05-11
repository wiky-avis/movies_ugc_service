clickhouse-client --host broker --port 9092 < src/db/setup_clickhouse.sql

docker-compose -f docker-compose-local.yml exec clickhouse-node1 sh <

command1 && command2