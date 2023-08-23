from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    ForeignKey,
    String,
    LargeBinary,
    DateTime,
)
from sqlalchemy.sql import func

from app.database.base_class import Base


class LinkedEmails(Base):
    """The linked_emails table. This table holds a linked email account to an email-tidy user.
    When a user links an email account to their email-tidy account an entry is created here and
    we perform a check on this email account for spam.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=True)
    insert_ts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
