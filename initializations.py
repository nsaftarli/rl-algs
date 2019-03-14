import numpy as np


def init_policy_esoft(epsilon, N_STATES, N_ACTIONS):
    pi = np.zeros((N_STATES, N_ACTIONS))

    for i in range(N_STATES):
        best_action = np.random.randint(0, N_ACTIONS)
        pi[i, :] = epsilon / 4
        pi[i, best_action] = 1 - epsilon + epsilon / 4

    return pi


def init_returns():
    pass


def init_mc(config):
    N_STATES = config['N_STATES']
    N_ACTIONS = config['N_ACTIONS']
    EPSILON = config['EPSILON']
    qSa = np.zeros((N_STATES, N_ACTIONS))
    pi = init_policy_esoft(EPSILON, N_STATES, N_ACTIONS)
    returns = np.zeros((N_STATES, N_ACTIONS))
    n_seen = np.zeros((N_STATES, N_ACTIONS))
    return qSa, returns, pi, n_seen


# def init_returns(states, actions):
#     returns = np.empty((states, actions), dtype=object)
#     for i in range(states):
#         for j in range(actions):
#             returns[i, j] = []

#     return returns
