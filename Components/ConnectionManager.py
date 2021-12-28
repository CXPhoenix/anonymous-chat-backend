from fastapi import WebSocket
class ConnectionManager:
    def __init__(self):
        self.__activeConnections: List[WebSocket] = []
    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        self.__activeConnections.append(websocket)
    
    def disconnect(self, websocket:WebSocket):
        self.__activeConnections.remove(websocket)
    
    async def broadcast(self, messageData:dict):
        for connection in self.__activeConnections:
            await connection.send_json(messageData)
    
    async def send(self, websocket: WebSocket, messageDatas: list):
        await websocket.send_json(messageDatas)