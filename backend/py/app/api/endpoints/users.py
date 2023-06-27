from fastapi import APIRouter, Depends, HTTPException, Request, status, responses
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.users import User
from app.database.database import get_db
from app.forms.users import RegisterForm

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/register")
async def register_user(*, request: Request, db: Session = Depends(get_db)) -> dict:
    """Register a new user.

    Args:
        user_in (schemas.UserCreate): The new user to create.
        db (Session, optional): The db session. Defaults to Depends(get_db).

    Returns:
        dict: The response
    """
    form = RegisterForm(request)
    await form.load_data()
    if await form.is_valid():
        user_in = schemas.UserCreate(
            first_name=form.first_name,
            last_name=form.last_name,
            email=form.email,
            password=form.password,
        )

        user = crud.user.get_by_email(db, email=user_in.email)
        if user:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)

        user = crud.user.create(db, obj_in=user_in)

        # TODO: add session for user here so they don't get redirected to the login page

        return responses.RedirectResponse(
            "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
        )  # default is post request, to use get request added status code 302

    return templates.TemplateResponse("users/register.html", form.__dict__)


@router.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})
