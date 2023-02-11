import scrypt

from datetime import datetime, timedelta
from typing import Any, Union

from app.config.config import settings

from jose import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create a JWT access token for an authenticated user.

    Args:
        subject (Union[str, Any]): TODO
        expires_delta (timedelta, optional): The expire time for the access token. Defaults to None.

    Returns:
        str: The encoded JWT
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a user's password matches the hashed_password in the DB.

    Args:
        plain_password (str): The password to check
        hashed_password (str): The hash_password to check against

    Returns:
        bool: True if password matches, else False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get a hashed password from a plaintext password to
    store in the DB.

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def encrypt_email_password(plain_password: str) -> bytes:
    """Encrypt a linked_email generated app password.

    Args:
        plain_password (str): The password

    Returns:
        bytes: The encrypted password
    """
    return scrypt.encrypt(plain_password, settings.EMAIL_CRYPT_MASTER_PASS, maxtime=0.1)


def decrypt_email_password(encrypted_password: bytes) -> str:
    """Decrypt a linked_email app password.

    Args:
        encrypted_password (bytes): The encrypted password

    Returns:
        str: The plain text password
    """
    return scrypt.decrypt(
        encrypted_password, settings.EMAIL_CRYPT_MASTER_PASS, maxtime=0.1
    )
