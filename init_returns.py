import numpy as np

def init_returns(states, actions):
    returns = np.empty((states, actions), dtype=object)
    for i in range(states):
        for j in range(actions):
            returns[i, j] = []

    return returns