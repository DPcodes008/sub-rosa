import os
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

load_dotenv()

SESSION_SECRET = os.getenv("SESSION_SECRET")

serializer = URLSafeTimedSerializer(SESSION_SECRET)

# ---------- Magic Link Tokens ----------

def create_magic_token(email: str) -> str:
    return serializer.dumps({"email": email}, salt="magic-link")


def verify_magic_token(token: str, max_age=300):
    try:
        return serializer.loads(token, salt="magic-link", max_age=max_age)
    except Exception:
        return None


# ---------- Session Tokens ----------

def create_session_token(payload: dict) -> str:
    return serializer.dumps(payload, salt="session")


def verify_session_token(token: str, max_age=1800):
    try:
        return serializer.loads(token, salt="session", max_age=max_age)
    except Exception:
        return None

