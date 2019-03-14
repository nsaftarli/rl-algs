import numpy as np
import time
from probs import *
# from state_rewards import *
from utils import *
# from action_select import *
# from init_policy import *
# from init_returns import *
from initializations import *


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
ACTIONS = [UP, RIGHT, DOWN, LEFT]
N_ACTIONS = 4
N_STATES = 100

config = {}
config['UP'] = UP
config['RIGHT'] = RIGHT
config['DOWN'] = DOWN
config['LEFT'] = LEFT
config['ACTIONS'] = ACTIONS
config['N_ACTIONS'] = N_ACTIONS
config['N_STATES'] = N_STATES


def main(iterations, p1, p2, alpha, gamma, epsilon):
    ENV = Environment(p1, p2)
    GAMMA = gamma
    EPSILON = epsilon
    config['ENV'] = ENV
    config['GAMMA'] = GAMMA
    config['EPSILON'] = EPSILON
    qSa, returns, pi, n_seen = init_mc(config)

    for k in range(iterations):
        # a) generate an episode using pi
        episode = generate_episode(pi, config)
        # b) Evaluate action-value function
        qSa, returns, n_seen = evaluate_episode(episode, qSa, returns, k, n_seen)
        # c) improve policy
        pi = greedify_policy(pi, qSa)


    # return np.argmax(pi, axis=1)
    policy = np.argmax(pi, axis=1)
    print_policy(policy)
    avg_val = np.mean(np.amax(qSa, axis=1))
    return pi, avg_val

def greedify_policy(pi, Q):
    best_actions = np.argmax(Q, axis=1)

    for state in range(N_STATES):
        optimal_action = best_actions[state]
        pi[state, :] = config['EPSILON'] / N_ACTIONS
        pi[state, optimal_action] += (1 - config['EPSILON'])

    return pi


def evaluate_episode(episode, qSa, returns, k, n_seen):
    unique_s_a_pairs = set()
    len_episode = len(episode)
    for i, (s, a) in enumerate(episode):
        if (s, a) not in unique_s_a_pairs:
            unique_s_a_pairs.add((s, a))
            n_seen[s, a] += 1
            if s != 9:
                G = (len_episode - i) * -1
            else:
                G = 100
            returns[s, a] = returns[s, a] + ((1/n_seen[s, a]) * (G - returns[s, a]))
            qSa[s, a] = returns[s, a]
    return qSa, returns, n_seen


# a) generate an episode using pi
def generate_episode(pi, config):
    # pi is a (100, 4) array. pi[x, a] specifies the probability of taking action a in state x
    episode = []
    ENV = config['ENV']
    steps = 0
    state = np.random.randint(0, N_STATES)
    action = np.random.choice(ACTIONS, p=pi[state])
    episode.append((state, action))
    while state != 9:
        steps += 1
        state = ENV.pick_next_state(state, action)
        action = np.random.choice(ACTIONS, p=pi[state])
        episode.append((state, action))

        if steps >= 100:
            return episode
    episode.append((9, 0))
    return episode


if __name__ == '__main__':
    main()
