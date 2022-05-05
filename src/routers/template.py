from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
def get_basic_form(request: Request) -> Response:
    """
    This endpoint returns the basic form template with two forms that triggers /json2xml and /xml2json endpoints.

    Parameters:
    - **request**: Request object

    Returns TemplateResponse with index html webpage
    \f
    :param request: Request object
    :return: TemplateResponse with index html webpage
    """
    return templates.TemplateResponse("index.html", {"request": request})
