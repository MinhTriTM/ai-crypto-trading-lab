"""WebSocket market - stream gia realtime."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, json, random, time

router = APIRouter()

@router.websocket("/ws/market/{symbol}")
async def ws_market(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        price = 67000
        while True:
            price += random.uniform(-5, 5)
            await websocket.send_json({"symbol": symbol, "price": price, "timestamp": int(time.time()*1000)})
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"WS market {symbol} disconnected")
