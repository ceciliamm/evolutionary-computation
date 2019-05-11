"""Individuals."""

import numpy as np  # type: ignore
from typing import List


class Individual:
    """Individual.

    An individual is composed of a fitness function
    and domain specific parameters.
    """

    def __init__(self, chromosome: List[float]) -> None:
        """Initialize individual."""
        self.chromosome = chromosome
        self.N = len(chromosome)
        self.df = 1.0  # type: float
        self.successful_mutations = []  # type: List[int]

    @property
    def fitness(self) -> float:
        """Must return a problem's specific evaluation."""
        raise NotImplementedError()

    def __str__(self) -> str:
        """Return chromosome with rounded values."""
        return str([round(x, 6) for x in self.chromosome])


class Sphere(Individual):
    """Sphere function."""

    @property
    def fitness(self) -> float:
        """Compute fitness."""
        return sum([x**2 for x in self.chromosome])


class Ackley(Individual):
    """Ackley function."""

    @property
    def fitness(self) -> float:
        """Compute fitness."""
        exp1 = np.exp(-0.2 * np.sqrt(
            (1 / self.N) *
            sum([x**2 for x in self.chromosome])
        ))
        exp2 = np.exp(
            (1 / self.N) *
            sum([np.cos(2 * np.pi * x) for x in self.chromosome])
        )
        return (-20 * exp1) - exp2 + 20 + np.exp(1)


class Griewangk(Individual):
    """Griewangk function."""

    @property
    def fitness(self) -> float:
        """Compute fitness."""
        s, p = 0.0, 1.0
        for i in range(self.N):
            xi = self.chromosome[i]
            s += xi ** 2
            p *= np.cos(xi / np.sqrt(i + 1))
        return 1 + ((1 / 4000) * s) - p
