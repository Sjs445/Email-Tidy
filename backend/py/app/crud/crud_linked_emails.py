import re

from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.linked_emails import LinkedEmails
from app.objects.email_unsubscriber import EmailUnsubscriber
from app.schemas.linked_emails import LinkedEmailsCreate, LinkedEmailsUpdate
from app.config import security


class CRUDLinkedEmails(CRUDBase[LinkedEmails, LinkedEmailsCreate, LinkedEmailsUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[LinkedEmails]:
        """Get a linked_email by email address.

        Args:
            db (Session): The db session
            email (str): The email to retrieve

        Returns:
            Optional[LinkedEmails]: The linked email object
        """
        return db.query(LinkedEmails).filter(LinkedEmails.email == email).first()

    def create_with_user(
        self, db: Session, *, obj_in: LinkedEmailsCreate, user_id: int
    ) -> LinkedEmails:
        """Create a linked_email entry for a user.

        Args:
            db (Session): The db session
            obj_in (LinkedEmailsCreate): The request params.
            user_id (int): The user_id creating the linked_email entry.

        Returns:
            LinkedEmails: The newly created linked_email object
        """

        # Get the email domain
        domain_match = re.search(r"@[\w\-]+", obj_in.email)
        if not domain_match:
            raise HTTPException(
                status_code=400,
                detail=f"Could not find email domain for email: {obj_in.email}",
            )

        # Chop off the '@'
        domain = domain_match.group()[1:]
        email_unsubscriber = EmailUnsubscriber(email_type=domain)

        if not email_unsubscriber.login(
            email_username=obj_in.email, email_password=obj_in.password
        ):
            raise HTTPException(
                status_code=400, detail=f"Login failed for email: {obj_in.email}"
            )

        # Encrypt the app password for this linked_email
        obj_in.password = security.encrypt_email_password(obj_in.password)
        obj_in.user_id = user_id
        return self.create(db, obj_in=obj_in)


linked_email = CRUDLinkedEmails(LinkedEmails)
