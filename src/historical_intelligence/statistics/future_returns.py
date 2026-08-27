"""Future returns - thong ke return tuong lai tu lich su."""
import numpy as np

def future_returns(prices: np.ndarray, horizons: list[int] = [10, 100, 1000]) -> dict:
    """Tinh return cho cac horizon tinh bang so tick."""
    out = {}
    for h in horizons:
        if len(prices) > h:
            rets = (prices[h:] - prices[:-h]) / prices[:-h]
            out[h] = {"mean": float(np.mean(rets)), "std": float(np.std(rets)), "median": float(np.median(rets))}
        else:
            out[h] = {"mean": 0, "std": 0, "median": 0}
    return out

def conditional_returns(neighbors_returns: list[float]) -> dict:
    arr = np.array(neighbors_returns)
    return {"mean": float(np.mean(arr)), "std": float(np.std(arr)), "p_positive": float((arr>0).mean()), "n": len(arr)}
