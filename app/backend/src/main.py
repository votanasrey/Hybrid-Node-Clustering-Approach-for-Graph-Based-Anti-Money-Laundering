from fastapi import FastAPI, Depends
from src.route import auth
from src.service.jwt_bearer import JWTBearer

app = FastAPI()

app.include_router(auth.router, prefix="/auth")


@app.get("/")
def read_root():
    return {"message": "Welcome to the hell"}


@app.get("/token", dependencies=[Depends(JWTBearer())])
def token():
    return {"message": "it is working fine guy!"}
