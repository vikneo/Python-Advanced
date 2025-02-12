setup poetry:
	pip install poetry

set_poetry:
	poetry install

run_test:
	python -m unittest descover tests -v

flask_run:
	flask --app app run

docker_build:
	docker compose build app

docker_run:
	docker compose up app
