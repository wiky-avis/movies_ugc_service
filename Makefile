flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

linters: isort black flake8

docker-up-all:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml -f docker-compose/db.yml -f docker-compose/etl.yml -f docker-compose/api.yml up --build

docker-down-all: docker-down-main docker-down-events docker-down-db docker-down-etl docker-down-api

docker-down-v-main:
	docker-compose -f docker-compose/main.yml down -v

docker-up-events:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml up --build

docker-down-v-events:
	docker-compose -f docker-compose/events.yml down -v

docker-up-db:
	docker-compose -f docker-compose/main.yml -f docker-compose/db.yml up --build

docker-down-v-db:
	docker-compose -f docker-compose/db.yml down -v

docker-up-etl:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml -f docker-compose/db.yml -f docker-compose/etl.yml up --build

docker-down-v-etl:
	docker-compose -f docker-compose/etl.yml down -v

docker-up-api:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml -f docker-compose/api.yml up --build

docker-down-v-api:
	docker-compose -f docker-compose/api.yml down -v