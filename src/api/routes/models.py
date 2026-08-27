"""Models routes."""
from fastapi import APIRouter
from src.storage.repositories.model_repository import ModelRepository

router = APIRouter()
repo = ModelRepository()

@router.get("/")
async def list_models():
    import pathlib
    p = repo.base / "checkpoints"
    if not p.exists():
        return []
    return [f.stem for f in p.glob("*.json")]

@router.get("/{name}")
async def get_model(name: str):
    data = repo.load(name)
    if not data:
        return {"error": "not found"}
    return data

@router.post("/{name}/promote")
async def promote(name: str):
    repo.promote(name)
    return {"promoted": name}
