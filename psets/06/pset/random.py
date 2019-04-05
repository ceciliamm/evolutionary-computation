"""Random module."""

import math
import random


def gen_normal(sigma=1):
    """Generate new random number.

    Return a normally-distributed value
    from an uniform distribution [0, 1)
    using the Box-Muller transform.
    """
    u1 = random.random()
    u2 = random.random()
    return sigma * (
        math.sqrt(-2 * math.log(u1)) *
        math.cos(2 * math.pi * u2)
    )
