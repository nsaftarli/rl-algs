import numpy as np
import time
from probs import *
from utils import *
from action_select import *
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
    ALPHA = alpha
    GAMMA = gamma
    EPSILON = epsilon
    config['ENV'] = ENV
    config['ALPHA'] = ALPHA
    config['GAMMA'] = GAMMA
    config['EPSILON'] = EPSILON

    qSa = np.zeros((N_STATES, N_ACTIONS))
    pi = init_policy_esoft(EPSILON, N_STATES, N_ACTIONS)
    rewards = np.full((N_STATES,), -1)
    rewards[9] = 100

    for k in range(iterations):
        print(k)
        # initialize S
        start_state = np.random.randint(0, N_STATES)
        state = start_state

        # Choose A from S using policy derived from Q
        action = derive_policy(Q=qSa, s=state, epsilon=EPSILON)

        # Repeat (for each step of episode until termination):
        nSteps = 0
        while True:
            nSteps += 1

            # Take action A, observe R, S'
            next_state = ENV.pick_next_state(state, action)
            reward = ENV.get_reward(next_state)

            # Choose A' from S', using policy derived from Q
            next_action = derive_policy(Q=qSa, s=next_state, epsilon=EPSILON)

            # Update Q(S, A)
            qSa[state, action] += ALPHA \
                * (reward + GAMMA * qSa[next_state, next_action] - qSa[state, action])

            # S = S', A = A'
            state = next_state
            action = next_action
            if state == 9:
                break

        policy = np.argmax(qSa, axis=1)
        print(nSteps)
        print_policy(policy)
    return policy

if __name__ == '__main__':
    main()