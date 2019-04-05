"""Individuals.

Contain the individuals representation for each problem.
"""

from typing import List

import math


class Individual:
    """Individual abstract class."""

    def __init__(self, chromosome: List[int]) -> None:
        """Set individual's initial state."""
        self.chromosome = chromosome
        self.std = 1.0

    def __str__(self):
        return ', '.join(['{:.4f}'.format(x) for x in self.chromosome])


class Sphere(Individual):
    """Individual related to the sphere problem."""

    @property
    def fitness(self):
        return sum([x**2 for x in self.chromosome])


class Ackley(Individual):
    """Individual related to the Ackley function."""

    @property
    def fitness(self):
        d = len(self.chromosome)
        sum_1 = sum([x** 2 for x in self.chromosome])
        sum_2 = sum([math.cos(2 * math.pi * x) for x in self.chromosome])
        return (
            (-20 * math.exp(-0.2 * math.sqrt( sum_1 / d ))) -
            math.exp(sum_2 / d) +
            20 + math.exp(1)
        )
