import sgamesolver
import numpy as np
import pandas as pd
from ._helpers import solve_game, assert_games_equal


# %% normal-form game: prisoner's dilemma


payoff_matrix = np.array([[[2, 0],
                           [3, 1]],
                          [[2, 3],
                           [0, 1]]])

# payoff_matrix.shape = (2,2,2)
# indices: [player, action_0, action_1]

game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

# optional: overwrite action labels
game.action_labels = ['cooperate', 'defect']

solve_game(game)


game_table = pd.DataFrame(data=[['delta', '', '', 0, 0, np.nan],
                                ['state0', 'cooperate', 'cooperate', 2, 2, 0],
                                ['state0', 'cooperate', 'defect', 0, 3, 0],
                                ['state0', 'defect', 'cooperate', 3, 0, 0],
                                ['state0', 'defect', 'defect', 1, 1, 0]],
                          columns=['state', 'a_player0', 'a_player1',
                                   'u_player0', 'u_player1', 'phi_state0'])

game2 = sgamesolver.SGame.from_table(game_table)

assert_games_equal(game, game2)
