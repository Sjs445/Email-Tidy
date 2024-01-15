from typing import Optional

from pydantic import BaseModel, EmailStr


class ScanEmails(BaseModel):
    linked_email_id: int


class ScannedEmailsCreate(BaseModel):
    email_from: EmailStr
    subject: Optional[str] = None
    linked_email_address: Optional[EmailStr] = None


class ScannedEmailUpdate(BaseModel):
    email_from: EmailStr
    linked_email_address: EmailStr

class GetScannedEmails(BaseModel):
    email_from: str
    linked_email: EmailStr
    page: int = 0
