# Reinforcement Learning - Assignment 3

## Nariman Saftarli - nsaftarli@ryerson.ca - 500615448
## Nimrod Vanir - nimrod.vanir@ryerson.ca - 500699818

#### Requirements/Dependencies:

* Python 3.6
* Numpy
* Matplotlib
* SciPy (only used for interpolation when graphing outputs in `run_gridworld.py`)

#### Instructions for running

* The three algorithms are located in `mc_alg.py`, `q.py`, and `sarsa.py` for the Monte Carlo, Q-Learning, and SARSA algorithms respectively. `run_gridworld.py` is a script that will run one of these, outputting the result to the terminal. 

* I've included an argument parser. `-f` specifies the file of the algorithm to be run, `-i` is iterations to run for, `-p1` is probability of successful transition to next state, `-p2` is probability of successful transition to self state, `-a` is alpha, `-g` is gamma, `-e` is epsilon, `-p` is an option to graphically create and save an image of the policy (used for the report, change directory in `utils.py` to use this), and `-g` is an option to draw and display the average rewards collected for both Q-Learning and SARSA (used for the report).

* An example line of code that will run the Q-Learning function for 1000 episodes, with alpha set to 0.1, p1 set to 0.75, p2 set to 0.2, and epsilon set to 0.1: `python3 run_gridworld.py -f 'q.py' -i 1000 -p1 0.75 -p2 0.2 -a 0.1 -e 0.1`. Resulting policy will print to the terminal.

### Notes

* The `-g` and `-p` arguments were meant to generate figures for the report, so the functions they call use specific font files and project directory. In general, any monospaced unicode font will work, and the directory `./Report/images/` should exist to run these (otherwise the final policy will just print to the terminal). `-g` takes a long time because it does 100 iterations of both Q-Learning and SARSA. 

* `probs.py` deals with the environment. The agent doesn't have access to the environment directly, so there is an Environment class within `probs.py` that is created at the start of each algorithm, and this deals with the dynamics of movement within the grid as well as rewards given.

* `utils.py` is for rules (such as checking whether the agent is by a wall) and also includes the code for printing the final policy.

* `initializations.py` deals with initializing policies and value functions.

* `action_select.py` deals with action selection.