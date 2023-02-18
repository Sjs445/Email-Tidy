import random
import string

from app.crud import crud_user
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
