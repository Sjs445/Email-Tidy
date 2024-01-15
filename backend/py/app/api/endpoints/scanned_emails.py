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

@router.get("/senders/{page}")
def get_senders(
    *,
    linked_email: str,
    page: int = 0,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a list of senders for this linked email.

    Args:
        linked_email (str): The linked email to filter by
        page (int, optional): The page to fetch. Defaults to 0.
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: A list of email senders that were scanned
    """
    return {
        "senders": crud.scanned_emails.get_senders_by_linked_email(db, user_id=user.id, linked_email=linked_email, page=page)
    }

@router.post("/get_scanned_emails")
def get_scanned_emails(
    *,
    get_scanned_email: schemas.GetScannedEmails,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a paginated list of scanned emails. Only includes a number count of links found for the email.

    Args:
        get_scanned_email (schemas.GetScannedEmails): request params including linked_email, email_from, and page
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: The scanned emails owned by the user.
    """
    return {
        "scanned_emails": crud.scanned_emails.get_scanned_emails(
            db,
            page=get_scanned_email.page,
            user_id=user.id,
            email_from=get_scanned_email.email_from,
            linked_email=get_scanned_email.linked_email,
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
