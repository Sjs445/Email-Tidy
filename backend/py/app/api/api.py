from fastapi import APIRouter

from app.api.endpoints import (
    users,
    linked_emails,
    login,
    scanned_emails,
    unsubscribe_links,
)

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    linked_emails.router, prefix="/linked_emails", tags=["linked_emails"]
)
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(
    scanned_emails.router, prefix="/scanned_emails", tags=["scanned_emails"]
)
api_router.include_router(
    unsubscribe_links.router, prefix="/unsubscribe_links", tags=["unsubscribe_links"]
)
