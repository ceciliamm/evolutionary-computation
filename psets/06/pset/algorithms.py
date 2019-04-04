"""Algorithms.

This module contain the (1+1)-ES implementation.
"""

from .individuals import Sphere
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
        precision = self.parent.fitness
        while self.generations < self.MAX_TRIALS and precision > self.PRECISION:
            child = self.mutate(self.parent)

            if child.fitness < self.parent.fitness:
                precision = self.parent.fitness - child.fitness
                self.parent = child
                self.successful_mutations.append(1)
            else:
                self.successful_mutations.append(0)

            self.generations += 1
            self.fitness_over_time.append(self.parent.fitness)

    def mutate(self, parent: Sphere) -> Sphere:
        """Mutate parent."""
        child = Sphere(parent.chromosome[:])
        self.update_std(child)
        d = len(child.chromosome)
        for i in range(d):
            child.chromosome[i] += random.gauss(0, child.std)
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
