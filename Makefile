flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

linters: isort black flake8

up-prod:
	docker-compose -f docker-compose-prod.yml up --build

down-prod: 
	docker-compose -f docker-compose-prod.yml down

up-local:
	docker-compose -f docker-compose-local.yml up --build

down-local:
	docker-compose -f docker-compose-local.yml down -v