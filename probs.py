import numpy as np
from utils import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Environment():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.probs = createStochastic(self.p1, self.p2)
        self.rewards = np.full((100,), -1)
        self.rewards[9] = 100

    def get_transitions(self):
        return self.probs

    def get_reward(self, state):
        return self.rewards[state]

    def pick_next_state(self, state, action):
        next_state_probs = self.probs[state, action]
        next_state = np.random.choice(list(range(100)), p=next_state_probs)
        return next_state


# For modeling the unknown transition probabilities
def createStochastic(p1, p2):

    states = list(range(0, 100))

    # Transition probabilities. Suppose grid of s a s'
    probs = np.zeros((100, 4, 100))
    for state in states:
        for direction in range(4):
            possNextStates = possibleNextStates(state, direction)

            moveGoal = possNextStates[0]
            moveSelf = possNextStates[1]
            moveAdjacent = possNextStates[2]
            nAdjacent = len(moveAdjacent)
            p3 = (1 - p1 - p2)/2

            # If goal s' possible to reach, p1 specifies probability of transition
            # If goal s' possible to reach, p2 specifies probability of self-transition
            if moveGoal is not None:
                if nAdjacent == 2:
                    probs[state, direction, moveGoal] = p1
                else:
                    probs[state, direction, moveGoal] = p1 + p3
                probs[state, direction, state] = p2
            else:
                # If goal s' not possible to reach, self-transition prob is p1 + p2
                if nAdjacent == 2:
                    probs[state, direction, state] = p1 + p2
                else:
                    probs[state, direction, state] = p1 + p2 + p3

            # Do probabilities for adjacent moves
            for adj in moveAdjacent:
                probs[state, direction, adj] = p3

    # Set terminal state
    probs[9, :, :] = 0
    probs[9, :, 9] = 1
    return probs


def possibleNextStates(state, action):
    # Possible next states starts off as empty
    states = []
    # If it's possible to reach the goal state (if the goal state doesn't go off the board)
    # Append it
    if possibleGoal(state, action):
        goalState = getNextState(state, action)
        states.append(goalState)
    # Otherwise append None
    else:
        states.append(None)

    # Append this state since self transition is always possible
    states.append(state)
    # Get adjacent state(s) which can be 1 or 2 and append them
    adjacents = getAdjacentStates(state, action)
    # [states.append(i) for i in adjacents]
    states.append(adjacents)
    return states


def getNextState(state, action):
    if action == UP:
        return getUpwardsOf(state)
    if action == RIGHT:
        return getRightOf(state)
    if action == DOWN:
        return getDownwardsOf(state)
    if action == LEFT:
        return getLeftOf(state)


def possibleGoal(state, action):
    if hasWallNorth(state) and action == UP:
        return False
    if hasWallEast(state) and action == RIGHT:
        return False
    if hasWallSouth(state) and action == DOWN:
        return False
    if hasWallWest(state) and action == LEFT:
        return False
    else:
        return True


def getProbNextStates(state, action, p1, p2, p3):
    # If trying to go up when blocked by walls upwards
    if hasWallNorth(state) and action == UP:
        probNoMove = p1 + p2
    # If trying to go right when blocked by walls rightwards
    if hasWallEast(state) and action == RIGHT:
        probNoMove = p1 + p2
    # If trying to go down when blocked by walls downwards
    if hasWallSouth(state) and action == DOWN:
        probNoMove = p1 + p2
    # If trying to go left when blocked by walls leftwards
    if hasWallWest(state) and action == LEFT:
        probNoMove = p1 + p2


def getAdjacentStates(state, action):
    if action == UP:
        return getUpwardsAdjacents(state)
    elif action == RIGHT:
        return getRightwardsAdjacents(state)
    elif action == DOWN:
        return getDownwardsAdjacents(state)
    elif action == LEFT:
        return getLeftwardsAdjacents(state)


# Trying to move up from any state, get adjacent states
def getUpwardsAdjacents(state):
    '''
    If a state borders a wall to the north, the adjacent states are
    ones next to the state. If a state does not border a wall to the north,
    the adjacent states are the ones next to the goal state
    '''
    if hasWallNorth(state):
        if hasWallEast(state):
            return [state - 1]
        if hasWallWest(state):
            return [state + 1]
        else:
            return [state - 1, state + 1]

    else:
        stateUp = getUpwardsOf(state)
        if hasWallEast(stateUp):
            return [stateUp - 1]
        if hasWallWest(stateUp):
            return [stateUp + 1]
        else:
            return [stateUp - 1, stateUp + 1]


def getRightwardsAdjacents(state):
    if hasWallEast(state):
        if hasWallNorth(state):
            return [state + 10]
        if hasWallSouth(state):
            return [state - 10]
        else:
            return [state - 10, state + 10]
    else:
        stateRight = getRightOf(state)
        if hasWallNorth(stateRight):
            return [stateRight + 10]
        if hasWallSouth(stateRight):
            return [stateRight - 10]
        else:
            return [stateRight - 10, stateRight + 10]


def getDownwardsAdjacents(state):
    if hasWallSouth(state):
        if hasWallEast(state):
            return [state - 1]
        if hasWallWest(state):
            return [state + 1]
        else:
            return [state - 1, state + 1]
    else:
        stateDown = getDownwardsOf(state)
        if hasWallEast(stateDown):
            return [stateDown - 1]
        if hasWallWest(stateDown):
            return [stateDown + 1]
        else:
            return [stateDown - 1, stateDown + 1]


def getLeftwardsAdjacents(state):
    if hasWallWest(state):
        if hasWallNorth(state):
            return [state + 10]
        if hasWallSouth(state):
            return [state - 10]
        else:
            return [state - 10, state + 10]
    else:
        stateLeft = getLeftOf(state)
        if hasWallNorth(stateLeft):
            return [stateLeft + 10]
        if hasWallSouth(stateLeft):
            return [stateLeft - 10]
        else:
            return [stateLeft - 10, stateLeft + 10]

# Given a state, action, and environment, pick the next state stochastically
# Invisible to agent
# def pick_next_state(state, action, probs):
#     next_state_probs = probs[state, action, :]
#     next_state = np.random.choice(list(range(100)), p=next_state_probs)
#     return next_state

if __name__ == '__main__':
    createStochastic(1, 0)
