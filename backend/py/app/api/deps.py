from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import RedirectResponse
from starlette.requests import Request
from jose import jwt
from pydantic import ValidationError

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.config.config import settings
from app.config.security import ALGORITHM
from app import crud, models, schemas
from apis.utils import OAuth2PasswordBearerWithCookie

reusable_oauth2 = OAuth2PasswordBearerWithCookie(
    tokenUrl="/login/access-token", auto_error=False
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/login/"},
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/login/"},
        )
    return user
