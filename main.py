from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from json import JSONDecodeError

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Task</title>
    </head>
    <body>
        <h1>Тестовое</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Отправить сообщение</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    counter = 0
    while True:
        try:
            counter += 1
            data = await websocket.receive_json()
            out_data = {"message_id": counter, "message_text": data}
            await websocket.send_json(out_data)
        except JSONDecodeError:
            await websocket.send_text("Invalid input format. Websocket will be closed. Please reload the page.")
            await websocket.close(code=1000, reason=None)

