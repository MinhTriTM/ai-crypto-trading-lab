"""ModelRepository."""
from pathlib import Path
import json, time

class ModelRepository:
    def __init__(self, base: str = "models"):
        self.base = Path(base)
    def save(self, name: str, metadata: dict):
        path = self.base / "checkpoints" / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        metadata["saved_at"] = int(time.time()*1000)
        path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        print(f"Model metadata saved {path}")
    def load(self, name: str) -> dict | None:
        path = self.base / "checkpoints" / f"{name}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding='utf-8'))
    def promote(self, name: str):
        src = self.base / "checkpoints" / f"{name}.json"
        dst = self.base / "production" / f"{name}.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
            print(f"Promoted {name} to production")
