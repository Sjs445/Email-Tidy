import re

from typing import List, Optional

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

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[dict]:
        """Get all linked_email entries by user_id

        Args:
            db (Session): The db session
            user_id (int): the user_id

        Returns:
            List[dict]: A list of dictionary data about the linked emails
        """
        results = (
            db.query(LinkedEmails.email, LinkedEmails.id, LinkedEmails.is_active)
            .filter(LinkedEmails.user_id == user_id)
            .all()
        )

        return [
            {"email": result[0], "id": result[1], "is_active": result[2]}
            for result in results
        ]

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
        domain = EmailUnsubscriber.get_domain_from_email(obj_in.email)
        email_unsubscriber = EmailUnsubscriber(email_type=domain)

        if not email_unsubscriber.login(
            email_username=obj_in.email, email_password=obj_in.password
        ):
            raise HTTPException(
                status_code=400, detail=f"Login failed for email: {obj_in.email}"
            )
        del email_unsubscriber

        # Encrypt the app password for this linked_email
        obj_in.password = security.encrypt_email_password(obj_in.password)
        obj_in.user_id = user_id
        db_obj = LinkedEmails(
            email=obj_in.email, password=obj_in.password, user_id=obj_in.user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


linked_email = CRUDLinkedEmails(LinkedEmails)