import numpy as np

def greedyActionSelect(epsilon, actions):
    roll = np.random.rand()

    if roll > epsilon:
        return np.argmax(actions)
    else:
        return np.random.randint(0, len(actions))

def epsilon_soft_action(eps, actions):
    prob_actions = np.full((4,), eps/len(actions))
    prob_actions[np.argmax(actions)] = 1 - eps + eps/len(actions)
    return prob_actions