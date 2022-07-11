import sgamesolver
import numpy as np
import pandas as pd
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


# %% TODO: check solver


payoff_matrix = np.array([[[3, 0],
                           [2, 1]],
                          [[3, 2],
                           [0, 1]]])

# payoff_matrix.shape = (2,2,2)
# indices: [player, action_0, action_1]

game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

# optional: overwrite action labels
game.action_labels = ['stag', 'hare']

homotopy = sgamesolver.homotopy.LogTracing(game)
homotopy.solver_setup()
homotopy.solver.set_parameters(homotopy.robust_parameters)
homotopy.solve()
