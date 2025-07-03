from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    """
    Render the main page.

    Returns:
        HTMLResponse: The rendered HTML page.
    """
    
    return templates.TemplateResponse("index.html", {"request": request})