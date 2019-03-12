import numpy as np
import random

qSa = list()
returns = list()
stateActions = list()

for i in range(0, 10):
    qSa.append([])
    returns.append([])
    stateActions.append([])
    for j in range(0, 10):
        qSa[i].append([0, 0, 0, 0])
        returns[i].append([[], [], [], []])
        stateActions[i].append([0.25, 0.25, 0.25, 0.25])

def randomStart():
    ret = [0, 9]
    while(ret == [0, 9]):
        ret = [random.randint(0, 9), random.randint(0, 9)]
    return ret

def env(start):
    envStateActions = list()
    envN = envNextAction(start)
    envStateActions.append([envN[0], envN[1]])
    reward = -1

    # envN is 3D array [s][a][s']
    while envN[0] != [0, 9]:
        envN = envNextAction(envN[2])

        reward += -1

        envStateActions.append([envN[0], envN[1]])

    reward += 100
    return [envStateActions, reward]

def envNextAction(state):
    choice = random.uniform(0.0, 1.0)

    if choice <= stateActions[state[0]][state[1]][0]:
        if state[0] - 1 >= 0:
            return [state, 0, [state[0]-1, state[1]]]

    elif choice <= stateActions[state[0]][state[1]][0] + stateActions[state[0]][state[1]][1]:
        if state[1] + 1 <= 9:
            return [state, 1, [state[0], state[1]+1]]

    elif choice <= stateActions[state[0]][state[1]][0] + stateActions[state[0]][state[1]][1] + stateActions[state[0]][state[1]][2]:
        if state[0] + 1 <= 9:
            return [state, 2, [state[0]+1, state[1]]]

    else:
        if state[1] - 1 >= 0:
            return [state, 3, [state[0], state[1]-1]]

    return envNextAction(state)

for i in range(5000):
    start = randomStart()
    episode = env(start)
    G = episode[1]

    for j in range(0, len(episode[0])): #[[0, 1], 0]
        returns[episode[0][j][0][0]][episode[0][j][0][1]][episode[0][j][1]].append(G)
        qSa[episode[0][j][0][0]][episode[0][j][0][1]][episode[0][j][1]] = sum(returns[episode[0][j][0][0]][episode[0][j][0][1]][episode[0][j][1]]) / len(returns[episode[0][j][0][0]][episode[0][j][0][1]][episode[0][j][1]])

    eachState = [[False] * 10] * 10

    for j in range(0, len(episode[0])):
        if eachState[episode[0][j][0][0]][episode[0][j][0][1]] != True:
            eachState[episode[0][j][0][0]][episode[0][j][0][1]] = True
            tempMax = qSa[episode[0][j][0][0]][episode[0][j][0][1]].index(max(qSa[episode[0][j][0][0]][episode[0][j][0][1]]))

            for i in range(0, 4):
                if i == tempMax:
                    qSa[episode[0][j][0][0]][episode[0][j][0][1]][i] = 1 - 0.1 + 0.1/4

                else:
                    qSa[episode[0][j][0][0]][episode[0][j][0][1]][i] = 0.1/4

for i in range(0, 10):
    print ""
    for j in range(0, 10):
        print qSa[i][j] ,
