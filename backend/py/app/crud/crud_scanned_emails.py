from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.scanned_emails import ScannedEmails
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
        self,
        db: Session,
        *,
        page: int = 0,
        email_from: str = None,
        linked_email: str = None,
    ) -> List[dict]:
        """Get a paginated list of scanned emails. Optionally filter by a specific email from address.

        Args:
            db (Session): The db session
            page (int, optional): The page to fetch. Defaults to 0.
            email_from (str, optional): An email to filter by. Defaults to None.
            linked_email (str, optional): Filter scanned_emails owned by a linked_email address.

        Returns:
            List[dict]: The scanned email data
        """
        where = ""
        bind = {}

        if page:
            offset = page * 10
        else:
            offset = 0

        # Bind WHERE params for email_from and a linked_email_address
        if email_from is not None and isinstance(email_from, str):
            where += "WHERE scanned_emails.email_from = :email_from"
            bind["email_from"] = email_from

        if bind and linked_email is not None and isinstance(linked_email, str):
            where += " AND scanned_emails.linked_email_address = :linked_email"
            bind["linked_email"] = linked_email

        bind["offset"] = offset

        # SQL AUDIT: Parameters are passed using bind. SAFE.
        results = db.execute(
            f"""SELECT scanned_emails.*, COUNT(unsubscribe_links.scanned_email_id) AS link_count
                    FROM scanned_emails
                LEFT OUTER JOIN unsubscribe_links
                    ON unsubscribe_links.scanned_email_id = scanned_emails.id
                {where}
                GROUP BY scanned_emails.id
                ORDER BY scanned_emails.insert_ts
                LIMIT 10
                OFFSET :offset
            """,
            bind,
        ).all()
        return [
            {
                "id": res[0],
                "email_from": res[1],
                "subject": res[2],
                "linked_email_address": res[3],
                "link_count": res[5],
            }
            for res in results
        ]


scanned_emails = CRUDScannedEmails(ScannedEmails)
