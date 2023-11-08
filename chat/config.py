import os

from dotenv import load_dotenv

load_dotenv()

APP_HOST = os.environ.get('APP_HOST')
APP_PORT = os.environ.get('APP_PORT')

DB_USER = os.environ.get('PGUSER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
SECRET = os.environ.get('SECRET') or 'ofjsdiofjio3jio43orfweogoi3hth34t'

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
          crossorigin="anonymous">
</head>
<body>
<div class="container mt-3">
    <h1>FastAPI WebSocket Chat</h1>
    <h2>Your ID: <span id="ws-id"></span></h2>
    <h2>Your Name: <span id="ws-name"></span></h2>
    <form action="" onsubmit="sendMessage(event)">
        <input type="text" class="form-control" id="messageText" autocomplete="off"/>
        <button class="btn btn-outline-primary mt-2">Send</button>
    </form>
    <ul id='messages' class="mt-5">
    </ul>
</div>

<script>
    var client_id = Date.now();
    var client_name = prompt("Введіть ваше ім'я:");
    document.querySelector("#ws-id").textContent = client_id;
    document.querySelector("#ws-name").textContent = client_name;
    var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}?client_name=${client_name}`);
    ws.onmessage = function(event) {
        var messages = document.getElementById('messages');
        var message = document.createElement('li');
        var content = document.createTextNode(event.data);
        message.appendChild(content);
        messages.appendChild(message);
    };
    function sendMessage(event) {
        var input = document.getElementById("messageText");
        ws.send(input.value);
        input.value = '';
        event.preventDefault();
    }
</script>
</body>
</html>

"""
