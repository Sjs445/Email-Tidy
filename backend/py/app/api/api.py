from fastapi import APIRouter

from app.api.endpoints import users, linked_emails

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    linked_emails.router, prefix="/linked_emails", tags=["linked_emails"]
)
