import numpy as np
from probs import *
from state_rewards import *
from action_select import *
from init_policy import *

GAMMA = 0.9
EPSILON = 0.1
UP = 0
RIGHT = 1
DOWN = 2
LEFT  = 3
def monte_carlo_alg(p1, p2):
    # Transition table is invisible to agent, but controls the dynamics of the grid
    transition_table = createStochastic(p1, p2)
    # Rewards are -1 for all but the final state which is +100
    reward_table = state_rewards()
    # Action value function starts as 0 for all action-state pairs
    qSa = np.zeros((100, 4))
    # Policy is randomly initialized to epsilon-soft and is (100, 4)
    pi_sa = init_policy(epsilon=EPSILON)

    generate_episode(pi_sa, transition_table, reward_table)


def generate_episode(policy, probs, rewards):
    episode = []
    state = np.random.randint(0, 100)
    while state != 9:
        actions = policy[state]
        action = greedyActionSelect(EPSILON, actions)
        episode.append((state, action))
        state = get_next_state(state, action, probs)
        print(state)


def get_next_state(state, action, probs):
    next_states = possibleNextStates(state, action)
    roll = np.random.rand()
    if roll <= probs[state, action, next_states[0]]:
        if next_states[0] == -1:
            print("WTF")
            print(probs[state, action, next_states[0]])
        return next_states[0]
    elif roll > probs[state, action, next_states[0]] and\
         roll <= probs[state, action, state]:
         return next_states[1]
    else:
        adj = next_states[2]
        if len(adj) == 1:
            return adj[0]
        else:
            return adj[np.random.randint(0, 2)]









if __name__ == '__main__':
    monte_carlo_alg(1, 0)