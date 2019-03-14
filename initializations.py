# Nariman Saftarli - 500615448
# Nimrod Vanir - 500699818

import numpy as np


def init_policy_esoft(epsilon, N_STATES, N_ACTIONS):
    pi = np.zeros((N_STATES, N_ACTIONS))

    for i in range(N_STATES):
        best_action = np.random.randint(0, N_ACTIONS)
        pi[i, :] = epsilon / 4
        pi[i, best_action] = 1 - epsilon + epsilon / 4

    return pi



def init_mc(config):
    N_STATES = config['N_STATES']
    N_ACTIONS = config['N_ACTIONS']
    EPSILON = config['EPSILON']
    qSa = np.zeros((N_STATES, N_ACTIONS))
    pi = init_policy_esoft(EPSILON, N_STATES, N_ACTIONS)
    returns = np.zeros((N_STATES, N_ACTIONS))
    n_seen = np.zeros((N_STATES, N_ACTIONS))
    return qSa, returns, pi, n_seen


