flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

linters: isort black flake8

docker-up-all:
	docker-compose up --build

docker-down-all: docker-compose down -v

docker-compose down -v zookeeper:
	docker-compose down -v zookeeper

docker-up-events:
	docker-compose up --build zookeeper broker

docker-down-v-events:
	docker-compose down -v zookeeper broker

docker-up-db:
	docker-compose up --build zookeeper clickhouse-node1 clickhouse-node2

docker-down-v-db:
	docker-compose down -v zookeeper clickhouse-node1 clickhouse-node2

docker-up-etl:
	docker-compose up --build zookeeper broker clickhouse-node1 clickhouse-node2 etl

docker-down-v-etl:
	docker-compose down -v zookeeper broker clickhouse-node1 clickhouse-node2 etl

docker-up-api:
	docker-compose up --build zookeeper broker fastapi nginx

docker-down-v-api:
	docker-compose down -v zookeeper broker fastapi nginx