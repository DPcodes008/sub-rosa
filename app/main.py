from fastapi import FastAPI, WebSocket
from app.ws import websocket_endpoint

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Sub Rosa backend alive"}

@app.websocket("/ws")
async def ws_route(websocket: WebSocket): 
    await websocket_endpoint(websocket)
    
#awaits are only allowed inside asyncs
#async fucntions means, they is allowed to be paused and be resumed later
#await inside means pause this fn until something happens
