from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect
from fastapi import WebSocket

from manager import manager

templates = Jinja2Templates(directory="templates")
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/{username}/{to_user}", response_class=HTMLResponse)
async def index(request: Request, username: str, to_user: str):
    return templates.TemplateResponse("socket.html", {"request": request, "username": username, "to_user": to_user})


banned = []


@app.websocket("/ws/{username}/{to_user}")
async def websocket_endpoint(websocket: WebSocket, username: str, to_user: str):
    print(manager.active_connections)
    await manager.connect(username, websocket)
    client_host = websocket.client.host
    if client_host in banned:
        manager.disconnect(username)
        await manager.send_personal_message('siz ban olgansiz {client_host}', websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if 'fuck' in data.lower():
                await manager.send_personal_message(f'{username} siz ban oldingiz {client_host}', websocket)
                manager.disconnect(websocket)
                await manager.broadcast(f'{username} ban oldi')
                banned.append(client_host)
            await manager.send_personal_message(data, websocket)
            await manager.send_message(data, username, to_user)
    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.send_message(f"Client #{username} left the chat", username, to_user)
