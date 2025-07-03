from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from app.routes.pages import router as pages_router
from app.routes.analysis import router as analysis_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(pages_router, tags=["pages"])
app.include_router(analysis_router, tags=["analysis"])

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom exception handler for 404 errors.

    Returns a custom 404 page for 404 errors.
    For other errors, it falls back to the default HTTP exception handler.
    """
    if exc.status_code == 404:
        return templates.TemplateResponse("not_found.html", {"request": request}, status_code=404)
    return await http_exception_handler(request, exc)