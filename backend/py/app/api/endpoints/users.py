from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.config import security
from app.config.config import settings
from app.database.database import get_db

router = APIRouter()


@router.post("/register")
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> dict:
    """Register a new user.

    Args:
        user_in (schemas.UserCreate): The new user to create.
        db (Session, optional): The db session. Defaults to Depends(get_db).

    Returns:
        dict: The response
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="The user with this email already exists"
        )
    user = crud.user.create(db, obj_in=user_in)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # TODO send welcome email here
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
