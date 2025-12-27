from fastapi import FastAPI, WebSocket
import asyncio
from app.ws import websocket_endpoint
from app.rooms import cleanup_expired_rooms
from app.rooms import create_room

app = FastAPI()

@app.on_event("startup")
async def start_room_reaper():
    async def room_reaper():
        while True:
            await cleanup_expired_rooms()
            await asyncio.sleep(5)  # check every 5 seconds
    asyncio.create_task(room_reaper())
#Starts when server starts .Every 5 seconds,Checks for expired rooms.Kills them if needed


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
