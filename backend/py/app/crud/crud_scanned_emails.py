import re

from typing import List, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.scanned_emails import ScannedEmails
from app.models.unsubscribe_links import UnsubscribeLinks
from app.models.linked_emails import LinkedEmails
from app.objects.email_unsubscriber import EmailUnsubscriber
from app.schemas.scanned_emails import (
    ScanEmails,
    ScannedEmailsCreate,
    ScannedEmailUpdate,
)
from app.config import security


class CRUDScannedEmails(
    CRUDBase[ScannedEmails, ScannedEmailsCreate, ScannedEmailUpdate]
):
    def scan_emails(self, db: Session, *, obj_in: ScanEmails, user_id: int) -> int:
        """Scan emails from a linked_email address.

        Args:
            db (Session): The db session
            obj_in (ScanEmails): The scan email params.
            user_id (int): the session user's user_id.

        Returns:
            int: The number of scanned emails
        """

        # Get the linked_email from the db
        linked_email = (
            db.query(LinkedEmails)
            .filter(
                LinkedEmails.email == obj_in.linked_email_address,
                LinkedEmails.user_id == user_id,
            )
            .first()
        )
        if not linked_email:
            raise HTTPException(
                status_code=400,
                detail=f"Could not find linked email for email '{obj_in.linked_email_address}'",
            )

        domain = EmailUnsubscriber.get_domain_from_email(
            email_address=obj_in.linked_email_address
        )
        email_unsubscriber = EmailUnsubscriber(email_type=domain)

        # Login the user and scan the emails.
        if not email_unsubscriber.login(
            email_username=linked_email.email,
            email_password=security.decrypt_email_password(linked_email.password),
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Could not login for linked email '{linked_email.email}'",
            )
        scanned = email_unsubscriber.get_unsubscribe_links_from_inbox(db)
        del email_unsubscriber
        return scanned

    def get_scanned_emails(
        self, db: Session, *, page: int = 0, email_from: str = None
    ) -> List[dict]:
        """Get a paginated list of scanned emails. Optionally filter by a specific email from address.

        Args:
            db (Session): The db session
            page (int, optional): The page to fetch. Defaults to 0.
            email_from (str, optional): An email to filter by. Defaults to None.

        Returns:
            List[dict]: The scanned email data
        """
        # TODO: Try to get the scanned_email data with a count of their unsubscribe_links
        # results = db.execute(
        #     """SELECT se.id, se.email_from, se.subject, se.linked_email_address
        #     FROM scanned_emails AS se
        #     INNER JOIN unsubscribe_links AS ul
        #     ON se.id = ul.scanned_email_id

        #     """
        # )
        return []


scanned_emails = CRUDScannedEmails(ScannedEmails)
