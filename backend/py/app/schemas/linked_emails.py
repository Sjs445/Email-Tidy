from typing import Optional

from pydantic import BaseModel, EmailStr

# Shared properties
class LinkedEmailsBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


class LinkedEmailsCreate(LinkedEmailsBase):
    email: EmailStr
    password: str


class LinkedEmailsUpdate(LinkedEmailsBase):
    password: Optional[str] = None


class LinkedEmialsInDBBase(LinkedEmailsBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
