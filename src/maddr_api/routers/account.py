from fastapi import APIRouter
from http import HTTPStatus

router = APIRouter(prefix="/account", tags=["account"])


@router.post(
    "/",
    summary="Create a new account",
    description="Create a new account with the provided data.",
    status_code=HTTPStatus.CREATED,
)
def create_account():
    return {"message": "Account created successfully."}
