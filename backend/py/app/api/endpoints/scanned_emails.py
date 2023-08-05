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
    """Scan emails for a linked_email address. Scans the email's inbox for possible marketing/spam
    to unsubscribe from.

    Args:
        scan_email (schemas.ScanEmails): The scan email info.
        db (Session): The db session.
        user (models.User): The user session.

    Returns:
        dict: Number of emails scanned.
    """
    return {
        "scanned": crud.scanned_emails.scan_emails(
            db, obj_in=scan_email, user_id=user.id
        )
    }


@router.get("/{page}")
def get_scanned_emails(
    *,
    page: int = 0,
    email_from: str = None,
    linked_email: str = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a paginated list of scanned emails. Only includes a number count of links found for the email.

    Args:
        page (int, optional): The page to fetch. Defaults to 0.
        email_from (str, optional): Filter scanned_emails by a specific from address.
        linked_email (str, optional): Filter scanned_emails owned by a linked_email address.
        db (Session): The db session.
        user (models.User): The session user.

    Returns:
        dict: The scanned emails owned by the user.
    """
    return {
        "scanned_emails": crud.scanned_emails.get_scanned_emails(
            db,
            page=page,
            email_from=email_from,
            linked_email=linked_email,
        )
    }
