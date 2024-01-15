from sqlalchemy.orm import Session

from app import crud, schemas
from app.config.config import settings
from app.database import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.database.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Create the admin user

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            first_name="admin",
            last_name="admin",
            invite_code='',
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
