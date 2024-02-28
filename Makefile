include .env
export $(shell sed 's/=.*//' .env)

define USAGE
Commands:
    app_run      Run application
    build_and_run		Run web application with Docker for Ubuntu with admin permissions

endef


app_run:
	uvicorn chat.main:app --host $(APP_HOST) --port $(APP_PORT) --reload

build_and_run:
	sudo docker-compose build && sudo docker-compose run web alembic revision --autogenerate -m "First migration" && sudo docker-compose run web alembic upgrade head && sudo docker-compose up
