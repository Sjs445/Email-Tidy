from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.sql import func

from app.database.base_class import Base


class ScannedEmails(Base):
    """The scanned emails table.
    We scan a user's inbox for spam and when we find an email with unsubscribe links
    we add the email info to this table.
    NOTE: We do not store any of the content of the email just the sender's address
    and the email subject.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_from = Column(String, nullable=False)
    subject = Column(String)
    insert_ts = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    linked_email_address = Column(
        String,
        ForeignKey("linked_emails.email", ondelete="CASCADE", onupdate="CASCADE"),
    )