"""Problem set algorithms."""

import numpy as np
import random


def simulated_annealing(s0, e, n, t, max_iters):
    """Simulated Annealing Algorithm.

    Attributes
    ==========
    s0: Initial state
    e: Energy function/Objective function
    n: Candidate generator function
    t: Annealing schedule function.

    Returns
    =======
    Global optimum state.
    """
    current_state = s0
    for i in range(max_iters):
        temperature = t(i/max_iters)
        new_state = n(current_state)
        if e(new_state) < e(current_state):
            current_state = new_state
        else:
            diff = e(new_state) - e(current_state)
            p = np.exp(diff/(temperature))
            current_state = current_state if random.random() <= p else new_state
    return current_state
