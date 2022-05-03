from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
def get_basic_form(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})
