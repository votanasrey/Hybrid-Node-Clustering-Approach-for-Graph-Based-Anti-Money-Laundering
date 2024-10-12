from http import HTTPStatus

from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.service.token_service import decode_jwt
from src.util.response import error_response


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise error_response(status_code=HTTPStatus.FORBIDDEN, message="Invalid authentication scheme or missing credentials.")

        if not self.verify_jwt(credentials.credentials):
            return error_response(message="Invalid or expired token.", status_code=HTTPStatus.FORBIDDEN)

        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:
        """Verify the validity of the JWT token."""
        try:
            payload = decode_jwt(token)
            return payload is not None
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return False
