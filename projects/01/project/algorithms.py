"""Algorithms."""


from typing import List, Tuple

from .individuals import AB, SearchSpace, Chromosome


import datetime
import numpy as np
import os
import random


# Custom types
Population = List[AB]


class ESMuPLambda:
    """(μ+λ) Evolution strategy algorithm."""

    def __init__(
            self,
            search_space: SearchSpace,
            n: int,
            y: int, x: int,
            max_trials: int,
            precision: float,
            mu: int,
            lam: int,
            store_results: bool = False,
            output_dir: str = None
    ) -> None:
        """Set up algorithm parameters."""
        self.MAX_TRIALS = max_trials
        self.PRECISION = precision

        self.search_space = search_space
        self.n = n
        self.y, self.x = y, x

        self.MU = mu
        self.LAMBDA = lam

        self.generations = 0
        self.population = []  # type: Population
        self.results = []  # type: Tuple(float, List[Population])

        self.store_results = store_results
        self.output_dir = output_dir if output_dir else self.create_output_dir()

    def run(self):
        """Run algorithm."""
        self.population = self.initialize()
        pop_fitness = self.population_fitness(self.population)

        precision = pop_fitness

        while self.generations < self.MAX_TRIALS and precision > self.PRECISION:
            # Off-algorithm features
            if self.store_results:
                self.store_population(self.population, pop_fitness, str(self.generations))
            self.results.append((pop_fitness, self.population))

            offspring = self.get_offspring(self.population)
            union = self.population + offspring
            self.population = sorted(union, key=lambda x: x.fitness)[:self.MU]
            new_pop_fitness = self.population_fitness(self.population)
            precision = abs(pop_fitness - new_pop_fitness)
            pop_fitness = new_pop_fitness
            self.generations += 1

    def initialize(self) -> Population:
        """Initialize parents population."""
        population = []  # type: Population
        for _ in range(self.MU):
            individual = AB(self.n, self.y, self.x, 1.0, self.search_space)
            individual.initialize()
            population.append(individual)
        return population

    def get_offspring(self, population: Population) -> Population:
        """Return a population of LAMBDA children derived from population."""
        offspring = []  # type: Population
        for _ in range(self.LAMBDA):
            # If LAMBDA > MU, after MU children, parent will be randomly selected from population
            parent = random.choice(population) if _ >= self.MU else self.population[_]

            child = AB(
                parent.n,
                parent.y, parent.x,
                parent.std,
                parent.search_space,
                parent.chromosome
            )

            self.mutate(child)
            offspring.append(child)

        return offspring

    def mutate(self, individual: AB) -> None:
        """Mutate given individual."""
        individual.chromosome = self.mutate_chromosome(individual)
        individual.std = self.mutate_std(individual)

    def mutate_chromosome(self, individual: AB) -> Chromosome:
        """Mutate individual's chromosome."""
        chromosome = individual.chromosome[:]
        for i in range(len(chromosome)):
            chromosome[i] += random.gauss(0, individual.std)
            chromosome[i] = self.search_space[0] if chromosome[i] < self.search_space[0] else chromosome[i]
            chromosome[i] = self.search_space[1] - self.PRECISION if chromosome[i] > self.search_space[1] else chromosome[i]
        return chromosome

    def mutate_std(self, individual):
        """Mutate individual's std."""
        tau_0 = 1 / np.sqrt(2 * self.n)
        tau = 1 / np.sqrt(2 * np.sqrt(self.n))
        std = individual.std
        std *= np.exp(tau_0 * random.gauss(0, 1) + tau * random.gauss(0, 1))
        return std

    def population_fitness(self, population: Population) -> float:
        """Return population's mean fitness."""
        pop_fitness = [i.fitness for i in population]
        return np.mean(pop_fitness)

    def create_output_dir(self) -> str:
        """Create output directory.

        If user wants to store the results over time, this method create
        a new directory named after the current datetime and return its
        name.
        """
        if not self.store_results:
            return ''
        dirname = 'results/' + str(datetime.datetime.now()).replace(' ', '-')
        os.makedirs(dirname)
        return dirname

    def store_population(self, population: Population, pop_fitness: float, generation: str) -> None:
        """Store results of given population in a generation file."""
        gen_str = generation.zfill(int(np.log10(self.MAX_TRIALS)))
        filename = '{}/{}.results'.format(self.output_dir, gen_str)
        content = '{n}, {y}, {x}\n'.format(n=self.n, y=self.y, x=self.x)
        content += '{}\n'.format(pop_fitness)
        for individual in population:
            content += ', '.join(['{0:.{1}f}'.format(x, 10) for x in individual.chromosome]) + '\n'
        f = open(filename, 'w')
        f.write(content)
        f.close()
