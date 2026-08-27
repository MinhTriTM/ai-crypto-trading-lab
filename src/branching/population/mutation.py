"""Mutation."""
import random
from ..branch import Branch

def mutate(branch: Branch, mutation_rate: float = 0.3) -> Branch:
    import copy
    child = copy.deepcopy(branch)
    child.parent_id = branch.id
    child.id = branch.id[:3] + str(random.randint(100,999))
    if random.random() < mutation_rate:
        child.position_pct = max(0.01, min(0.5, child.position_pct + random.uniform(-0.05, 0.05)))
    if random.random() < mutation_rate:
        child.leverage = random.choice([1,2,3,5])
    if random.random() < mutation_rate:
        child.action = random.choice(["LONG","SHORT","HOLD"])
    if random.random() < mutation_rate:
        child.symbol = random.choice(["BTCUSDT","ETHUSDT","SOLUSDT"])
    child.depth += 1
    return child

def mutate_population(branches: list[Branch], rate: float = 0.3) -> list[Branch]:
    return [mutate(b, rate) for b in branches]
