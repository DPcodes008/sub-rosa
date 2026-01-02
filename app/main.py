from fastapi import FastAPI, WebSocket,Request, HTTPException
from fastapi.responses import RedirectResponse
from app.auth import verify_magic_token, create_session_token
from app.auth import create_magic_token
from app.emailer import send_magic_link
from app.ws import websocket_endpoint
from app.rooms import create_room
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.post("/auth/request-link")
async def request_link(data: dict):
    email = data.get("email")

    if not email or not email.endswith("@nitc.ac.in"):
        raise HTTPException(status_code=403, detail="NITC email required")

    token = create_magic_token(email)
    link = f"http://localhost:8000/auth/verify?token={token}"

    send_magic_link(email, link)
    return {"status": "link_sent"}
@app.get("/auth/verify")
async def verify_link(token: str):
    data = verify_magic_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired link")

    session_token = create_session_token({"email": data["email"]})

    return RedirectResponse(
        url=f"/rooms.html?token={session_token}"
    )
  
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

app.mount("/", StaticFiles(directory="static", html=True), name="static")
