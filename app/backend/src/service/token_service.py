import os
import time
from typing import Dict, Optional
import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def token_response(token: str) -> Dict[str, str]:
    """Generate a token response dictionary."""
    return {"access_token": token}


def sign_jwt(user_id: str, expires_in: int = 600) -> Dict[str, str]:
    """Sign a JWT token with user_id and expiration time."""
    payload = {
        "user_id": user_id,
        "exp": time.time() + expires_in  # Use 'exp' for expiration
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str) -> Optional[Dict[str, str]]:
    """Decode a JWT token and return its payload or None if invalid."""
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        return None
