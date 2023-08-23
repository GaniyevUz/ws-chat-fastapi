from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str:WebSocket] = {}

    async def connect(self, username, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username):
        try:
            del self.active_connections[username]
        except KeyError:
            pass

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_message(self, message: str, from_user, to_user):
        try:
            await self.active_connections[to_user].send_text(f'{message} <- {to_user}')
        except KeyError:
            await self.active_connections[from_user].send_text('bunday user yoq')

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
