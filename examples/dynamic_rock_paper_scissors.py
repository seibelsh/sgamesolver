import sgamesolver
import numpy as np
import pandas as pd
from examples._helpers import solve_game, assert_games_equal


# %% stochastic game: dynamic rock-paper-scissors


# dynamic variation of Rock-Paper-Scissors:
#   - if one player played Scissors in the previous round
#     (and the other player did NOT play Scissors),
#     that player will win a tie on Scissors in the next round
#   - if both players or neither player played Scissors in the previous round,
#     a normal round of Rock-Paper-Scissors is played

# 3 states:
#   0: both players or neither player have played Scissors in the previous round
#   1: player0 has played Scissors in the previous round and player1 has not
#   2: player1 has played Scissors in the previous round and player0 has not


payoff_matrices = [  # state0:
                   np.array([[[0,  -1,  1],
                              [1,   0, -1],
                              [-1,  1,  0]],
                             [[0,   1, -1],
                              [-1,  0,  1],
                              [1,  -1,  0]]]),
                     # state1:
                   np.array([[[0,  -1,  1],
                              [1,   0, -1],
                              [-1,  1,  1]],    # player0 wins tie on Scissors
                             [[0,   1, -1],
                              [-1,  0,  1],
                              [1,  -1, -1]]]),  # player1 loses tie on Scissors
                     # state2:
                   np.array([[[0,  -1,  1],
                              [1,  0, -1],
                              [-1,  1, -1]],    # player0 loses tie on Scissors
                             [[0,   1, -1],
                              [-1,  0,  1],
                              [1,  -1,  1]]])]  # player1 wins tie on Scissors

# transitions identical for each state
transition_matrices = [np.array([[[1, 0, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]],
                                 [[1, 0, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]],
                                 [[0, 1, 0],
                                  [0, 1, 0],
                                  [1, 0, 0]]])] * 3

common_discount_factor = 0.95

game = sgamesolver.SGame(payoff_matrices=payoff_matrices,
                         transition_matrices=transition_matrices,
                         discount_factors=common_discount_factor)

# optional: overwrite action labels
game.action_labels = ['rock', 'paper', 'scissors']

solve_game(game)


game_table = pd.DataFrame(data=[['delta', '', '', 0.95, 0.95, np.nan, np.nan, np.nan],
                                ['neutral', 'rock', 'rock', 0, 0, 1, 0, 0],
                                ['neutral', 'rock', 'paper', -1, 1, 1, 0, 0],
                                ['neutral', 'rock', 'scissors', 1, -1, 0, 0, 1],
                                ['neutral', 'paper', 'rock', 1, -1, 1, 0, 0],
                                ['neutral', 'paper', 'paper', 0, 0, 1, 0, 0],
                                ['neutral', 'paper', 'scissors', -1, 1, 0, 0, 1],
                                ['neutral', 'scissors', 'rock', -1, 1, 0, 1, 0],
                                ['neutral', 'scissors', 'paper', 1, -1, 0, 1, 0],
                                ['neutral', 'scissors', 'scissors', 0, 0, 1, 0, 0],

                                ['adv_p0', 'rock', 'rock', 0, 0, 1, 0, 0],
                                ['adv_p0', 'rock', 'paper', -1, 1, 1, 0, 0],
                                ['adv_p0', 'rock', 'scissors', 1, -1, 0, 0, 1],
                                ['adv_p0', 'paper', 'rock', 1, -1, 1, 0, 0],
                                ['adv_p0', 'paper', 'paper', 0, 0, 1, 0, 0],
                                ['adv_p0', 'paper', 'scissors', -1, 1, 0, 0, 1],
                                ['adv_p0', 'scissors', 'rock', -1, 1, 0, 1, 0],
                                ['adv_p0', 'scissors', 'paper', 1, -1, 0, 1, 0],
                                ['adv_p0', 'scissors', 'scissors', 1, -1, 1, 0, 0],

                                ['adv_p1', 'rock', 'rock', 0, 0, 1, 0, 0],
                                ['adv_p1', 'rock', 'paper', -1, 1, 1, 0, 0],
                                ['adv_p1', 'rock', 'scissors', 1, -1, 0, 0, 1],
                                ['adv_p1', 'paper', 'rock', 1, -1, 1, 0, 0],
                                ['adv_p1', 'paper', 'paper', 0, 0, 1, 0, 0],
                                ['adv_p1', 'paper', 'scissors', -1, 1, 0, 0, 1],
                                ['adv_p1', 'scissors', 'rock', -1, 1, 0, 1, 0],
                                ['adv_p1', 'scissors', 'paper', 1, -1, 0, 1, 0],
                                ['adv_p1', 'scissors', 'scissors', -1, 1, 1, 0, 0]],
                          columns=['state', 'a_p0', 'a_p1', 'u_p0', 'u_p1',
                                   'phi_neutral', 'phi_adv_p0', 'phi_adv_p1'])

game2 = sgamesolver.SGame.from_table(game_table)

assert_games_equal(game, game2)


game_table_2 = pd.DataFrame(data=[['delta', '', '', 0.95, 0.95, ''],
                                  ['neutral', 'rock', 'rock', 0, 0, 'neutral'],
                                  ['neutral', 'rock', 'paper', -1, 1, 'neutral'],
                                  ['neutral', 'rock', 'scissors', 1, -1, 'adv_p1'],
                                  ['neutral', 'paper', 'rock', 1, -1, 'neutral'],
                                  ['neutral', 'paper', 'paper', 0, 0, 'neutral'],
                                  ['neutral', 'paper', 'scissors', -1, 1, 'adv_p1'],
                                  ['neutral', 'scissors', 'rock', -1, 1, 'adv_p0'],
                                  ['neutral', 'scissors', 'paper', 1, -1, 'adv_p0'],
                                  ['neutral', 'scissors', 'scissors', 0, 0, 'neutral'],

                                  ['adv_p0', 'rock', 'rock', 0, 0, 'neutral'],
                                  ['adv_p0', 'rock', 'paper', -1, 1, 'neutral'],
                                  ['adv_p0', 'rock', 'scissors', 1, -1, 'adv_p1'],
                                  ['adv_p0', 'paper', 'rock', 1, -1, 'neutral'],
                                  ['adv_p0', 'paper', 'paper', 0, 0, 'neutral'],
                                  ['adv_p0', 'paper', 'scissors', -1, 1, 'adv_p1'],
                                  ['adv_p0', 'scissors', 'rock', -1, 1, 'adv_p0'],
                                  ['adv_p0', 'scissors', 'paper', 1, -1, 'adv_p0'],
                                  ['adv_p0', 'scissors', 'scissors', 1, -1, 'neutral'],

                                  ['adv_p1', 'rock', 'rock', 0, 0, 'neutral'],
                                  ['adv_p1', 'rock', 'paper', -1, 1, 'neutral'],
                                  ['adv_p1', 'rock', 'scissors', 1, -1, 'adv_p1'],
                                  ['adv_p1', 'paper', 'rock', 1, -1, 'neutral'],
                                  ['adv_p1', 'paper', 'paper', 0, 0, 'neutral'],
                                  ['adv_p1', 'paper', 'scissors', -1, 1, 'adv_p1'],
                                  ['adv_p1', 'scissors', 'rock', -1, 1, 'adv_p0'],
                                  ['adv_p1', 'scissors', 'paper', 1, -1, 'adv_p0'],
                                  ['adv_p1', 'scissors', 'scissors', -1, 1, 'neutral']],
                            columns=['state', 'a_p0', 'a_p1', 'u_p0', 'u_p1', 'to_state'])

game3 = sgamesolver.SGame.from_table(game_table_2)

assert_games_equal(game, game3)


# %% QRE


homotopy = sgamesolver.homotopy.QRE(game)

# default
homotopy.solver_setup()
homotopy.solve()

# silent
homotopy.solver_setup()
homotopy.solver.verbose = 0
homotopy.solve()

# path plot
homotopy.solver_setup()
homotopy.solver.start_storing_path()
homotopy.solve()
homotopy.plot_path()


# %% LogTracing


homotopy = sgamesolver.homotopy.LogTracing(game)

# path plot
homotopy.solver_setup()
homotopy.solver.start_storing_path()
homotopy.solve()
homotopy.plot_path()

fig = homotopy.plot_path()
fig.savefig("docs/source/img/rps_path_s.svg")

fig = homotopy.plot_path(x_axis='t')
fig.savefig("docs/source/img/rps_path_t.svg")

# custom prior: always rock
rho = np.array([  # state0
                [[1, 0, 0],    # player0
                 [1, 0, 0]],   # player1
                # state1
                [[1, 0, 0],    # player0
                 [1, 0, 0]],   # player1
                # state2
                [[1, 0, 0],    # player0
                 [1, 0, 0]]])  # player1
homotopy = sgamesolver.homotopy.LogTracing(game, rho=rho)
homotopy.solver_setup()
homotopy.solver.start_storing_path()
homotopy.solve()
homotopy.plot_path()

# custom weights
nu = np.array([  # state0
               [[1, 2, 3],    # player0
                [1, 2, 3]],   # player1
               # state1
               [[1, 2, 3],    # player0
                [1, 2, 3]],   # player1
               # state2
               [[1, 2, 3],    # player0
                [1, 2, 3]]])  # player1
homotopy = sgamesolver.homotopy.LogTracing(game, nu=nu, eta=0.5)
homotopy.solver_setup()
homotopy.solver.start_storing_path()
homotopy.solve()
homotopy.plot_path()
