import numpy as np
import time
from probs import *
from state_rewards import *
from utils import *
from action_select import *
from init_policy import *
from init_returns import *

ALPHA = 0.1
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
    qSa = np.zeros((N_STATES, N_ACTIONS))
    pi = init_policy(EPSILON)
    rewards = np.full((N_STATES,), -1)
    rewards[9] = 100

    for k in range(10000):
        # initialize S
        print(k)
        episode = []
        start_state = np.random.randint(0, N_STATES)
        state = start_state

        # Repeat (for each step of episode until termination):
        nSteps = 0
        while True:
            nSteps += 1
            # Choose A from S using policy derived from Q
            action = derive_policy(Q=qSa, s=state, epsilon=EPSILON)
            # Take action A, observe R, S'
            episode.append((state, action))
            next_state = pick_next_state(state, action)
            reward = rewards[next_state]

            # Update Q(S, A)
            qSa[state, action] += ALPHA \
                * (reward + GAMMA * np.amax(qSa[next_state, action]) - qSa[state, action])

            # S = S'
            state = next_state

            if state == 9:
                break

        print(nSteps)
        policy = np.argmax(qSa, axis=1)
        print_policy(policy)

def generate_episode():
    states = list(range(N_STATES))
    policy = np.zeros((N_STATES,))
    # for i in range(N_STATES):
        
def pick_next_state(state, action):
    next_state_probs = PROBS[state, action, :]
    next_state = np.random.choice(list(range(100)), p=next_state_probs)
    return next_state

if __name__ == '__main__':
    main()