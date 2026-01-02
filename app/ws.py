from fastapi import WebSocket, WebSocketDisconnect
from app.auth import verify_session_token
import json
from app.rooms import add_socket_to_room, remove_socket_from_room, get_room

async def websocket_endpoint(websocket: WebSocket):
    print("websocket hit")

    # AUTH CHECK — MUST BE BEFORE accept()
    token = websocket.query_params.get("token")
    payload = verify_session_token(token)

    if not payload:
        print("invalid or missing token")
        await websocket.close()
        return

    await websocket.accept()
    print("accepted")

    room_id = websocket.query_params.get("room_id")
    print("room_id:", room_id)

    room = get_room(room_id)
    print("room exists:", bool(room))

    success = add_socket_to_room(room_id, websocket)
    print("added to room:", success)

    if not success:
        print("closing socket")
        await websocket.close()
        return

    print("ENTER receive loop")

    try:
        while True:
            data = await websocket.receive_text()
            print("received:", data)

            event = json.loads(data)

            if event.get("type") == "MESSAGE":
                for conn in list(room.sockets):
                    if conn is not websocket:
                        await conn.send_json(event)

    except WebSocketDisconnect:
        print("client disconnected")

    finally:
        remove_socket_from_room(room_id, websocket)

