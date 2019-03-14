import argparse
import mc_alg
import q
import sarsa
from utils import draw_policy

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='', type=str)
parser.add_argument('-i', '--iterations', default=1000, type=int)
parser.add_argument('-p1', '--p1', default=1.0, type=float)
parser.add_argument('-p2', '--p2', default=0.0, type=float)
parser.add_argument('-a', '--alpha', default=0.1, type=float)
parser.add_argument('-g', '--gamma', default=0.9, type=float)
parser.add_argument('-e', '--epsilon', default=0.1, type=float)
args = parser.parse_args()

f = args.file
iterations = args.iterations
p1 = args.p1
p2 = args.p2
alpha = args.alpha
gamma = args.gamma
epsilon = args.epsilon

if f == 'mc_alg.py':
    policy = mc_alg.main(iterations, p1, p2, alpha, gamma, epsilon)
elif f == 'q.py':
    policy = q.main(iterations, p1, p2, alpha, gamma, epsilon)
elif f == 'sarsa.py':
    policy = sarsa.main(iterations, p1, p2, alpha, gamma, epsilon)
else:
    print('Enter a file/algorithm to run.')
    print('-f [file] where [file] is one of [\'mc_alg.py\', \'q.py\', \'sarsa.py\']')
    exit(1)

config = {}
config['alg'] = f[:-3]
config['a'] = alpha
config['g'] = gamma
config['e'] = epsilon
config['p1'] = p1
config['p2'] = p2
config['it'] = iterations
draw_policy(policy, config)









