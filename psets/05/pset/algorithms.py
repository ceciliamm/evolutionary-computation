"""Algorithms.

Module containing an implementation of the SGA
fitted to the problem in hand.
"""

from .individuals import Individual

import random
import numpy as np
from typing import Dict, List, Tuple


class SGA:
    """Simple Genetic Algorithm (SGA) implementation."""

    WINNERS_PER_TOURNAMENT = 2
    PARENTS_COUNT = 4
    TOURNAMENT_GROUP_SIZE = 7

    def __init__(
            self,
            mutation_prob: float = 0.01,
            combination_prob: float = 0.7,
            max_trials: int = 100,
            precision: float = 0.01,
            population_size: int = 20,
            chromosome_length: int = 30
    ) -> None:
        """Set SGA parameters."""

        self.MAX_TRIALS = max_trials
        self.PRECISION = precision
        self.POP_SIZE = population_size
        self.CHROMOSOME_LENGTH = chromosome_length

        self.mutation_prob = mutation_prob
        self.combination_prob = combination_prob

        self.fitness_over_time = [[], [], []]  # A[0] being the mean, A[1] the standard deviation, A[2] best
        self.generations = 0

    def run(self):
        """Start SGA."""
        population = self.initialize()
        pop_mean = self.population_fitness(population, update=True)[0]

        while self.generations < self.MAX_TRIALS and (1 - pop_mean) > self.PRECISION:
            parents = self.select_parents(population)
            offspring = self.recombine(parents)
            self.mutate(offspring)

            population = self.select_new_population(population + offspring)

            pop_mean = self.population_fitness(population, update=True)[0]
            self.generations += 1

        self.last_pop = population

    def initialize(self) -> List[Individual]:
        """Start population with random candidates."""
        population = []
        for _ in range(self.POP_SIZE):
            population.append(Individual(
                bin(random.getrandbits(self.CHROMOSOME_LENGTH))[2:].zfill(self.CHROMOSOME_LENGTH)
            ))

        return population

    def select_parents(self, population: List[Individual]) -> List[tuple]:
        """Return sets of mating partners."""
        mating_partners = []
        pop = population[:]
        while len(mating_partners) < self.PARENTS_COUNT // self.WINNERS_PER_TOURNAMENT:
            random.shuffle(pop)
            tournament = pop[:self.TOURNAMENT_GROUP_SIZE]
            tournament.sort(key=lambda a: a.fitness, reverse=True)
            mating_partners.append(tuple(tournament[:self.WINNERS_PER_TOURNAMENT]))
        return mating_partners

    def recombine(self, parents: Tuple[Individual]) -> List[Individual]:
        """Generate offspring by using 1-point crossover."""
        offspring = []
        for mating_group in parents:
            p1, p2 = mating_group
            if random.random() < self.combination_prob:
                c = random.randint(1, self.CHROMOSOME_LENGTH - 2)  # -2 because lists are 0-indexed
                offspring.append(Individual(p1.chromosome[:c] + p2.chromosome[c:]))
                offspring.append(Individual(p2.chromosome[:c] + p1.chromosome[c:]))
                
            else:
                offspring.append(p1)
                offspring.append(p2)
        return offspring

    def mutate(self, individuals: List[Individual]) -> None:
        """Mutate individuals' chromosome alleles based on the mutation probability."""
        for i in individuals:
            chromosome = ''
            for j in range(self.CHROMOSOME_LENGTH):
                allele = i.chromosome[j]
                chromosome += str(int(allele) ^ 1) if random.random() < self.mutation_prob else allele
            i.chromosome = chromosome

    def select_new_population(self, population: List[Individual]) -> List[Individual]:
        """Select new population of size POP_SIZE using FPS."""
        pop_mean, pop_std, _ = self.population_fitness(population, update=False)

        # Assign new temporal fitness to each individual
        for i in population:
            i.tmp_fitness = max(i.fitness - (pop_mean - (2 * pop_std)), 0)

        pop_total = sum(i.tmp_fitness for i in population)
        # Assign FPS probability to each individual
        for i in population:
            i.fps_prob = i.tmp_fitness / pop_total

        population.sort(key=lambda i: i.fps_prob)

        new_population = []
        while len(new_population) < self.POP_SIZE:
            state = random.random()
            for i in population:
                state -= i.fps_prob
                if state < 0:
                    new_population.append(i)
                    break
            new_population.append(population[-1])  # Round error happend

        return new_population

    def population_fitness(self, population: List[Individual], update: bool = False) -> Tuple[float]:
        """Return population's mean fitness and best."""
        pop_fitness = [a.fitness for a in population]
        pop_mean, pop_std =  np.mean(pop_fitness), np.std(pop_fitness)
        best = max(pop_fitness)
        if update:
            self.fitness_over_time[0].append(pop_mean)
            self.fitness_over_time[1].append(pop_std)
            self.fitness_over_time[2].append(best)
        return pop_mean, pop_std, best