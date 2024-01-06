from typing import Optional, List

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


class UnsubscribeEmail(BaseModel):
    email_sender: List[int]
    linked_email_address: EmailStr
    page: int = 0

class UnsubscribeFromAll(BaseModel):
    linked_email_address: EmailStr

class UnsubscribeFromSenders(BaseModel):
    email_senders: List[str]
    linked_email_address: EmailStr


# Placeholder
class UnsubscribeEmailUpdate(BaseModel):
    pass
