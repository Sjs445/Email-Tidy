from typing import Optional

from pydantic import BaseModel, EmailStr


# Not used yet. Placeholders for crud_unsubscribe_links
class FetchUnsubscribeLinks(BaseModel):
    linked_email_address = EmailStr
    scanned_email_id: int
    order_by: Optional[str] = "desc"


# Placeholder
class UnsubscribeEmailsCreate(BaseModel):
    linked_email_address: EmailStr
    scanned_email_id: int
    link: str
    unsubscribe_status: str
    insert_ts: str


# Placeholder
class UnsubscribeEmailUpdate(BaseModel):
    pass
