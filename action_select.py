# Nariman Saftarli - 500615448
# Nimrod Vanir - 500699818

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


def derive_policy(Q, s, epsilon):
    actions = Q[s]
    action = greedyActionSelect(epsilon=epsilon, actions=actions)
    return action
