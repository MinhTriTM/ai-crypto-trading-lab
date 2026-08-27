"""Serialization."""
import json, pickle
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)

def to_json(obj, indent: int = 2) -> str:
    return json.dumps(obj, cls=NumpyEncoder, indent=indent, ensure_ascii=False)

def from_json(s: str):
    return json.loads(s)

def to_pickle(obj, path: str):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def from_pickle(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)
