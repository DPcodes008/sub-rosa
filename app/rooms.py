# app/rooms.py

import time
import secrets
from typing import Dict, Set


class Room:
    """
    Represents a single ephemeral chat room.
    """

    def __init__(self, room_id: str, max_users: int, ttl_seconds: int):
        self.room_id = room_id
        self.max_users = max_users
        self.expires_at = time.time() + ttl_seconds
        self.sockets: Set = set()   # WebSocket objects will be stored here

    def is_expired(self) -> bool:
        return time.time() >= self.expires_at

    def is_full(self) -> bool:
        return len(self.sockets) >= self.max_users


# -----------------------------
# In-memory room registry
# -----------------------------

rooms: Dict[str, Room] = {}


# -----------------------------
# Room management functions
# -----------------------------

def generate_room_id(length: int = 6) -> str:
    """
    Generates a secure, URL-safe room ID.
    """
    return secrets.token_urlsafe(length)[:length]


def create_room(max_users: int, ttl_seconds: int) -> Room:
    """
    Creates a new room and stores it in memory.
    """
    room_id = generate_room_id()

    room = Room(
        room_id=room_id,
        max_users=max_users,
        ttl_seconds=ttl_seconds
    )

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


async def cleanup_expired_rooms():
    """
    Close sockets and delete expired rooms.
    """
    expired_room_ids = [
        rid for rid, room in rooms.items() if room.is_expired()
    ]

    for rid in expired_room_ids:
        room = rooms.get(rid)
        if not room:
            continue

        # Kick all sockets
        for websocket in list(room.sockets):
            try:
                await websocket.close(code=1000)
            except Exception:
                pass

        # Delete room
        delete_room(rid)
        print(f"Room {rid} expired and destroyed")


def add_socket_to_room(room_id: str, websocket) -> bool:
    room = get_room(room_id)

    if not room:
        print("room not found")
        return False

    print("TTL remaining:", room.expires_at - time.time())

    if room.is_expired():
        print("room already expired")
        return False

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

