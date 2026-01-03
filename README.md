---

# Sub Rosa

**Ephemeral, room-based chat with strong privacy guarantees**

Sub Rosa is a real-time chat system designed around one core principle:

> **The server should not own user messages.**

Messages are ephemeral, rooms auto-expire, and authentication controls access without compromising anonymity. Sub Rosa is built incrementally with clear architectural phases, prioritizing correctness, security boundaries, and explainability.

---

## Features (up to Phase 6)

### Ephemeral Rooms

* Rooms are created with a fixed TTL
* Rooms automatically self-destruct after expiry
* No manual cleanup required
* TTL enforced server-side

### Real-time Messaging (WebSockets)

* Low-latency, bidirectional communication
* Messages are scoped strictly to rooms
* Server acts as a **dumb relay**
* Messages are **never persisted**

### Ephemeral Messages

* Messages include a TTL
* Clients enforce message expiry and removal
* No message history retrieval by design

### Redis-backed State (Phase 5)

* Room state stored in Redis instead of in-memory dicts
* TTL handled at datastore level
* Crash-resilient room expiry
* Scales beyond a single process

### Authentication (Phase 6)

* Passwordless **Magic Link Email Authentication**
* Only `@nitc.ac.in` email addresses allowed
* No passwords stored
* Short-lived, signed session tokens
* Authentication happens **before WebSocket upgrade**

### WebSocket Access Control

* WebSocket connections require a valid session token
* Unauthorized users never get persistent connections
* Session tokens are short-lived and stateless

---

## Design Philosophy

Sub Rosa is built around a few strict ideas:

* **No message persistence**
  Messages are transient WebSocket events, not database records.

* **Separation of concerns**
  Rooms, messaging, auth, and crypto are isolated modules.

* **Server is untrusted by design**
  The server relays messages but does not interpret or store them.

* **Progressive complexity**
  Each phase is completed and stabilized before adding the next.

---

## Architecture Overview

```
Client (Browser)
  ├── login.html        (Magic link auth)
  ├── rooms.html        (Chat UI + WS client)
  │
  ├── ws_test.html
  │
FastAPI Backend
  ├── main.py           (Routes + static serving)
  ├── ws.py             (WebSocket lifecycle & messaging)
  ├── rooms.py          (Room management & TTL)
  ├── auth.py           (Token creation & verification)
  ├── emailer.py        (SMTP magic link delivery)
  ├── crypto.py         (Reserved for Phase 7)
  │
Redis
  ├── Room state
  └── TTL enforcement
```

---

## Authentication Model (Phase 6)

### Magic Link Flow

1. User enters their `@nitc.ac.in` email
2. Backend generates a **time-limited magic link token**
3. Login link is sent via email
4. User clicks the link
5. Backend verifies the token
6. Backend issues a **short-lived session token**
7. Session token is used for HTTP and WebSocket access

### Token Separation

* **Magic link token**

  * One-time use
  * Short TTL (e.g., 5 minutes)
  * Proves email ownership

* **Session token**

  * Longer TTL (e.g., 30 minutes)
  * Used repeatedly
  * Required for WebSocket connections

This separation prevents replay attacks and limits damage if a token leaks.

---

## WebSocket Design

* Messaging happens **only** over WebSockets
* HTTP is used only for:

  * Room creation
  * Authentication
* WebSocket authentication is validated **before** `accept()`
* Rooms act as isolated broadcast domains

---

## Current Limitations (Intentional)

* No message persistence
* No message history
* No end-to-end encryption (yet)
* No user presence tracking
* No multi-device sessions

These are **deliberate design choices**, not missing features.

---

## Roadmap

### Phase 7 — End-to-End Encryption (E2EE)

* Client-side encryption using libsodium
* Server remains completely blind to message contents
* Key exchange and protocol validation
* `crypto.py` will be implemented in this phase

---

## Running Locally

### Requirements

* Python 3.10+
* Redis
* Gmail account with App Password (for SMTP)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start Redis
```
redis-server
```

### Run the server

```
uvicorn app.main:app --reload
```

### Open in browser
```
http://localhost:8000/login.html
```

---

## Project Status

* Phase 1 → Phase 6: Complete
* Phase 7 (E2EE): Planned

---

## Author

Built as a learning-focused, privacy-first system to explore:

* WebSockets
* Ephemeral systems
* Authentication boundaries
* Secure architecture design

---
