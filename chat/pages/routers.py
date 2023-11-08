from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

pages_router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="chat\\templates")


@pages_router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
