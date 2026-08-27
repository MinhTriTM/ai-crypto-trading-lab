"""Return metrics."""
import numpy as np

def total_return(start: float, end: float) -> float:
    return (end-start)/start if start else 0

def annualized_return(returns: list[float], periods_per_year: int = 365*24*60) -> float:
    if not returns: return 0.0
    total = np.prod([1+r for r in returns]) - 1
    n = len(returns)
    return (1+total)**(periods_per_year/n) - 1 if n else 0

def return_metrics(equities: list[float]) -> dict:
    if len(equities) < 2:
        return {"total":0, "mean":0, "std":0}
    rets = [(equities[i]-equities[i-1])/equities[i-1] for i in range(1,len(equities))]
    return {"total": total_return(equities[0], equities[-1]), "mean": float(np.mean(rets)), "std": float(np.std(rets)), "min": float(np.min(rets)), "max": float(np.max(rets))}

def cagr(start: float, end: float, days: int) -> float:
    if start<=0 or days<=0: return 0.0
    return (end/start)**(365/days) - 1
