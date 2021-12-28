from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import base64
import time
from Components.ConnectionManager import ConnectionManager
from Components.DataBaseManager import DataBaseManager

app = FastAPI()
manager = ConnectionManager()
db = DataBaseManager()

@app.get('/')
async def welcome():
    return {'message': "Hello World!"}

@app.websocket("/ws/{client_token}")
async def chatroom_endpoint(websocket: WebSocket, client_token:str):
    await manager.connect(websocket)
    datas = db.read_all()
    all_data = []
    for data in datas:
        all_data.append({"message": data["message"], "client_token": data["client_token"]})
    # print(all_data)
    if (list(all_data)):
        # print(all_data)
        await manager.send(websocket, all_data)
    try:
        while True:
            messageData = await websocket.receive_json()
            print(messageData)
            messageData['client_token'] = client_token
            db.write_in(messageData["message"], client_token, time.time())
            await manager.broadcast([messageData])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast([{"status": "SIGNOUT", "client_token": client_token}])