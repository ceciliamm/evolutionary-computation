"""Algorithms.

This module contain the (1+1)-ES implementation.
"""

from .individuals import Sphere
from .random import gen_normal

import math
import numpy as np
import random


class ES1P1:
    "(1+1) Evolution Strategy algorithm."

    def __init__(
            self,
            max_trials: int,
            precision: float,
            parent: Sphere,
            fifth_rule_enabled: bool = False,
    ) -> None:
        """Set algorithm parameters."""
        self.MAX_TRIALS = max_trials
        self.PRECISION = precision
        self.WITH_FIFTH_RULE = fifth_rule_enabled

        self.parent = parent

        self.generations = 0
        self.successful_mutations = []
        self.fitness_over_time = []

    def run(self) -> None:
        """Run evolution strategy."""
        while self.generations < self.MAX_TRIALS and self.parent.fitness > self.PRECISION:
            child = self.mutate(self.parent)

            if child.fitness < self.parent.fitness:
                self.parent = child
                self.successful_mutations.append(1)
            else:
                self.update_std(self.parent)
                self.successful_mutations.append(0)

            self.generations += 1
            self.fitness_over_time.append(self.parent.fitness)

    def mutate(self, parent: Sphere) -> Sphere:
        """Mutate parent."""
        child = Sphere(parent.chromosome[:])
        child.std = parent.std
        d = len(child.chromosome)
        for i in range(d):
            child.chromosome[i] += gen_normal(child.std)
            if child.chromosome[i] < -100:
                child.chromosome[i] = -100
            elif child.chromosome[i] > 100:
                child.chromosome[i] = 100
        return child

    def update_std(self, individual: Sphere) -> None:
        """Update individual STD bases on the 1/5 rule."""
        if self.WITH_FIFTH_RULE:
            h = len(individual.chromosome)
            history = self.successful_mutations[-h:]
            success_rate = sum(history) / len(history) if len(history) > 0 else 0

            if success_rate < 1/5:
                individual.std *= 0.82
            elif success_rate > 1/5:
                individual.std *= 1.22


class ESMuPLambda:
    """(μ+λ) Evolution strategy algorithm."""

    def __init__(self, max_trials, precision, problem_class, dimensions, mu, lam, search_space):
        """Set up algorithm parameters."""
        self.MAX_TRIALS = max_trials
        self.PRECISION = precision

        self.ProblemClass = problem_class
        self.dimensions = dimensions
        self.search_space = search_space

        self.MU = mu
        self.LAMBDA = lam

        self.population = []
        self.generations = 0
        self.best_over_time = []

    def run(self):
        """Run algorithm"""
        self.population = self.initialize()
        pop_fitness = self.population_fitness(self.population)
        while self.generations < self.MAX_TRIALS and pop_fitness > self.PRECISION:
            offspring = self.get_offspring(self.population)
            union = self.population + offspring
            self.population = sorted(union, key=lambda x: x.fitness)[:self.MU]
            self.best_over_time.append(self.population[0])
            pop_fitness = self.population_fitness(self.population)
            self.generations += 1

    def initialize(self):
        """Initialize parents population."""
        population = [None] * self.MU
        for i in range(self.MU):
            individual = self.ProblemClass(
                [random.randint(-30, 30) for _ in range(self.dimensions)]
            )
            individual.std = 1.0
            population[i] = individual
        return population

    def get_offspring(self, population):
        """Return a population of LAMBDA children derived from population."""
        offspring = []
        for _ in range(self.LAMBDA):
            # If LAMBDA > MU, after MU children, parent will be randomly selected from population
            parent = random.choice(population) if _ >= self.MU else self.population[_]

            child = self.ProblemClass(parent.chromosome)
            child.std = parent.std

            self.mutate(child)
            offspring.append(child)

        return offspring

    def mutate(self, individual):
        """Mutate individual."""
        individual.chromosome = self.mutate_chromosome(individual)
        individual.std = self.mutate_std(individual)

    def mutate_chromosome(self, individual):
        """Mutate individual's chromosome."""
        chromosome = individual.chromosome[:]
        for i in range(len(chromosome)):
            chromosome[i] += gen_normal(individual.std)
            chromosome[i] = self.search_space[0] if chromosome[i] < self.search_space[0] else chromosome[i]
            chromosome[i] = self.search_space[1] if chromosome[i] > self.search_space[1] else chromosome[i]
        return chromosome

    def mutate_std(self, individual):
        """Mutate individual's std."""
        tau_0 = 1 / math.sqrt(2 * self.dimensions)
        tau = 1 / math.sqrt(2 * math.sqrt(self.dimensions))
        std = individual.std
        std *= math.exp(tau_0*gen_normal() + tau*gen_normal())
        return std


    def population_fitness(self, population):
        """Return population's mean fitness."""
        pop_fitness = [i.fitness for i in population]
        return np.mean(pop_fitness)