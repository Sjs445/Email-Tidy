from app.database.database import SessionLocal
from app.config import security
from app.config.config import settings
from app.models.linked_emails import LinkedEmails
from app.objects.email_unsubscriber import EmailUnsubscriber

from celery import Celery
from sqlalchemy.orm import Session

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery.task(name="scan_emails", bind=True)
def scan_emails(self, domain: str, linked_email_id: int, user_id: int, range_params: tuple, how_many: int) -> int:
    """A task method for EmailUnsubscriber._do_scan_emails

    Args:
        email_unsubscriber (EmailUnsubscriber): The email unsubscriber instance
        range_params (tuple): The range params to fetch emails from the inbox
        db (Session): The db session

    Returns:
        int: The number of emails that found unsubscribe links
    """
    db = SessionLocal()

    try:
        # Get the linked_email from the db
        linked_email = (
            db.query(LinkedEmails)
            .filter(
                LinkedEmails.id == linked_email_id,
                LinkedEmails.user_id == user_id,
            )
            .first()
        )
        linked_email.task_id = self.request.id
        db.commit()

        if not linked_email:
            raise Exception(f"Could not find linked email {linked_email_id}")
        
        domain = EmailUnsubscriber.get_domain_from_email(
            email_address=linked_email.email
        )
        email_unsubscriber = EmailUnsubscriber(domain)
        email_unsubscriber = EmailUnsubscriber(email_type=domain)

        # Login the user and scan the emails.
        if not email_unsubscriber.login(
            email_username=linked_email.email,
            email_password=security.decrypt_email_password(linked_email.password),
        ):
            raise Exception(
                f"Could not login for linked email '{linked_email.email}'",
            )
        
        # Scan emails for spam
        spam_emails_found = email_unsubscriber._do_scan_emails(
            task=self,
            range_params=range_params,
            how_many=how_many,
            db=db,
        )
    
    finally:
        remove_task_id_from_linked_email(db, linked_email_id)
        db.close()

    return spam_emails_found


def remove_task_id_from_linked_email(db: Session, linked_email_id: int):
    """Remove the task_id from a linked_email object.
    This is run when a task has ended or when the task has failed.

    Args:
        db (Session): The db session
        linked_email_id (int): The linked_email_id to update
    """
    linked_email = (
        db.query(LinkedEmails)
        .filter(LinkedEmails.id == linked_email_id)
        .first()
    )
    linked_email.task_id = None
    db.commit()