import numpy as np
import time
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

actionNtoS = ['up', 'right', 'down', 'left']

def monte_carlo_alg(p1, p2):
    # Transition table is invisible to agent, but controls the dynamics of the grid
    transition_table = createStochastic(p1, p2)
    reward_table = state_rewards()
    # Action value function starts as 0 for all action-state pairs
    qSa = np.zeros((100, 4))
    # Policy is randomly initialized to epsilon-soft and is (100, 4)
    pi_sa = init_policy(epsilon=EPSILON)

    returns = np.zeros((100, 4))
    returnsCount = np.zeros((100, 4))

    returns = {}
    for s in range(100):
        for a in range(4):
            returns[(s, a)] = []

    for q in range(500):
        print("Iteration: ", str(q))
        episode = generate_episode(pi_sa, transition_table, reward_table)
        while episode is None:
            pi_sa = init_policy(epsilon=EPSILON)
            episode = generate_episode(pi_sa, transition_table, reward_table)

        stateActionSet = set()

        for i, (s, a) in enumerate(episode):
            if (s, a) not in stateActionSet:
                stateActionSet.add((s, a))

                returnsCount[s, a] += 1

                if not s == 9:
                    returns[(s, a)].append(-1 * i)
                else:
                    returns[(s, a)].append(100)

                qSa[s, a] = np.average(returns[(s, a)])

        stateSet = set()

        for (s, a) in episode:
            if (s) not in stateSet:
                stateSet.add((s))
                a_opt = np.argmax(qSa[s, :])
                for a in range(4):
                    if a == a_opt:
                        pi_sa[s, a] = 1 - EPSILON + EPSILON/4
                    else:
                        pi_sa[s, a] = EPSILON/4

        # print(pi_sa)
        # print(len(episode))

    policy_maxes = np.argmax(pi_sa, axis=1)
    # print([actionNtoS[j] for j in policy_words])
    # print(policy_words)
    # for i, act in enumerate(policy_words):
        # print("Cell: ", str(i), " Action: ", actionNtoS[act])

    print_policy(policy_maxes)


def generate_episode(policy, probs, rewards):
    episode = []
    states = []
    # Randomly pick a state to start in
    state = np.random.randint(0, 100)
    steps = 0
    # While not at the terminal state
    while state != 9:
        steps += 1
        states.append(state)
        # Pick the set of actions indexed by the state
        actions = policy[state]
        # Pick action greedily
        action = greedyActionSelect(EPSILON, actions)
        # Append all state/action pairs as tuples to the episode
        episode.append((state, action))
        # Get the next state according to current state, action, and board dynamics
        state = get_next_state(state, action, probs)

        if steps >= 500:
            # print("RESTARTING")
            # time.sleep(0.1)
            return None

    if state == 9:
        action = np.random.randint(0, 4)
    episode.append((state, action))
    states.append(state)
    # print("EPISODE LENGTH IS: ", len(episode))
    # print(states)
    # print("STEPS TAKEN: ", steps)
    return episode

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
    # print(distrib)
    # print(distrib_states)
    # Go through adjacent state array and append probability of transitioning to them
    for i in next_states[2]:
        distrib.append(probs[state, action, i])
        distrib_states.append(i)

    # Sample a next state based on the probability distribution given.
    # print(distrib)
    next_state = np.random.choice(distrib_states, p=distrib)
    return next_state


if __name__ == '__main__':
    monte_carlo_alg(1, 0)
