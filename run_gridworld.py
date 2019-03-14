import argparse
import mc_alg
import q
import sarsa
from utils import draw_policy
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='', type=str)
parser.add_argument('-i', '--iterations', default=1000, type=int)
parser.add_argument('-p1', '--p1', default=1.0, type=float)
parser.add_argument('-p2', '--p2', default=0.0, type=float)
parser.add_argument('-a', '--alpha', default=0.1, type=float)
parser.add_argument('-g', '--gamma', default=0.9, type=float)
parser.add_argument('-e', '--epsilon', default=0.1, type=float)
parser.add_argument('-p', '--picture', default=False, type=bool)
parser.add_argument('-d', '--draw_graph', default=False, type=bool)

args = parser.parse_args()

f = args.file
iterations = args.iterations
p1 = args.p1
p2 = args.p2
alpha = args.alpha
gamma = args.gamma
epsilon = args.epsilon
make_image = args.picture
draw_graph = args.draw_graph
if f == 'mc_alg.py':
    policy, _ = mc_alg.main(iterations, p1, p2, alpha, gamma, epsilon)
elif f == 'q.py':
    policy, _ = q.main(iterations, p1, p2, alpha, gamma, epsilon)
elif f == 'sarsa.py':
    policy, _ = sarsa.main(iterations, p1, p2, alpha, gamma, epsilon)
else:
    print('Enter a file/algorithm to run.')
    print('-f [file] where [file] is one of [\'mc_alg.py\', \'q.py\', \'sarsa.py\']')
    exit(1)



if make_image:
    config = {}
    config['alg'] = f[:-3]
    config['a'] = alpha
    config['g'] = gamma
    config['e'] = epsilon
    config['p1'] = p1
    config['p2'] = p2
    config['it'] = iterations
    draw_policy(policy, config)


if draw_graph:
    average_val_q = []
    average_val_sarsa = []


    for i in range(100):
        _, v = q.main(100, p1, p2, alpha, gamma, epsilon)
        average_val_q.append(v)
    for i in range(100):
        _, v = sarsa.main(100, p1, p2, alpha, gamma, epsilon)
        average_val_sarsa.append(v)

    print(average_val_q)
    print(average_val_sarsa)
    print(len(average_val_q))
    print(len(average_val_sarsa))
    x = np.linspace(0, 99, 500)
    smooth_q = spline(list(range(100)), average_val_q, x)
    smooth_s = spline(list(range(100)), average_val_sarsa, x)
    # plt.plot(average_val_q)
    plt.title('Average reward for Q learning and SARSA with alpha=' + str(alpha) + ", reducing epsilon")
    plt.plot(x, smooth_q, color='red')
    plt.plot(x, smooth_s, color='blue')
    plt.show()







