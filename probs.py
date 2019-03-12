import numpy as np

UP = 0
RIGHT = 1
DOWN = 2
LEFT  = 3
# For modeling the unknown transition probabilities
def createStochastic(p1, p2):
    p3 = (1 - p1 - p2) / 2
    actionStoN = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
    actionNtoS = ['up', 'right', 'down', 'left']
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT  = 3

    start_action_table = np.zeros((10, 10, 4))
    # Transitions modeled by [s, a, s']
    transition_probs = np.zeros((100, 4, 100))

    # # Set these first
    # edges = [[], [], [], []]
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

    # print(edge_states)
    unique, counts = np.unique(edge_states, return_counts=True)
    unique_edge_states = dict(zip(unique, counts))
    print(unique_edge_states)
    return

    # # Overwrite corners
    # corners = [[], [], [], []]
    # for state in states:
    #     if isTopRow(state) and isRightCol(state):
    #         corners[0].append(state)
    #     if isRightCol(state) and isBottomRow(state):
    #         corners[1].append(state)
    #     if isBottomRow(state) and isLeftCol(state):
    #         corners[2].append(state)
    #     if isLeftCol(state) and isTopRow(state):
    #         corners[3].append(state)

    cantGoUp = []
    cantGoRight = []
    cantGoDown = []
    cantGoLeft = []
    for state in states:
        if hasWallNorth(state):
            cantGoUp.append(state)
        if hasWallEast(state):
            cantGoRight.append(state)
        if hasWallSouth(state):
            cantGoDown.append(state)
        if hasWallWest(state):
            cantGoLeft.append(state)
    print("Up blocked: ", cantGoUp)
    print("Right blocked: ", cantGoRight)
    print("Down blocked: ", cantGoDown)
    print("Left blocked: ", cantGoLeft)

    # Now for the actual transition probabilities. Suppose grid of s a s'

    probs = np.zeros((100, 4, 100))
    for state in states:
        for direction in range(4):
            possNextStates = possibleNextStates(state, direction)

            moveGoal = possNextStates[0]
            noMove = possNextStates[1]
            moveAdjacent = possNextStates[2]

            # If goal s' possible to reach, p1 specifies probability of transition
            if moveGoal != -1:
                probs[state, direction, moveGoal] = p1

            # Probability of self transition depends on whether or not state is edge case
            # probs[state, direction, noMove] = 


def possibleNextStates(state, action):
    states = []
    if possibleGoal(state, action):
        goalState = getNextState(state, action)
        states.append(goalState)
    else:
        states.append(-1)

    states.append(state)
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
    print("ACTION IS: ", action)
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
            print("HAS WALL EAST")
            return [stateDown - 1]
        if hasWallWest(stateDown):
            print("HAS WALL WEST")
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
