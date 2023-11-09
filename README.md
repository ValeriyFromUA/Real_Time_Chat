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

## Running the Server

To run the FastAPI server, use the following command:
```uvicorn chat.main:app --reload```
The server will be available at [http://localhost:8000](http://localhost:8000).

## Endpoints

[Swagger UI](http://127.0.0.1:8000/docs)

```
http://127.0.0.1:8000/docs - Documentation, endpoints, data formats, IMPORTANTLY.

http://127.0.0.1:8000/guests/get_user - return user from DB or unknown User (need some fix)
http://127.0.0.1:8000/guests/set_name - create new user with name
http://127.0.0.1:8000/guests/get_name - return username from Cookies

http://127.0.0.1:8000/messages/get_room_messages/{room_id} - return messages for room #{room_id} (need some fix)

http://127.0.0.1:8000/rooms/create_room - create room with name and description
http://127.0.0.1:8000/rooms/join_room - allows you to pin the user to the room, probably a rudiment, needs revision
http://127.0.0.1:8000/rooms/get_rooms - allows you to view the keys to which the user is attached, probably a rudiment, needs revision

http://127.0.0.1:8000/pages/room/{room_id} - allows you to test the chat with a primitive interface (rudiment)




```

## License

This project is licensed under the [MIT License](LICENSE).
