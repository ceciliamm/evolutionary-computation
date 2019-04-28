"""Individuals."""

from typing import List, Tuple

import math
import numpy as np
import random


# Custom types
Chromosome = List[float]
SearchSpace = Tuple[float, float]


class AB:
    """Approximated Brachistochrone.

    Approximated brachistochrones are the individuals that going to be evolving
    during the main algorithm execution. Each AB is represented as a set of
    n-1 vertical coordinates representing the overall curve, where n is the
    number of evenly distributed "slots" between the starting point and the
    final point.
    """

    def __init__(
            self,
            n: int,
            y: float,
            x: float,
            std: float,
            search_space: SearchSpace,
            chromosome: Chromosome = None
    ) -> None:
        """AB initialization."""
        self.n = n
        self.y = y
        self.x = x

        self.std = std

        self.search_space = search_space
        self.chromosome = chromosome if chromosome else self.initialize()

    def initialize(self) -> Chromosome:
        """Return a real-valued random vector constrained by the search space."""
        chromosome = []
        for _ in range(self.n - 1):
            value = self.y
            while value >= self.y:
                value = random.randint(*self.search_space)
            chromosome.append(value)
        return chromosome

    @property
    def fitness(self) -> float:
        """Compute AB's fitness based on Borschbach-Dreckmann."""
        bin_width = self.x / self.n
        total_sum = 0.0
        for i in range(self.n - 2):
            cur_y, next_y = self.chromosome[i], self.chromosome[i + 1]
            total_sum += (
                math.sqrt((bin_width**2) + (next_y - cur_y)**2) /
                (math.sqrt(self.y - cur_y) + math.sqrt(self.y - next_y))
            )
        return math.sqrt(2 / 9.81) * total_sum
