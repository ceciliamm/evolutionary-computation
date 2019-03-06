"""Problem set algorithms."""


def simulated_annealing(s0, t0, e, n, t):
    """Simulated Annealing Algorithm.
    
    Attributes
    ==========
    s0: Initial state
    t0: Initial temperature
    e: Energy function/Objective function
    n: Candidate generator function
    t: Annealing schedule function.

    Returns
    =======
    Global optimum state.
    """
    current_state = s0
    temperature = t0
    while temperature > 0:
        new_state = n(current_state)
        if e(new_state) < e(current_state):
            current_state = new_state
        else:
            diff = e(new_state) - e(current_state)
            p = np.exp(-diff/temperature)
            current_state = current_state if random.random() <= p else new_state
        temperature = t(temperature)
    return current_state