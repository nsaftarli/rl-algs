import numpy as np

def state_rewards():
    rew = np.full((100), -1)
    rew[9] = 100
    return rew