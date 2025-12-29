from fastapi import FastAPI, WebSocket
import asyncio
from app.ws import websocket_endpoint
from app.rooms import create_room

app = FastAPI()


@app.post("/create-room")
def create_room_api():
    room = create_room(max_users=2, ttl_seconds=90)
    return {"room_id": room.room_id}
#ROom creation is an HTTP POST method.It is used only once.

@app.get("/")
def root():
    return {"status": "Sub Rosa backend alive"}

@app.websocket("/ws")
async def ws_route(websocket: WebSocket): 
    await websocket_endpoint(websocket)
    
#awaits are only allowed inside asyncs
#async fucntions means, they is allowed to be paused and be resumed later
#await inside means pause this fn until something happens
