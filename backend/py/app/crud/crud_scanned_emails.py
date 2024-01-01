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
        
        # TODO: Currently our logic is create 1 celeryworker to scan the entire inbox.
        # This takes way too long when a user has thousands of emails. Instead, let's divide the work
        # into multiple celery tasks per linked email. This should in theory speed up the time it takes
        # to san an entire user's inbox.
        # 1. Change the linked_email task_id column to an array of task ids.
        # 2. When the front-end makes a request to scan emails allow the backend to check how many emails
        #      a user has, then divide up the work into a number of taskworkers scanning seperate parts of
        #      a user's inbox.
        # 3. To get the scan progress change the backend to accept a list of task_ids instead of just one
        #      and assemble the tasks states into one.
        task_id = email_unsubscriber.get_unsubscribe_links_from_inbox(
            linked_email_id=linked_email.id, user_id=user_id,
        )
        return task_id
    
    def get_senders_by_linked_email(
            self,
            db: Session,
            *,
            user_id: int,
            linked_email: str,
            page: int = 0,
    ) -> List[dict]:
        """Get a list of email senders that were scanned by linked_email.

        Args:
            db (Session): The db session
            user_id (int): The session user
            linked_email (str): The linked_email
            page (int, optional): The page to fetch. Defaults to 0.

        Returns:
            List[dict]: The sender data
        """
        linked_email = crud.linked_email.get_single_by_user_id(
            db, user_id=user_id, linked_email_address=linked_email
        )

        # Fetch 10 at a time
        offset = 0

        if page:
            offset = page * 10

        bind = {"linked_email": linked_email.email, "offset": offset}

        results = db.execute(
            f"""SELECT DISTINCT
                    email_from,
                    COUNT(DISTINCT se.id) AS scanned_email_count,
                    COUNT(ul.id) AS unsubscribe_link_count,
                    COUNT(*) OVER() as total_count,

                    -- Get an array of unsubscribe statuses for this sender. Cast back to text array so sqlalchemy can return as a list in python
                    ( array_agg( ul.unsubscribe_status ) FILTER ( WHERE ul.unsubscribe_status IS NOT NULL ) )::text[] AS unsubscribe_statuses
                FROM
                    scanned_emails se
                LEFT OUTER JOIN
                    unsubscribe_links AS ul
                ON ul.scanned_email_id = se.id
                WHERE
                    se.linked_email_address = :linked_email
                GROUP BY email_from
                LIMIT 10
                OFFSET :offset
            """,
            bind
        ).all()
        return [ dict(res) for res in results ]

    def get_scanned_emails(
        self,
        db: Session,
        *,
        user_id: int,
        linked_email: str,
        email_from: str,
        page: int = 0,
    ) -> List[dict]:
        """Get a paginated list of scanned emails. Filter by a specific email from address.

        Args:
            db (Session): The db session
            user_id (int): The session user_id
            linked_email (str): Filter scanned_emails owned by a linked_email address.
            email_from (str): An email to filter by.
            page (int, optional): The page to fetch. Defaults to 0.
        Returns:
            List[dict]: The scanned email data
        """
        linked_email = crud.linked_email.get_single_by_user_id(
            db, user_id=user_id, linked_email_address=linked_email
        )

        if page:
            offset = page * 10
        else:
            offset = 0

        bind = {
            "email_from": email_from,
            "offset": offset
        }

        results = db.execute(
            f"""SELECT
                    se.id,
                    se.subject,
                    COUNT(ul.id) AS unsubscribe_link_count,
                    ( array_agg( ul.unsubscribe_status ) FILTER ( WHERE ul.unsubscribe_status IS NOT NULL ) )::text[] AS unsubscribe_statuses,
                    COUNT(*) OVER() as total_count
                FROM
                    scanned_emails AS se
                LEFT OUTER JOIN
                    unsubscribe_links AS ul
                ON
                    ul.scanned_email_id = se.id
                WHERE
                    se.email_from = :email_from
                GROUP BY se.id, se.insert_ts
                LIMIT 10
                OFFSET :offset
            """,
            bind,
        ).all()
        return [ dict(res) for res in results ]
    
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
