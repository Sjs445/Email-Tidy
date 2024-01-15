import pytz
import secrets

from datetime import datetime, timedelta
from typing import Optional, Tuple

from jose import jwt

from app.config.config import settings
from app.models.invite_codes import InviteCodes

from sqlalchemy.orm import Session


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None

def generate_invite_code(db: Session, expires_in: float) -> Tuple[str, datetime]:
    """Generate an invite code for registration.

    Args:
        db (Session): The db session
        expires_in (float): Time in minutes to expire

    Returns:
        str: The invite code
    """
    # Convert expires_in to a datetime timestamp
    expire_ts = datetime.now(tz=pytz.UTC) + timedelta(minutes=expires_in)

    # Generate a 32 byte invite code
    code = secrets.token_urlsafe(32)

    # Create the db entry
    invite_code = InviteCodes(
        code=code,
        expire_ts=expire_ts,
    )
    db.add(invite_code)
    db.commit()

    return code, expire_ts
