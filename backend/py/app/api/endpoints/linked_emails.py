from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_user
from app.database.database import get_db

router = APIRouter()


@router.post("/link_email")
def link_email(
    *,
    email_info: schemas.LinkedEmailsCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Link an email to an account.

    Args:
        email_info (schemas.LinkedEmailsCreate): The email info to link.
        db (Session): Db session.
        user (models.LinkedEmails): The session user.

    Returns:
        dict: The success status of the email link.
    """
    email = crud.linked_email.get_by_email(db, email=email_info.email)

    if email is not None:
        raise HTTPException(status_code=400, detail="Email already exists!")

    email = crud.linked_email.create_with_user(db, obj_in=email_info, user_id=user.id)

    return {"success": bool(email)}


@router.get("/linked_emails")
def get_linked_emails(
    *,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a list of linked_emails owned by the session user.

    Args:
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: the linked email info owned by the user
    """
    return {"linked_emails": crud.linked_email.get_by_user_id(db=db, user_id=user.id)}
