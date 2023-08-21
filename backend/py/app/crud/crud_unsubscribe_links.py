import requests

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.linked_emails import LinkedEmails
from app.models.unsubscribe_links import UnsubscribeLinks, UnsubscribeStatus
from app.schemas.unsubscribe_links import (
    FetchUnsubscribeLinks,
    UnsubscribeEmailsCreate,
    UnsubscribeEmailUpdate,
)


class CRUDUnsubscribeLinks(
    CRUDBase[UnsubscribeLinks, UnsubscribeEmailsCreate, UnsubscribeEmailUpdate]
):
    def get_unsubscribe_links_by_email(
        self,
        db: Session,
        *,
        linked_email_address: str,
        scanned_email_id: int,
        user_id: int,
    ) -> list:
        """Get unsubscribe links by a scanned email and linked email address.

        Args:
            db (Session): The db session
            linked_email_address (str): the linked email
            scanned_email_id (int): the scanned email id
            user_id (int): the session user_id

        Returns:
            list: The list of unsubscribe links objects.
        """

        # Check first that this user owns the scanned_email
        linked_email = (
            db.query(LinkedEmails)
            .filter(
                LinkedEmails.email == linked_email_address,
                LinkedEmails.user_id == user_id,
            )
            .first()
        )

        if not linked_email:
            raise HTTPException(
                status_code=400, detail=f"Could not find linked email"
            )

        # Fetch the unsubscribe links for this user
        links = (
            db.query(UnsubscribeLinks)
            .filter(
                UnsubscribeLinks.linked_email_address == linked_email_address,
                UnsubscribeLinks.scanned_email_id == scanned_email_id,
            )
            .all()
        )

        return links
    
    def unsubscribe(
            self,
            db: Session,
            *,
            scanned_email_ids: List[int],
            linked_email: str,
            user_id: int,
    ) -> list:
        """Unsubscribe from a scanned email

        Args:
            db (Session): The db session
            scanned_email_ids (List[int]): The scanned email ids to unsubscribe from
            linked_email (str): The linked email address
            user_id (int): The session user id

        Returns:
            list: The updated unsubscribe links
        """

        # Check first that this user owns the scanned_email
        linked_email = (
            db.query(LinkedEmails)
            .filter(
                LinkedEmails.email == linked_email,
                LinkedEmails.user_id == user_id,
            )
            .first()
        )

        if not linked_email:
            raise HTTPException(
                status_code=400, detail=f"Could not find linked email"
            )

        links = (
            db.query(UnsubscribeLinks)
            .filter(
                UnsubscribeLinks.linked_email_address == linked_email,
                UnsubscribeLinks.scanned_email_id.in_(scanned_email_ids),
            )
            .all()
        )

        for link in links:
            
            res = requests.get(link)

            # TODO: Do something with the res.text. We could possibly parse it
            # to see if there is another 'click' needed to unsubscribe.
            if res.status_code == 200:
                link.unsubscribe_status = UnsubscribeStatus.success
            else:
                link.unsubscribe_status = UnsubscribeStatus.failure
        
        db.commit()

        return links



unsubscribe_links = CRUDUnsubscribeLinks(UnsubscribeLinks)
