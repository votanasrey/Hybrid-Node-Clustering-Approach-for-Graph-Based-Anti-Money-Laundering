from fastapi import APIRouter, Depends

from src.service.jwt_bearer import JWTBearer
from src.util.response import success_response

router = APIRouter()


@router.get('/overview', dependencies=[Depends(JWTBearer())])
def get_dashboard_overview():
    data = {
        "accounts": 932,
        "transactions": 1000,
        "amount": 4000,
        "banks": 10
    }
    return success_response("Have been retrieved", data)
