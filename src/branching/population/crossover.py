"""Crossover."""
import random
from ..branch import Branch
import copy

def crossover(a: Branch, b: Branch) -> Branch:
    child = copy.deepcopy(a)
    child.id = a.id[:2] + b.id[:2] + str(random.randint(10,99))
    child.parent_id = a.id
    # tron gen
    child.symbol = random.choice([a.symbol, b.symbol])
    child.position_pct = (a.position_pct + b.position_pct)/2
    child.leverage = random.choice([a.leverage, b.leverage])
    child.action = random.choice([a.action, b.action])
    child.depth = max(a.depth, b.depth) + 1
    return child

def crossover_population(parents: list[Branch], n_children: int = 10) -> list[Branch]:
    children = []
    for _ in range(n_children):
        a,b = random.sample(parents, 2)
        children.append(crossover(a,b))
    return children
