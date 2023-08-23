from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_user
from app.database.database import get_db
from app.schemas.unsubscribe_links import UnsubscribeEmail

router = APIRouter()


@router.get("/unsubscribe_links_by_email/{scanned_email_id}")
def get_unsubscribe_links_by_email(
    *,
    scanned_email_id: int = None,
    linked_email: str = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Get a list of unsubscribe links by an scanned_email and linked_email address.

    Args:
        scanned_email_id (int): the scanned email to fetch
        linked_email (str): the linked email
        db (Session): The db session.
        user (models.User): The session user

    Returns:
        dict: The unsubscribe links
    """
    return {
        "links": crud.unsubscribe_links.get_unsubscribe_links_by_email(
            db,
            linked_email_address=linked_email,
            scanned_email_id=scanned_email_id,
            user_id=user.id,
        )
    }


@router.post("/")
def unsubscribe(
    *,
    unsub_info: UnsubscribeEmail,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> dict:
    """Unsubscribe from an email.

    Args:
        unsub_info (UnsubscribeEmail): The scanned email id and linked_email
        db (Session): The db session.
        user (models.User): The session user

    Returns:
        dict: The modified unsubscribe links
    """
    return {
        "scanned_emails": crud.unsubscribe_links.unsubscribe(
            db,
            scanned_email_ids=unsub_info.scanned_email_ids,
            linked_email_address=unsub_info.linked_email_address,
            user_id=user.id,
            page=unsub_info.page,
        )
    }
