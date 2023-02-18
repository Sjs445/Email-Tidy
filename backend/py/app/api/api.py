from fastapi import APIRouter

from app.api.endpoints import users, linked_emails, login

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    linked_emails.router, prefix="/linked_emails", tags=["linked_emails"]
)
api_router.include_router(login.router, prefix="/login", tags=["login"])
