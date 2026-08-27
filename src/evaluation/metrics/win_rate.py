"""Win rate."""
def win_rate(returns: list[float]) -> float:
    if not returns: return 0.0
    wins = sum(1 for r in returns if r > 0)
    return wins / len(returns)

def profit_factor(returns: list[float]) -> float:
    gains = sum(r for r in returns if r > 0)
    losses = abs(sum(r for r in returns if r < 0))
    if losses == 0:
        return float('inf') if gains>0 else 0.0
    return gains / losses

def avg_win_loss(returns: list[float]) -> dict:
    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r < 0]
    return {"avg_win": sum(wins)/len(wins) if wins else 0, "avg_loss": sum(losses)/len(losses) if losses else 0}
