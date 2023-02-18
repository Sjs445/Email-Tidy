from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
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

    # TODO login the user after registering. Give them a session.
    # TODO send welcome email here
    return {"id": user.id}
