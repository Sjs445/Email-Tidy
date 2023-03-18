import random
import string

from datetime import timedelta

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
