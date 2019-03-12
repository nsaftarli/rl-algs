import numpy as np

def greedyActionSelect(epsilon, actions):
    roll = np.random.rand()

    if roll > epsilon:
        return np.argmax(actions)
    else:
        return np.random.randint(0, len(actions))