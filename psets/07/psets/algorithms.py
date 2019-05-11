"""Algorithms."""

from .individuals import Individual


from typing import List, Tuple, Type
import numpy as np  # type: ignore
import random


class DE:
    """Differential evolution.

    Differential evolution is an optimization heuristic
    that doesn't require the optimization problem to be
    differentiable. It works by trying to improve a solution
    upon each iteration and sticking to the best solutions
    found.
    """

    def __init__(
        self,
        problem_class: Type[Individual],
        dimensions: int,
        search_space: Tuple[int, int],  # Define the range of each dimension
        population_size: int = 100,
        crossover_probability: float = 0.75,
        differential_weight: float = 0.5,
        maximum_iterations: int = 5000000,  # 5 x 10^6
        precision: float = 0.000001  # 10^(-6)
    ) -> None:
        """Initialize algorithm with control parameters."""
        self.PClass = problem_class
        self.D = dimensions
        self.S = search_space

        self.POP_SIZE = population_size
        self.CR = crossover_probability
        self.F = differential_weight
        self.MAX_ITERS = maximum_iterations
        self.PRECISION = precision

        self.generations = 0
        self.results = []  # type: List[Tuple[float, List[Individual]]]

    def run(self) -> None:
        """Run algorithm."""
        self.agents = self.initialize_agents()
        precision = self.agents_fitness(self.agents)
        pop_fitness = precision
        self.results.append((pop_fitness, self.agents))
        while self.generations < self.MAX_ITERS and precision > self.PRECISION:
            self.results.append((pop_fitness, self.agents))
            self.agents = self.mutate_agents(self.agents)
            new_pop_fitness = self.agents_fitness(self.agents)
            precision = abs(pop_fitness - new_pop_fitness)
            pop_fitness = new_pop_fitness
            self.generations += 1

    def initialize_agents(self) -> List[Individual]:
        """Randomly place agents withing the given search space."""
        agents = []  # type: List[Individual]
        while len(agents) < self.POP_SIZE:
            chromosome = [float(random.randint(self.S[0], self.S[1])) for _ in range(self.D)]
            agents.append(self.PClass(chromosome))
        return agents

    def mutate_agents(self, agents: List[Individual]) -> List[Individual]:
        """Mutate agents by following DE's formulae."""
        new_agents = []
        for i in range(self.POP_SIZE):
            agent = agents[i]

            # Pick 3 distinct agents randomly.
            a, b, c = random.choices(agents, k=3)
            while len(set([a, b, c, agent])) < 4:
                a, b, c = random.choices(agents, k=3)

            # Set up replacement agent
            new_chromosome = agent.chromosome[:]
            R = random.randint(0, self.D - 1)
            for j in range(self.D):
                ri = random.random()
                if ri < self.CR or j == R:
                    ai = a.chromosome[j]
                    bi = b.chromosome[j]
                    ci = c.chromosome[j]
                    new_y = ai + (self.F * (bi - ci))
                    new_chromosome[j] = self.reflect_gene(new_y)

            # Replace agent if candidate solution is better
            replacement_agent = self.PClass(new_chromosome)
            if replacement_agent.fitness < agent.fitness:
                new_agents.append(replacement_agent)
            else:
                new_agents.append(agent)

        return new_agents

    def reflect_gene(self, gene: float) -> float:
        """Reflect gene.

        If the given gene gets out of boundaries (search space),
        the gene's value will be reflected by the exceeding
        amount.
        """
        if self.S[0] <= gene <= self.S[1]:
            return gene
        if gene < self.S[0]:
            return self.reflect_gene((self.S[0] * 2) - gene)
        else:
            return self.reflect_gene((self.S[1] * 2) - gene)

    def agents_fitness(self, agents: List[Individual]) -> float:
        """Return the mean fitness of a given set of agents."""
        fitness = [x.fitness for x in agents]
        return np.mean(fitness)
