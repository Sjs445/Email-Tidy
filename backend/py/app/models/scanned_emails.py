from sqlalchemy import Column, Integer, ForeignKey, String

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
    linked_email_address = Column(String, ForeignKey("linked_emails.email"))
