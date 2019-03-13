import numpy as np
import time
from probs import *
from state_rewards import *
from utils import *
from action_select import *
from init_policy import *
from init_returns import *

GAMMA = 0.9
EPSILON = 0.1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
ACTIONS = [UP, RIGHT, DOWN, LEFT]
N_ACTIONS = 4
N_STATES = 100
PROBS = createStochastic(1.0, 0.0)


def main():
    qSa, returns, pi = initialize_mc()

    n_seen = np.zeros((100, 4))

    for k in range(10000):
        # a) generate an episode using pi
        episode = generate_episode(pi)
        while episode is None:
            episode = generate_episode(pi)
        # b) Evaluate action-value function
        qSa, returns, n_seen = evaluate_episode(episode, qSa, returns, k, n_seen)
        # c) improve policy
        pi = greedify_policy(pi, qSa)

        print(k)
        print_policy(np.argmax(pi, axis=1))

    # print_policy(np.argmax(pi, axis=1))
    print(returns[19, :])


def initialize_mc():
    qSa = np.zeros((N_STATES, N_ACTIONS))
    pi = init_policy(EPSILON)
    returns = np.zeros((N_STATES, N_ACTIONS))
    return qSa, returns, pi

def greedify_policy(pi, Q):
    best_actions = np.argmax(Q, axis=1)

    for state in range(N_STATES):
        optimal_action = best_actions[state]
        pi[state, :] = EPSILON / N_ACTIONS
        pi[state, optimal_action] += (1 - EPSILON)
    # for (s, _) in episode:
    #     optimal_action = best_actions[s]
    #     pi[s, :] = EPSILON / N_ACTIONS
    #     pi[s, optimal_action] += (1 - EPSILON)
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
def generate_episode(pi):
    # pi is a (100, 4) array. pi[x, a] specifies the probability of taking action a in state x
    episode = []
    steps = 0
    state = np.random.randint(0, N_STATES)
    action = np.random.choice(ACTIONS, p=pi[state])
    episode.append((state, action))
    while state != 9:
        steps += 1
        state = pick_next_state(state, action)
        action = np.random.choice(ACTIONS, p=pi[state])
        episode.append((state, action))
        
        # if state == 9:
        #     break
        if steps >= 1000:
            return episode
    episode.append((9, 0))
    return episode




def pick_next_state(state, action):
    next_state_probs = PROBS[state, action, :]
    next_state = np.random.choice(list(range(100)), p=next_state_probs)
    return next_state



if __name__ == '__main__':
    main()