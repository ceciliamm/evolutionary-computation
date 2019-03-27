"""Individuals.

Module containing the Individual class.
"""

from typing import Dict


class Individual:
    """Individual.

    An entity containing the information of an individual
    ass well as it fitness function.
    """

    def __init__(self, chromosome: str) -> None:
        """Initialize with the given chromosome."""
        self.chromosome = chromosome

    @property
    def fitness(self) -> float:
        """Return fitness defined the amount of 1s it have on its chromosome.

        Fitness is mapped to range [0, 1] by dividing over
        the amount of bits.
        """
        total = sum(int(c) for c in self.chromosome)
        return total / len(self.chromosome)

    def __str__(self) -> str:
        """Return individual's chromosome."""
        return '{:.3f}: {}'.format(self.fitness, self.chromosome)

    def __repr__(self) -> str:
        """Return str representation."""
        return str(self)

