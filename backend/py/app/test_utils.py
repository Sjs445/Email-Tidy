import random
import string

from datetime import timedelta
from email.message import EmailMessage

from app.crud import crud_user
from app.config import security
from app.models.users import User
from app.database.database import SessionLocal
from app.schemas.users import UserCreate

from sqlalchemy.orm import Session


def get_session() -> Session:
    """Get a db session.

    Returns:
        Session: The db session.
    """
    return SessionLocal()


def generate_user(db: Session) -> User:
    """Generate a test user

    Returns:
        User: The newly created user
    """
    email = f"testuser{random.randint(0, 100)}@test-email.com"
    user = crud_user.user.create(
        db,
        obj_in=UserCreate(
            email=email,
            first_name="test_user_first_name",
            last_name="test_user_last_name",
            password="".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(12)
            ),
            invite_code="",
        ),
    )
    return user


def generate_auth_header(user_id: int) -> dict:
    """Generate an authorization header.

    Args:
        user_id (int): The user id to generate the header for

    Returns:
        dict: The header info
    """
    return {
        "Authorization": f"Bearer {security.create_access_token(user_id, expires_delta=timedelta(minutes=5))}"
    }


def generate_email_message(
    to_email: str, from_email: str, subject: str, body: str, list_unsubscribe: list,
) -> EmailMessage:
    """Generate an email message object. Currently only supports html
    emails. TODO: text/plain

    Args:
        to_email (str): The recipient email address
        from_email (str): The sender email address
        subject (str): The subject of the email
        body (str): The body of the email
        list_unsubscribe (list): A list of unsubscribe links to add as the List-Unsubscribe header

    Returns:
        EmailMessage: The email message object
    """
    message = EmailMessage()

    message.add_header("To", to_email)
    message.add_header("From", from_email)
    message.add_header("Subject", subject)
    message.add_header("List-Unsubscribe", ",".join(list_unsubscribe))
    message.set_content(body)

    # TODO: pass a param for either text/plain or text/html?
    message.replace_header("content-type", "text/html")
    return message
