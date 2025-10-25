from http import HTTPStatus
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from maddr_api.models.account import Account
from maddr_api.schemas.token import Token
from maddr_api.security.access_token import create_access_token
from maddr_api.security.hash_password import verify_password
from maddr_api.services.main import BaseCRUD

from sqlalchemy.ext.asyncio import AsyncSession as Session


class TokenService(BaseCRUD[Account, Token]):
    """
    Service layer for token operations.
    """

    def __init__(self, session: Session):
        super().__init__(model=Account, session=session)

    async def create_access_token(
        self, form_data: OAuth2PasswordRequestForm
    ) -> Token:
        """
        Create an access token for the given account.
        """

        account_data = await self.read("username", form_data.username)

        if not account_data:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect username or password.",
            )

        if not verify_password(form_data.password, account_data.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect username or password.",
            )

        access_token = create_access_token(data={"sub": account_data.username})

        return Token(access_token=access_token, token_type="bearer")
