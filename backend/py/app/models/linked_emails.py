from sqlalchemy import Boolean, Column, Integer, ForeignKey, String

from app.database.base_class import Base


class LinkedEmails(Base):
    """The linked_emails table. This table holds a linked email account to an email-tidy user.
    When a user links an email account to their email-tidy account an entry is created here and
    we perform a check on this email account for spam.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
