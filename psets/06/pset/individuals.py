"""Individuals.

Contain the individuals representation for each problem.
"""

from typing import List


class Sphere:
    """Individual related to the sphere problem."""

    def __init__(self, chromosome: List[int]) -> None:
        """Set individual's initial state."""
        self.chromosome = chromosome
        self.std = 1.0

    @property
    def fitness(self):
        return sum([x**2 for x in self.chromosome])

    def __str__(self):
        return ', '.join(['{:.4f}'.format(x) for x in self.chromosome])