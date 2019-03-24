"""Algorithms.

Module containing an implementation of the SGA
fitted to the problem in hand.
"""

from .individuals import Avatar

import random
import numpy as np
from typing import Dict, Tuple


class SGA:
    """Simple Genetic Algorithm implementation."""

    POP_SIZE = 100
    GENOME_LENGTH = 84

    PARENTS_COUNT = 6
    TOURNAMENT_GROUP_SIZE = 33
    WINNERS_PER_TOURNAMENT = 2

    fitness_over_time = [[], []]  # A[0] being the mean and A[1] the standard deviation

    def __init__(
            self,
            mutation_prob: float,
            role_model: Dict,
            max_trials: int = 10 ** 8,
            precision: float = 0.03
    ) -> None:
        """Set SGA role model and mutation probability."""
        rm_genome = Avatar.build_genome_from_attributes(role_model)

        self.role_model = Avatar(rm_genome, None)
        self.role_model.role_model = self.role_model

        self.mutation_prob = mutation_prob
        self.MAX_TRIALS = max_trials
        self.PRECISION = acceptable_solution_range

    def run(self):
        """Start SGA."""
        population = self.initialize()
        pop_fitness = [a.fitness for a in population]

        pop_mean, pop_std = np.mean(pop_fitness), np.std(pop_fitness)
        self.fitness_over_time[0].append(pop_mean)
        self.fitness_over_time[1].append(pop_std)

        trials = 0

        while trials < self.MAX_TRIALS and (1 - pop_mean) > self.PRECISION:
            parents = self.select_parents(population)
            offspring = self.recombine(parents, n=2)

        self.last_pop = population

    def initialize(self):
        """Start population with random candidates."""
        genomes = []
        for _ in range(self.POP_SIZE):
            genomes.append(bin(random.getrandbits(self.GENOME_LENGTH))[2:])

        population = []
        for genome in genomes:
            population.append(Avatar(genome, self.role_model))

        return population

    def select_parents(self, population: List(Avatar)) -> List(Tuple):
        """Return sets of mating partners."""
        mating_partners = []
        while len(mating_partners) < self.PARENTS_COUNT // 2:
            tournament = random.choices(population, self.TOURNAMENT_GROUP_SIZE)
            tournament.sort(key=lambda a: a.fitness, reversed=True)
            mating_partners.append(tuple(tournament[:self.WINNERS_PER_TOURNAMENT]))
        return mating_partners

    def recomibe(self, parents: Tuple(Avatar), crossover_points: int) -> List(Avatar):
        """Generate offspring by using n-point crossover."""
        return []