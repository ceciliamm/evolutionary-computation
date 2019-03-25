"""Algorithms.

Module containing an implementation of the SGA
fitted to the problem in hand.
"""

from .individuals import Avatar

import random
import numpy as np
from typing import Dict, List, Tuple


class SGA:
    """Simple Genetic Algorithm implementation."""

    POP_SIZE = 100
    GENOME_LENGTH = 84

    PARENTS_COUNT = 6
    TOURNAMENT_GROUP_SIZE = 33
    WINNERS_PER_TOURNAMENT = 2

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
        self.PRECISION = precision

        self.fitness_over_time = [[], []]  # A[0] being the mean and A[1] the standard deviation
        self.generations = 0

    def run(self):
        """Start SGA."""
        population = self.initialize()
        pop_mean, _ = self.population_fitness(population, update=True)

        while self.generations < self.MAX_TRIALS and (1 - pop_mean) > self.PRECISION:
            parents = self.select_parents(population)
            offspring = self.recombine(parents)
            self.mutate(offspring)

            population = self.select_new_population(population + offspring)

            pop_mean, _ = self.population_fitness(population, update=True)
            self.generations += 1

        self.last_pop = population

    def initialize(self):
        """Start population with random candidates."""
        genomes = []
        for _ in range(self.POP_SIZE):
            genomes.append(bin(random.getrandbits(self.GENOME_LENGTH))[2:].zfill(self.GENOME_LENGTH))

        population = []
        for genome in genomes:
            population.append(Avatar(genome, self.role_model))

        return population

    def select_parents(self, population: List[Avatar]) -> List[tuple]:
        """Return sets of mating partners."""
        mating_partners = []
        pop = population[:]
        while len(mating_partners) < self.PARENTS_COUNT // self.WINNERS_PER_TOURNAMENT:
            random.shuffle(pop)
            tournament = pop[:self.TOURNAMENT_GROUP_SIZE]
            tournament.sort(key=lambda a: a.fitness, reverse=True)
            mating_partners.append(tuple(tournament[:self.WINNERS_PER_TOURNAMENT]))
        return mating_partners

    def recombine(self, parents: Tuple[Avatar]) -> List[Avatar]:
        """Generate offspring by using 2-point crossover."""
        offspring = []
        for mating_group in parents:
            last_point = 0
            children = ['', '']
            p1, p2 = mating_group
            for i in range(3):
                new_point = random.randint(last_point + 1, self.GENOME_LENGTH - (4 - i)) if i < 2 else self.GENOME_LENGTH
                children[0] += p1.genome[last_point:new_point] if i % 2 == 0 else p2.genome[last_point:new_point]
                children[1] += p2.genome[last_point:new_point] if i % 2 == 0 else p1.genome[last_point:new_point]
                last_point = new_point
            offspring.append(Avatar(children[0], self.role_model))
            offspring.append(Avatar(children[1], self.role_model))
        return offspring

    def mutate(self, individuals: List[Avatar]) -> None:
        """Mutate individuals' genome genes based on the mutation probability."""
        for i in individuals:
            genome = ''
            for j in range(self.GENOME_LENGTH):
                gene = i.genome[j]
                genome += str(int(gene) ^ 1) if random.random() < self.mutation_prob else gene
            i.genome = genome

    def select_new_population(self, population: List[Avatar]) -> List[Avatar]:
        """Select new population of size POP_SIZE using FPS."""
        pop_mean, pop_std = self.population_fitness(population, update=False)

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

    def population_fitness(self, population: List[Avatar], update: bool = False) -> Tuple[float]:
        """Return population's mean fitness and standard deviation."""
        pop_fitness = [a.fitness for a in population]
        pop_mean, pop_std = np.mean(pop_fitness), np.std(pop_fitness)
        if update:
            self.fitness_over_time[0].append(pop_mean)
            self.fitness_over_time[1].append(pop_std)
        return pop_mean, pop_std