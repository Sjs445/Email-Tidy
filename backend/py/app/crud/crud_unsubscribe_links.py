from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.unsubscribe_links import UnsubscribeLinks
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
    ) -> list:
        """Get unsubscribe links by a scanned email and linked email address.

        Args:
            db (Session): The db session
            linked_email_address (str): the linked email
            scanned_email_id (int): the scanned email id

        Returns:
            list: The list of unsubscribe links found.
        """

        # TODO: Make sure this query joins with a user_id.
        links = (
            db.query(UnsubscribeLinks)
            .filter(
                UnsubscribeLinks.linked_email_address == linked_email_address,
                UnsubscribeLinks.scanned_email_id == scanned_email_id,
            )
            .all()
        )

        return links


unsubscribe_links = CRUDUnsubscribeLinks(UnsubscribeLinks)
