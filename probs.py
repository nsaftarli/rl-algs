import numpy as np

UP = 0
RIGHT = 1
DOWN = 2
LEFT  = 3

# For modeling the unknown transition probabilities
def createStochastic(p1, p2):
    actionStoN = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
    actionNtoS = ['up', 'right', 'down', 'left']

    # Used for getting all the states that are along edges
    edge_states = []
    states = list(range(0, 100))
    for state in states:
        if isTopRow(state):
            edge_states.append(state)
        if isRightCol(state):
            edge_states.append(state)
        if isBottomRow(state):
            edge_states.append(state)
        if isLeftCol(state):
            edge_states.append(state)

    unique, counts = np.unique(edge_states, return_counts=True)
    unique_edge_states = dict(zip(unique, counts))
    # print(unique_edge_states)
    #######################################################################

    # Transition probabilities. Suppose grid of s a s'
    probs = np.zeros((100, 4, 100))
    for state in states:
        for direction in range(4):
            possNextStates = possibleNextStates(state, direction)

            moveGoal = possNextStates[0]
            moveSelf = possNextStates[1]
            moveAdjacent = possNextStates[2]
            nAdjacent = len(moveAdjacent)
            p3 = (1 - p1 - p2)/nAdjacent

            # If goal s' possible to reach, p1 specifies probability of transition
            # If goal s' possible to reach, p2 specifies probability of self-transition
            if moveGoal is not None:
                if nAdjacent == 2:
                    probs[state, direction, moveGoal] = p1
                else:
                    probs[state, direction, moveGoal] = p1 + (1 - p1 - p2)/2
                probs[state, direction, state] = p2
            else:
                # If goal s' not possible to reach, self-transition prob is p1 + p2
                if nAdjacent == 2:
                    probs[state, direction, state] = p1 + p2
                else:
                    probs[state, direction, state] = p1 + p2 + (1 - p1 - p2)/2

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


def setEdges(grid, edges, p1, p2, p3):
    for edge in edges[0]:
        # Set probability for up from top row
        pass
    for edge in edges[1]:
        # Set prob for right from right col
        pass
    for edge in edges[2]:
        # Set prob for down from bottom row
        pass
    for edge in edges[3]:
        # Set prob for left from left col
        pass

    return newGrid


def setCorners(grid, corners, p1, p2, p3):
    for corner in corners[0]:
        # Set for top-right
        pass
    for corner in corners[1]:
        # Set for bottom-right
        pass
    for corner in corners[2]:
        # Set for bottom-left
        pass
    for corner in corners[3]:
        # Set for top-left
        pass

    return newGrid


def getUpwardsOf(state_num):
    return state_num - 10


def getRightOf(state_num):
    return state_num + 1


def getDownwardsOf(state_num):
    return state_num + 10


def getLeftOf(state_num):
    return state_num - 1


def isTopRow(state):
    return True if state - 10 < 0 else False


def isRightCol(state):
    return True if state % 10 == 9 else False


def isBottomRow(state):
    return True if state + 10 >= 100 else False


def isLeftCol(state):
    return True if state % 10 == 0 else False


def hasWallEast(state):
    return True if (
        (state % 10 == 4 and state != 24 and state != 74)
        or
        (isRightCol(state)))\
        else False


def hasWallWest(state):
    return True if (
        (state % 10 == 5 and state != 25 and state != 75)
        or
        (isLeftCol(state)))\
        else False


def hasWallNorth(state):
    return True if (
        (state >= 50 and state < 60 and state != 52 and state != 57)
        or
        (isTopRow(state)))\
        else False


def hasWallSouth(state):
    return True if (
        (state >= 40 and state < 50 and state != 42 and state != 47)
        or
        (isBottomRow(state)))\
        else False


if __name__ == '__main__':
    createStochastic(1, 0)
