![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker Compose](https://img.shields.io/badge/docker--compose-039be5?style=for-the-badge&logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/poetry-%231227B7.svg?style=for-the-badge&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-%23DC382D.svg?style=for-the-badge&logo=Redis&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-%2300D47D.svg?style=for-the-badge&logo=FastAPI&logoColor=white)

# Real_Time_Chat

This project is an educational example of using FastAPI, a modern web framework for building web applications with
Python.

## Installation

1. Clone the repository:
   ```git clone https://github.com/ValeriyFromUA/Real_Time_Chat.git```

2. Create a virtual environment
3. Install the dependencies using `poetry install` or `pip install -r requirements.txt`
4. Create an `.env` file. and add your own data following the structure of the `.env.sample` file.
5. Run migrations with alembic in terminal:

### Hints:

- init migrations: ```alembic init migrations ```
  Now you see migrations folder and alembic.ini file 

Change file `migrations\env.py` like in example: `arch\env.py`
Change file `alembic.ini` like in example `arch\alembic.ini`

- create db: ```alembic revision --autogenerate -m "Database creation"```
- migrate: ```alembic upgrade head```

### Tutorials:

[Tutorial 1](https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396)

[Tutorial 2](https://pawamoy.github.io/posts/add-alembic-migrations-to-existing-fastapi-ormar-project/)

## Running with Docker ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

1. `sudo docker-compose build`
2. `sudo docker-compose run web alembic upgrade head`
3. `sudo docker-compose up`

Application will be available  [here](http://0.0.0.0:7000/).

## Running the Server

To run the FastAPI server, use the following command:
```uvicorn chat.main:app --reload``` or
RUN `make build_and_run`
The server will be available at [http://localhost:7000](http://localhost:7000).

## Endpoints

[Swagger UI](http://0.0.0.0:7000/docs)

```

```

## License

This project is licensed under the [MIT License](LICENSE).
