from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_user
from app.database.database import get_db

router = APIRouter()


@router.post("/")
def scan_emails(
    *,
    scan_email: schemas.ScanEmails,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Scan emails for a linked_email address. Scans the email's inbox for possible marketing/spam to unsubscribe from.

    Args:
        scan_email (schemas.ScanEmails): The scan email info.
        db (Session): The db session.
        user (models.User): The user session.

    Returns:
        dict: The task id of the celery job
    """
    return {
        "task_id": crud.scanned_emails.scan_emails(
            db, obj_in=scan_email, user_id=user.id
        )
    }


@router.get("/{page}")
def get_scanned_emails(
    *,
    linked_email: str,
    page: int = 0,
    email_from: str = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a paginated list of scanned emails. Only includes a number count of links found for the email.

    Args:
        page (int, optional): The page to fetch. Defaults to 0.
        email_from (str, optional): Filter scanned_emails by a specific from address.
        linked_email (str): Filter scanned_emails owned by a linked_email address.
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: The scanned emails owned by the user.
    """
    return {
        "scanned_emails": crud.scanned_emails.get_scanned_emails(
            db,
            page=page,
            user_id=user.id,
            email_from=email_from,
            linked_email=linked_email,
        )
    }


@router.get("/count/{linked_email}")
def count_scanned_emails(
    *,
    linked_email: str,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a count of the number of scanned emails for this linked email. Used for pagination by the front-end.

    Args:
        count_email (schemas.CountScannedEmails): The linked email.
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: The number of scanned emails.
    """
    return {
        "count": crud.scanned_emails.count_scanned_emails(
            db, user_id=user.id, linked_email=linked_email
        )
    }

@router.get("/task_status/{task_id}")
def get_task_status(
    *,
    task_id: str,
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get the status of a task by task id

    Args:
        task_id (str): The task id to check
        user (models.User): The session user.

    Returns:
        dict: The task info
    """
    result = AsyncResult(task_id)
    return {
        "state": result.state,
        "details": result.info,
    }
