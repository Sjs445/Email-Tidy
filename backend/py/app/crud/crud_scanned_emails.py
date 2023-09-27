from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import crud
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
            int: The celery task id for scanning the emails
        """

        # Get the linked_email from the db
        linked_email = (
            db.query(LinkedEmails)
            .filter(
                LinkedEmails.id == obj_in.linked_email_id,
                LinkedEmails.user_id == user_id,
            )
            .first()
        )
        if not linked_email:
            raise HTTPException(
                status_code=400,
                detail=f"Could not find linked email",
            )

        domain = EmailUnsubscriber.get_domain_from_email(
            email_address=linked_email.email
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
        task_id = email_unsubscriber.get_unsubscribe_links_from_inbox(
            linked_email_id=linked_email.id, user_id=user_id, how_many=obj_in.how_many
        )
        return task_id

    def get_scanned_emails(
        self,
        db: Session,
        *,
        user_id: int,
        linked_email: str,
        page: int = 0,
        email_from: str = None,
    ) -> List[dict]:
        """Get a paginated list of scanned emails. Optionally filter by a specific email from address.

        Args:
            db (Session): The db session
            user_id (int): The session user_id
            linked_email (str): Filter scanned_emails owned by a linked_email address.
            page (int, optional): The page to fetch. Defaults to 0.
            email_from (str, optional): An email to filter by. Defaults to None.

        Returns:
            List[dict]: The scanned email data
        """
        linked_email = crud.linked_email.get_single_by_user_id(
            db, user_id=user_id, linked_email_address=linked_email
        )

        where = ""
        bind = {}

        if page:
            offset = page * 10
        else:
            offset = 0

        # Bind WHERE params for email_from and a linked_email_address
        where += "WHERE se.linked_email_address = :linked_email"
        where += " AND users.id = :user_id"
        bind["linked_email"] = linked_email.email
        bind["user_id"] = user_id

        if email_from is not None and isinstance(email_from, str):
            where += " AND se.email_from = :email_from"
            bind["email_from"] = email_from

        bind["offset"] = offset

        # SQL AUDIT: Parameters are passed using bind. SAFE.
        results = db.execute(
            f"""SELECT se.id, se.email_from, se.subject, se.linked_email_address, COUNT(ul.scanned_email_id) AS link_count, ul.unsubscribe_status
                    FROM scanned_emails AS se
                LEFT OUTER JOIN unsubscribe_links AS ul
                    ON ul.scanned_email_id = se.id
                INNER JOIN linked_emails AS le
                    ON le.email = se.linked_email_address
                INNER JOIN users
                    ON users.id = le.user_id
                {where}
                GROUP BY se.id, se.insert_ts, ul.unsubscribe_status
                LIMIT 10
                OFFSET :offset
            """,
            bind,
        ).all()
        return [
            {
                "id": res[0],
                "from": res[1],
                "subject": res[2],
                "linked_email_address": res[3],
                "link_count": res[4],
                "unsubscribe_status": res[5],
            }
            for res in results
        ]

    def count_scanned_emails(
        self,
        db: Session,
        *,
        user_id: int,
        linked_email: str,
    ) -> int:
        """Count the number of scanned emails for this linked email.

        Args:
            db (Session): The db session.
            user_id (int): The user_id.
            linked_email (str): The linked email address.

        Returns:
            int: The number of scanned emails.
        """
        linked_email_obj = crud.linked_email.get_single_by_user_id(
            db, user_id=user_id, linked_email_address=linked_email
        )

        count = (
            db.query(ScannedEmails)
            .filter(ScannedEmails.linked_email_address == linked_email_obj.email)
            .count()
        ) or 0

        return count
    
    def delete_scanned_emails(
            self,
            db: Session,
            *,
            user_id: int,
            linked_email: str,
    ) -> int:
        """Delete all scanned emails in this linked_email.
        NOTE this does not delete emails from the user's inbox, but only
        deletes the scanned_emails from the scanned_emails table linked to this linked_email.

        Args:
            db (Session): The db session
            user_id (int): The session user id
            linked_email (str): The linked email to delete from

        Returns:
            int: Number of deleted scanned emails
        """
        link_email_obj = crud.linked_email.get_single_by_user_id(
            db, user_id=user_id, linked_email_address=linked_email
        )

        deleted_count = db.execute(
            "DELETE FROM scanned_emails WHERE linked_email_id = :linked_email_id",
            {"linked_email_id": link_email_obj.id},
        ).count()
        db.commit()
        return deleted_count


scanned_emails = CRUDScannedEmails(ScannedEmails)
