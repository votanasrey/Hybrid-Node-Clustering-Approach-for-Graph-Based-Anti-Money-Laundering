from fastapi import HTTPException
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pydantic import BaseModel
from typing import Optional, Any


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[Any] = None


def success_response(message: str, data: Optional[Any] = None, status_code: Optional[int] = HTTPStatus.OK):
    success = SuccessResponse(message=message, data=data)
    return JSONResponse(status_code=status_code, content=success.dict())


def error_response(message: str, detail: Optional[Any] = None, status_code: int = HTTPStatus.BAD_REQUEST):
    error = ErrorResponse(message=message, detail=detail)
    return JSONResponse(status_code=status_code, content=error.dict())
