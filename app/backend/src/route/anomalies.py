from fastapi import APIRouter, Depends
from src.service.jwt_bearer import JWTBearer
from datetime import datetime, timedelta

from src.util.response import success_response

router = APIRouter()


@router.get('/daily', dependencies=[Depends(JWTBearer())])
def get_dashboard_overview():
    start_date = datetime(2024, 1, 1)
    data = []

    for i in range(12):
        date = start_date + timedelta(days=i * 30)
        transaction_count = 50 + i * 5
        amount = 1000 + i * 100
        data.appddend({
            "date": date.strftime('%Y-%m-%d'),
            "count": transaction_count,
            "amount": amount
        })

    return success_response("Have been retrieved", data)


@router.get('/top-users', dependencies=[Depends(JWTBearer())])
def get_top_users():
    base_datetime = datetime(2024, 1, 1, 23, 59, 59)
    users = []

    for i in range(5):
        sender_account = f"00012332{i + 1}"
        sender_bank = f"Bank {chr(65 + i)}"
        amount = 1000 + i * 500
        transaction_datetime = base_datetime + timedelta(days=i * 15)
        users.append({
            "sender_account": sender_account,
            "sender_bank": sender_bank,
            "amount": amount,
            "transaction_datetime": transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')
        })

    return success_response("Have been retrieved", users)
