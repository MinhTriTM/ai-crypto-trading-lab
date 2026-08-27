"""Evolutionary training."""
import random
import numpy as np
from src.branching.population.population import Population
from src.branching.population.selection import tournament_selection
from src.branching.population.mutation import mutate
from src.branching.population.crossover import crossover

class EvolutionaryTrainer:
    def __init__(self, population: Population, fitness_fn, mutation_rate: float = 0.3):
        self.pop = population
        self.fitness_fn = fitness_fn
        self.mutation_rate = mutation_rate

    def evolve(self, generations: int = 100, pop_size: int = 100):
        for g in range(generations):
            # danh gia
            scored = [(s, self.fitness_fn(s)) for s in self.pop.states]
            scored.sort(key=lambda x: x[1], reverse=True)
            best = scored[0][1]
            print(f"Gen {g} best fitness={best:.3f}")
            # chon loc
            survivors = [s for s,_ in scored[:pop_size//2]]
            # sinh con
            children = []
            while len(children) < pop_size//2:
                if random.random() < 0.5:
                    parent = tournament_selection(survivors)
                    children.append(mutate(parent.branch, self.mutation_rate))
                else:
                    a,b = random.sample(survivors, 2)
                    children.append(crossover(a.branch, b.branch))
            # placeholder: tao state moi
            self.pop.generation += 1
        return self.pop
