"""Training routes."""
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

router = APIRouter()
_status = {"running": False, "progress": 0, "timesteps": 0}

class TrainReq(BaseModel):
    algorithm: str = "ppo"
    total_timesteps: int = 1_000_000
    config_path: str = "config/training.yaml"

def _train_task(req: TrainReq):
    import time
    _status["running"] = True
    for i in range(10):
        time.sleep(0.1)
        _status["progress"] = (i+1)*10
        _status["timesteps"] = int(req.total_timesteps * (i+1)/10)
    _status["running"] = False

@router.post("/start")
async def start_training(req: TrainReq, background: BackgroundTasks):
    background.add_task(_train_task, req)
    return {"status": "started", "config": req.dict()}

@router.get("/status")
async def get_status():
    return _status

@router.post("/stop")
async def stop_training():
    _status["running"] = False
    return {"status": "stopped"}
