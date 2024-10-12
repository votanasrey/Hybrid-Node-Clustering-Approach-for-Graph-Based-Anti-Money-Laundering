from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.service.token_service import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme or missing credentials.")

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:
        """Verify the validity of the JWT token."""
        try:
            payload = decode_jwt(token)
            return payload is not None
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return False
