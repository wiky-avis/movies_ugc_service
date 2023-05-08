flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

linters: isort black flake8

docker-up-all:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml -f docker-compose/db.yml -f docker-compose/etl.yml -f docker-compose/api.yml up --build

docker-up-events:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml up --build

docker-up-db:
	docker-compose -f docker-compose/main.yml -f docker-compose/db.yml up --build

docker-up-etl:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml -f docker-compose/db.yml -f docker-compose/etl.yml up --build

docker-up-api:
	docker-compose -f docker-compose/main.yml -f docker-compose/events.yml -f docker-compose/api.yml up --build