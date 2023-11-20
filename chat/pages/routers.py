from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

pages_router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="chat/templates")
print(templates)


@pages_router.get("/room/{room_id}")
def get_chat_page(request: Request, room_id: int):
    return templates.TemplateResponse("room_chat.html", {"request": request, "room_id": room_id})
