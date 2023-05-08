import enum

from sqlalchemy import Column, DateTime, Enum, Integer, ForeignKey, String
from sqlalchemy.sql import func

from app.database.base_class import Base


class UnsubscribeStatus(enum.Enum):
    """Unsubscribe status enum type."""

    success = "success"
    pending = "pending"
    failure = "failure"
    unsure = "unsure"


class UnsubscribeLinks(Base):
    """The unsubscribe_links table.
    We scan a user's inbox for spam and when we find an email with an unsubscribe link
    we add an entry to this table. It references an email sender and a linked_email.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    link = Column(String, nullable=False)
    unsubscribe_status = Column(Enum(UnsubscribeStatus), nullable=False)
    insert_ts = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    scanned_email_id = Column(
        Integer, ForeignKey("scanned_emails.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    linked_email_address = Column(
        String,
        ForeignKey("linked_emails.email", ondelete="CASCADE", onupdate="CASCADE"),
    )
