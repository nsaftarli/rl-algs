import numpy as np

def init_policy(epsilon):
    pi = np.zeros((100, 4))
    for i in range(100):
        best_action = np.random.randint(0, 4)
        pi[i, :] = epsilon
        pi[i, best_action] = 1 - epsilon
    return pi

if __name__ == '__main__':
    init_policy(0.1)