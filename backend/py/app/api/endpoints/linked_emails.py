from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_user
from app.database.database import get_db

router = APIRouter()


@router.post("/")
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
        dict: The email obj
    """
    email = crud.linked_email.get_by_email(db, email=email_info.email)

    if email is not None:
        raise HTTPException(status_code=400, detail="Email already exists!")

    email = crud.linked_email.create_with_user(db, obj_in=email_info, user_id=user.id)

    return {
        "id": email.id,
        "email": email.email,
        "insert_ts": str(email.insert_ts),
        "is_active": email.is_active,
    }


@router.get("/")
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


@router.delete("/{id}")
def delete_linked_email(
    *,
    id: int = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Delete a linked email by id.

    Args:
        id (int): the id of the linked email to delete
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: the linked email id that was deleted
    """
    email = crud.linked_email.remove(db=db, id=id)
    return {"id": email.id}

@router.get("/tasks/{linked_email_address}")
def get_current_running_task(
    *,
    linked_email_address: str,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get the current running task id for this linked email.
    This tells us whether a scan is still happening for a linked_email_address.

    Args:
        linked_email_address (id): The linked_email_address

    Returns:
        dict: Information regarding the status of the task
    """
    return {
        "task": crud.linked_email.get_task_id(
            db, linked_email_address=linked_email_address, user_id=user.id,
        )
    }
