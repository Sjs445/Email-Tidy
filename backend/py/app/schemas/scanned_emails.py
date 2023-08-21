from typing import Optional

from pydantic import BaseModel, EmailStr


class ScanEmails(BaseModel):
    linked_email_id: int
    how_many: Optional[int] = 10
    order_by: Optional[str] = "desc"


class ScannedEmailsCreate(BaseModel):
    email_from: EmailStr
    subject: Optional[str] = None
    linked_email_address: Optional[EmailStr] = None


class ScannedEmailUpdate(BaseModel):
    email_from: EmailStr
    linked_email_address: EmailStr
