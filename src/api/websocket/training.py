"""WebSocket training - stream tien trinh train."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, random

router = APIRouter()

@router.websocket("/ws/training")
async def ws_training(websocket: WebSocket):
    await websocket.accept()
    try:
        step = 0
        while True:
            step += 1000
            await websocket.send_json({"step": step, "reward": random.uniform(-1, 1), "loss": random.uniform(0.1, 1.0)})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WS training disconnected")
