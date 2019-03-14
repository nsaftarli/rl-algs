import numpy as np

def init_policy(epsilon):
    pi = np.zeros((100, 4))


    for i in range(100):
        best_action = np.random.randint(0, 4)
        pi[i, :] = epsilon / 4
        pi[i, best_action] = 1 - epsilon + epsilon / 4

    return pi

def init_policy_egreedy(epsilon):
    pi = np.zeros((100, 4))
    roll = np.random.rand()
    if roll > epsilon:
        # exploit
        pass
    else:
        # explore
        pass



if __name__ == '__main__':
    init_policy(0.1)