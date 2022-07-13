"""Stag hunt examples on how to use sGameSolver."""


import datetime
import sys

import sgamesolver
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize

from examples._helpers import solve_game, assert_games_equal


# %% normal-form game: stag hunt


payoff_matrix = np.array([[[10, 1],
                           [8, 5]],
                          [[10, 8],
                           [1, 5]]])

# payoff_matrix.shape = (2,2,2)
# indices: [player, action_0, action_1]

game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

# optional: overwrite action labels
game.action_labels = ['stag', 'hare']

solve_game(game)


game_table = pd.DataFrame(data=[['delta', '', '', 0, 0, np.nan],
                                ['state0', 'stag', 'stag', 10, 10, 0],
                                ['state0', 'stag', 'hare', 1, 8, 0],
                                ['state0', 'hare', 'stag', 8, 1, 0],
                                ['state0', 'hare', 'hare', 5, 5, 0]],
                          columns=['state', 'a_player0', 'a_player1',
                                   'u_player0', 'u_player1', 'phi_state0'])

game2 = sgamesolver.SGame.from_table(game_table)

assert_games_equal(game, game2)


# %% qre for multiple lambdas


homotopy = sgamesolver.homotopy.QRE(game)
homotopy.solver_setup()
homotopy.solver.verbose = 0  # make silent

lambdas = np.arange(0.1, 2.1, 0.1)

# for player_0 only (strategies of player_1 identical due to symmetry)
strategies = np.zeros(shape=(len(lambdas), 2), dtype=np.float64)

for idx, lambda_ in enumerate(lambdas):
    homotopy.solver.t_target = lambda_
    homotopy.solve()
    strategies[idx] = homotopy.equilibrium.strategies[0, 0]  # state_0, player_0

plt.plot(lambdas, strategies[:, 0], label='stag')
plt.plot(lambdas, strategies[:, 1], label='hare')
plt.xlabel(r'$\lambda$')
plt.ylabel('strategy')
plt.legend()
# plt.show()

plt.savefig("docs/source/img/stag_hunt_qre_lambdas.svg", bbox_inches='tight')


# %% start at equilibrium

homotopy = sgamesolver.homotopy.LogTracing(game)
homotopy.solver_setup()
homotopy.solve()

print(homotopy.equilibrium)
# +++++++++ state0 +++++++++
#                      stag  hare
# player0 : v=5.00, σ=[0.000 1.000]
# player1 : v=5.00, σ=[0.000 1.000]


# mixed equilibrium

def f(q):
    return np.dot(payoff_matrix[0][0], np.array([q, 1-q])) - np.dot(payoff_matrix[0][1], np.array([q, 1-q]))


q = scipy.optimize.brentq(f, 1e-9, 1 - 1e-9)
assert q > 0 and q < 1

strategies = np.array([[[q, 1 - q],
                        [q, 1 - q]]])
print(strategies)
# array([[[0.66666667, 0.33333333],
#         [0.66666667, 0.33333333]]])

assert np.allclose(game.check_equilibrium(strategies), 0)

values = game.get_values(strategies)
print(values)
# array([[7., 7.]])

y0 = homotopy.sigma_V_t_to_y(strategies, values, 1)
assert np.allclose(homotopy.H(y0), 0)

homotopy.solver_setup()
homotopy.solver.y = y0
homotopy.solver.sign *= -1  # going "backwards"
homotopy.solve()

print(homotopy.equilibrium)
# +++++++++ state0 +++++++++
#                       stag  hare
# player0 : v=10.00, σ=[1.000 0.000]
# player1 : v=10.00, σ=[1.000 0.000]


# %% log tracing: searching prior space


payoff_matrix = np.array([[[10, 1],
                           [8, 5]],
                          [[10, 8],
                           [1, 5]]])
game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

runs = 100
strategies = np.zeros(shape=(runs, 4), dtype=np.float64)

for run in range(runs):
    # homotopy = sgamesolver.homotopy.LogTracing(game, rho='random')
    rho = homotopy.game.random_strategy(seed=run)
    homotopy = sgamesolver.homotopy.LogTracing(game, rho=rho)
    homotopy.solver_setup()
    homotopy.solver.verbose = 0  # make silent
    homotopy.solve()
    strategies[run] = homotopy.equilibrium.strategies[0].flatten().round(4)  # state 

print(np.unique(strategies, axis=0))


def get_eq(strat: np.ndarray) -> str:
    if np.allclose(strat, np.array([0, 1, 0, 1])):
        return 'hare'
    elif np.allclose(strat, np.array([1, 0, 1, 0])):
        return 'stag'
    elif np.allclose(np.array([2/3, 1/3, 2/3, 1/3])):
        return 'mixed'
    else:
        raise ValueError('unknown equilibrium')


equilibria = np.array([get_eq(strat) for strat in strategies])
eq_vals, counts = np.unique(equilibria, return_counts=True)
pcts = 100 * counts / counts.sum()

plt.bar(eq_vals, pcts)
plt.xticks([0, 1, 2], ['(hare, hare)', '(stag, stag)', 'mixed'])
plt.xlim(-0.6, 2.6)
plt.ylabel('%')
plt.ylim(0, 100)
# plt.show()

plt.savefig("docs/source/img/stag_hunt_logtracing_search_priors.svg", bbox_inches='tight')


# systematic search

# priors = np.linspace

# toc = datetime.datetime.now()
# sys.stdout.write(f"done run {run + 1} / {runs}. time elapsed = {str(toc-tic).split('.')[0]}\r")
# sys.stdout.flush()


# %% TODO: check solver


payoff_matrix = np.array([[[3, 0],
                           [2, 1]],
                          [[3, 2],
                           [0, 1]]])
game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

homotopy = sgamesolver.homotopy.LogTracing(game)
homotopy.solver_setup()
# homotopy.solver.set_parameters(homotopy.robust_parameters)
homotopy.solve()
