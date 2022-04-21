from typing import List

from fastapi import APIRouter
from fastapi.websockets import WebSocket

from app.chat import chat

router = APIRouter()


@router.websocket('/{user_id}/ws')
async def ws_connection(ws: WebSocket, user_id: str) -> None:
    await chat.handle_ws_connection(ws, user_id)


@router.get('/{user_id}/history')
async def get_history(user_id: str) -> List[str]:
    return await chat.get_history(user_id)
