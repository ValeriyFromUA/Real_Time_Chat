from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from chat.config import ORIGINS
from chat.guest.routers import router as guest_router
from chat.message.routers import router as message_router
from chat.room.routers import router as room_router
from chat.category.routers import router as category_router
from chat.pages.routers import pages_router

app = FastAPI()

app.include_router(guest_router)
app.include_router(message_router)
app.include_router(room_router)
app.include_router(category_router)
app.include_router(pages_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.get('/')
async def healthcheck():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
