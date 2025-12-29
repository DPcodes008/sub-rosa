# app/rooms.py

from typing import Dict, Set
from fastapi import WebSocket
from app.config import redis_client
import secrets


class Room:


    def __init__(self, room_id: str, max_users: int):
        self.room_id = room_id
        self.max_users = max_users
        self.sockets: Set = set()   # WebSocket objects will be stored here

    def is_full(self) -> bool:
        return len(self.sockets) >= self.max_users

rooms: Dict[str, Room] = {}


#--------------
# Room management functions
# -----------------------------

def generate_room_id(length: int = 6) -> str:
    return secrets.token_urlsafe(length)[:length]


def create_room(max_users: int, ttl_seconds: int) -> Room:
    room_id = generate_room_id()

    # Redis = source of truth
    redis_client.set(
        name=f"room:{room_id}",
        value=str(max_users),
        ex=ttl_seconds
    )

    room = Room(room_id=room_id, max_users=max_users)
    rooms[room_id] = room

    return room



def get_room(room_id: str) -> Room | None:
    """
    Fetch a room by ID.
    """
    return rooms.get(room_id)


def delete_room(room_id: str) -> None:
    """
    Deletes a room from memory.
    """
    if room_id in rooms:
        del rooms[room_id]

def room_exists(room_id: str) -> bool:
    return redis_client.exists(f"room:{room_id}") == 1

def add_socket_to_room(room_id: str, websocket: WebSocket) -> bool:
    if not room_exists(room_id):
        print("room expired or does not exist")
        return False

    room = rooms.get(room_id)

    if not room:
        max_users = int(redis_client.get(f"room:{room_id}"))
        room = Room(room_id, max_users)
        rooms[room_id] = room

    if room.is_full():
        print("room full")
        return False

    room.sockets.add(websocket)
    return True

#adding websocket to the set sockets


def remove_socket_from_room(room_id: str, websocket) -> None:
    """
    Removes a WebSocket from a room.
    """
    room = get_room(room_id)

    if not room:
        return

    room.sockets.discard(websocket)

    if len(room.sockets) == 0:
        delete_room(room_id)

