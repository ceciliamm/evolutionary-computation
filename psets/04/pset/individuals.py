"""Individuals.

Module containing the Avatar class.
"""

from typing import Dict
from .utils import int_to_gray, gray_to_int


class Avatar:
    """Avatar.

    An avatar hold information about its genome,
    its fitness compared to a desired avatar, and
    functions related to encoding and decoding.
    """

    def __init__(self, genome: str, role_model: "Avatar") -> None:
        """Initialize with basic avatar attributes."""
        self.genome = genome
        self.role_model = role_model

    @property
    def fitness(self) -> int:
        """Return fitness compared to role model.

        Fitness is defined as the Hamming distance between
        avatar's genome and role model's genome mapped to [0, 1].
        """
        if len(self.genome) != len(self.role_model.genome):
            raise ValueError("Undefined for sequences of unequal length")
        h = sum(a != b for a, b in zip(self.genome, self.role_model.genome))
        return 1 - (h / 84)

    @staticmethod
    def build_genome_from_attributes(attr: Dict) -> str:
        """Given an attributes dictionary, compute genome's binary string."""
        genome = ''

        for color_feature in [attr['hair_color'], attr['eyes_color'], attr['skin_color']]:
            for color in color_feature:  # Expecting color future to be (R, G, B)
                genome += int_to_gray(color)

        genome += int_to_gray(attr['height'], l=8)
        genome += int_to_gray(attr['body_type'], l=4)

        return genome

    @property
    def attributes(self) -> Dict:
        """Return attributes from genome, A.K.A decoding."""
        attr = {'height': None, 'body_type': None, 'hair_color': None, 'eyes_color': None, 'skin_color': None}
        colors = []
        for i in range(3):
            color_feature = self.genome[(i * 24): (i*24) + 24]
            color = [None, None, None]
            for i in range(3):
                color[i] = gray_to_int(color_feature[i * 8: (i * 8) + 8])
            colors.append(tuple(color))
        attr['hair_color'], attr['eyes_color'], attr['skin_color'] = colors[0], colors[1], colors[2]
        attr['height'] = gray_to_int(self.genome[72: 80])
        attr['body_type'] = gray_to_int(self.genome[80: 84])
        return attr

    def __str__(self) -> str:
        """Return avatar's genome."""
        return self.genome

