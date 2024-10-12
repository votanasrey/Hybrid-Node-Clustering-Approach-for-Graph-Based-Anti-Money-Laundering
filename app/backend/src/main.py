from http import HTTPStatus

from fastapi import FastAPI, Depends, Request, HTTPException
from src.route import auth, dashboard, anomalies
from src.service.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder

from src.util.response import error_response

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(anomalies.router, prefix="/anomalies")

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return error_response(
        status_code=exec.status_code if isinstance(exc, HTTPException) else HTTPStatus.INTERNAL_SERVER_ERROR,
        message=jsonable_encoder(str(exc.args))
    )


@app.get("/")
def read_root():
    return {"message": "Welcome to the hell"}


@app.get("/token", dependencies=[Depends(JWTBearer())])
def token():
    return {"message": "it is working fine guy!"}


@app.get("/error")
def trigger_error():
    raise ValueError("This is a test error")
