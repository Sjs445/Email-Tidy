import requests

from typing import List

from app.database.database import SessionLocal
from app.config import security
from app.config.config import settings
from app.models.linked_emails import LinkedEmails
from app.models.scanned_emails import ScannedEmails
from app.models.unsubscribe_links import UnsubscribeLinks, UnsubscribeStatus
from app.objects.email_unsubscriber import EmailUnsubscriber

from celery import Celery
from sqlalchemy.orm import Session

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery.task(name="scan_emails", bind=True)
def scan_emails(self, domain: str, linked_email_id: int, user_id: int, range_params: tuple) -> int:
    """A task method for EmailUnsubscriber._do_scan_emails

    Args:
        domain (str): The email domain
        linked_email_id (int): The linked email id to scan
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

        if not linked_email:
            raise Exception(f"Could not find linked email {linked_email_id}")

        linked_email.scan_task_id = self.request.id
        db.commit()

        domain = EmailUnsubscriber.get_domain_from_email(
            email_address=linked_email.email
        )
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
            db=db,
        )
    
    finally:
        remove_task_id_from_linked_email(db, linked_email_id, 'scan')
        del email_unsubscriber
        db.close()

    return spam_emails_found

@celery.task(name="unsubscribe_from_all", bind=True)
def unsubscribe_from_all(self, linked_email_id: int, user_id: int) -> int:
    """Unsubscribe from all emails associated with this linked email address.

    Args:
        linked_email_id (int): The linked email address
        user_id (int): the session user id

    Returns:
        int: The number of email unsubscribed from
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

        if not linked_email:
            raise Exception(f"Could not find linked email {linked_email_id}")

        linked_email.unsubscribe_task_id = self.request.id
        db.commit()

        links = (
            db.query(UnsubscribeLinks)
            .filter(
                UnsubscribeLinks.linked_email_address == linked_email.email,
                UnsubscribeLinks.unsubscribe_status == UnsubscribeStatus.pending,
            )
            .all()
        )

        total_links = len(links)

        for idx, link in enumerate(links):

            try:
                res = requests.get(link.link, timeout=5)
                # TODO: Do something with the res.text. We could possibly parse it
                # to see if there is another 'click' needed to unsubscribe.
                if res.status_code == 200:
                    link.unsubscribe_status = UnsubscribeStatus.success
                else:
                    link.unsubscribe_status = UnsubscribeStatus.failure
            except:
                link.unsubscribe_status = UnsubscribeStatus.failure

            self.update_state(
                state='PROGRESS',
                meta={
                    'current': idx,
                    'total': total_links
                }
            )

        db.commit()
    
    finally:
        remove_task_id_from_linked_email(db, linked_email_id, 'unsubscribe')
        db.close()

@celery.task(name="unsubscribe_from_senders", bind=True)
def unsubscribe_from_senders(self, linked_email_id: int, user_id: int, email_senders: List[str]) -> int:
    """Unsubscribe from selected senders associated with this linked email address.

    Args:
        linked_email_id (int): The linked email address
        user_id (int): the session user id
        email_senders (List[str]): A list of email senders

    Returns:
        int: The number of email unsubscribed from
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

        if not linked_email:
            raise Exception(f"Could not find linked email {linked_email_id}")

        linked_email.unsubscribe_task_id = self.request.id
        db.commit()

        links = (
            db.query(UnsubscribeLinks)
            .join(ScannedEmails, ScannedEmails.id == UnsubscribeLinks.scanned_email_id)
            .filter(
                UnsubscribeLinks.linked_email_address == linked_email.email,
                UnsubscribeLinks.unsubscribe_status == UnsubscribeStatus.pending,
                ScannedEmails.email_from.in_(email_senders),
            )
            .all()
        )

        total_links = len(links)

        for idx, link in enumerate(links):

            try:
                res = requests.get(link.link, timeout=5)
                # TODO: Do something with the res.text. We could possibly parse it
                # to see if there is another 'click' needed to unsubscribe.
                if res.status_code == 200:
                    link.unsubscribe_status = UnsubscribeStatus.success
                else:
                    link.unsubscribe_status = UnsubscribeStatus.failure
            except:
                link.unsubscribe_status = UnsubscribeStatus.failure

            self.update_state(
                state='PROGRESS',
                meta={
                    'current': idx,
                    'total': total_links
                }
            )

        db.commit()
    
    finally:
        remove_task_id_from_linked_email(db, linked_email_id, 'unsubscribe')
        db.close()

def remove_task_id_from_linked_email(db: Session, linked_email_id: int, job_type: str):
    """Remove the task_id from a linked_email object.
    This is run when a task has ended or when the task has failed.

    Args:
        db (Session): The db session
        linked_email_id (int): The linked_email_id to update
        job_type (str): Must be scan or unsubscribe
    """
    linked_email = (
        db.query(LinkedEmails)
        .filter(LinkedEmails.id == linked_email_id)
        .first()
    )

    if job_type == 'scan':
        linked_email.scan_task_id = None
    elif job_type == 'unsubscribe':
        linked_email.unsubscribe_task_id = None
    else:
        raise Exception(f"Unkown job_type {job_type}")

    db.commit()
