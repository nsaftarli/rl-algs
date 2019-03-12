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
    states = []
    # Randomly pick a state to start in
    state = np.random.randint(0, 100)
    # While not at the terminal state
    while state != 9:
        states.append(state)
        # Pick the set of actions indexed by the state
        actions = policy[state]
        # Pick action greedily
        action = greedyActionSelect(EPSILON, actions)
        # Append all state/action pairs as tuples to the episode
        episode.append((state, action))
        # Get the next state according to current state, action, and board dynamics
        state = get_next_state(state, action, probs)
    print(states)

def get_next_state(state, action, probs):
    # Get the list of next states possible
    # next_states given by [target_state, self_state, [adjacent1, adjacent2]]
    next_states = possibleNextStates(state, action)
    distrib = []
    distrib_states = []
    # next_states[0] is the goal state by taking an action. So if the action
    # doesn't take the agent off the grid, append the probability of going to that state
    if next_states[0] is not None:
        distrib.append(probs[state, action, next_states[0]])
        distrib_states.append(next_states[0])

    # Append the probability of self-transitioning
    distrib.append(probs[state, action, state])
    distrib_states.append(state)
    print(distrib)
    print(distrib_states)
    # Go through adjacent state array and append probability of transitioning to them
    for i in next_states[2]:
        distrib.append(probs[state, action, i])
        distrib_states.append(i)

    # Sample a next state based on the probability distribution given.
    next_state = np.random.choice(distrib_states, p=distrib)
    return next_state


if __name__ == '__main__':
    monte_carlo_alg(0.75, 0.2)