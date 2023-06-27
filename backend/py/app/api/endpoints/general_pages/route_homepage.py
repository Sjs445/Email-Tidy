"""Home page routers. These requests serve html files as the front-end.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


from app.api import deps
from app.models.users import User

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(
    request: Request, user: User = Depends(deps.get_current_user), msg: str = None
):
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "msg": msg}
    )
