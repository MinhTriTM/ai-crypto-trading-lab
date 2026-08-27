"""Simulation routes."""
from fastapi import APIRouter
from pydantic import BaseModel
from src.simulation.environment import TradingEnv
from src.simulation.episode_runner import EpisodeRunner
from src.ai.agent.trading_agent import TradingAgent

router = APIRouter()

class SimReq(BaseModel):
    episodes: int = 10
    max_steps: int = 1000

@router.post("/run")
async def run_simulation(req: SimReq):
    episodes = []
    for _ in range(req.episodes):
        env = TradingEnv()
        agent = TradingAgent()
        runner = EpisodeRunner(env, agent)
        ep = runner.run(max_steps=req.max_steps)
        episodes.append(ep.to_dict())
    avg = sum(e["return"] for e in episodes)/len(episodes) if episodes else 0
    return {"episodes": episodes, "avg_return": avg, "count": len(episodes)}

@router.get("/scenarios")
async def list_scenarios():
    from src.simulation.scenario import ScenarioType
    return [s.value for s in ScenarioType]
