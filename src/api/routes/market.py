"""Market routes."""
from fastapi import APIRouter
import random, time

router = APIRouter()

@router.get("/price/{symbol}")
async def get_price(symbol: str):
    # mock realtime price
    base = 67000 if "BTC" in symbol else 3400
    price = base + random.uniform(-100, 100)
    return {"symbol": symbol, "price": price, "timestamp": int(time.time()*1000)}

@router.get("/orderbook/{symbol}")
async def get_orderbook(symbol: str):
    price = 67000
    bids = [[price - i*0.5, random.uniform(0.1, 2)] for i in range(1, 6)]
    asks = [[price + i*0.5, random.uniform(0.1, 2)] for i in range(1, 6)]
    return {"symbol": symbol, "bids": bids, "asks": asks}

@router.get("/features/{symbol}")
async def get_features(symbol: str):
    import numpy as np
    return {"symbol": symbol, "features": np.random.randn(32).tolist(), "imbalance": random.uniform(-0.5, 0.5)}
