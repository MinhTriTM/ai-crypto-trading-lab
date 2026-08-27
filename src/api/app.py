"""FastAPI app."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import accounts, market, training, simulation, models

app = FastAPI(title="AI Crypto Trading Lab", version="0.1.0", description="Thi truong that - Tien ao - San mo phong")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(training.router, prefix="/api/training", tags=["training"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])
app.include_router(models.router, prefix="/api/models", tags=["models"])

@app.get("/")
async def root():
    return {"name": "AI Crypto Trading Lab", "version": "0.1.0", "status": "running", "principle": "Thi truong that, tien ao, san mo phong"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# websocket
from .websocket.market import router as ws_market
from .websocket.training import router as ws_training
app.include_router(ws_market)
app.include_router(ws_training)
