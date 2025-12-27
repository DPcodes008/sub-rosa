
from fastapi import WebSocket, WebSocketDisconnect
from app.rooms import add_socket_to_room, remove_socket_from_room, get_room
#printing was done at each step to make debugging easier
async def websocket_endpoint(websocket: WebSocket):
    print("websocket hit")

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

    except WebSocketDisconnect:
        print("client disconnected")
        remove_socket_from_room(room_id, websocket)

