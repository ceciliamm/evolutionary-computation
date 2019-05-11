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
            agent = self.PClass(chromosome)
            agent.df = self.F
            agents.append(agent)
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
                    new_y = ai + (agent.df * (bi - ci))
                    new_chromosome[j] = self.reflect_gene(new_y)

            # Replace agent if candidate solution is better
            replacement_agent = self.PClass(new_chromosome)
            replacement_agent.successful_mutations = agent.successful_mutations[:]
            replacement_agent.df = agent.df
            if replacement_agent.fitness < agent.fitness:
                replacement_agent.successful_mutations.append(1)
                new_agents.append(replacement_agent)
            else:
                agent.successful_mutations.append(0)
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


class CustomDE(DE):
    """Custom Differential Evolution.

    This custom implementation will add the initialize_agents weight
    as part of and individual's information. Although it will
    clearly not be used during fitness computation, it will be
    used during mutation, as mutated as well using the one-fifth
    success rule.
    """

    def mutate_agents(self, agents: List[Individual]) -> List[Individual]:
        """After mutations, alter the DF value based on the one-fifth rule."""
        # Retrieve base mutations
        new_agents = super().mutate_agents(agents)
        for agent in new_agents:
            h = self.D
            history = agent.successful_mutations[-h:]
            success_rate = sum(history) / len(history) if len(history) > 0 else 0
            if success_rate < 1/5:
                agent.df *= 0.82
            else:
                agent.df *= 1.22
        return new_agents
