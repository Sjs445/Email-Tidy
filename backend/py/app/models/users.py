from sqlalchemy import Boolean, Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class User(Base):
    """The user account table. This table holds a user's account to use the
    email-tidy app, but we don't use this email to check for spam. That is handled
    in the linked_emails table.
    """

    # Specify 'users' because Postgres reserves the keyword 'user'.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    email = Column(String, primary_key=True, index=True, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    linked_emails = relationship("LinkedEmails")
    PrimaryKeyConstraint("id", "email", name="users_pk")
