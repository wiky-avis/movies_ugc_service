flake8:
	flake8 --config=.flake8

black:
	black . --config pyproject.toml

isort:
	isort .

mypy:
	mypy src --explicit-package-bases


linters: isort black flake8 mypy

up-prod:
	docker-compose -f docker-compose-prod.yml up --build

up-prod-d:
	docker-compose -f docker-compose-prod.yml up -d --build	

down-prod: 
	docker-compose -f docker-compose-prod.yml down

up-local:
	docker-compose -f docker-compose-local.yml up --build

up-local-d:
	docker-compose -f docker-compose-local.yml up -d --build

down-local:
	docker-compose -f docker-compose-local.yml down -v