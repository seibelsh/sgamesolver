sgamesolver.SGame
=================

*class* **sgamesolver.SGame(** *payoff_matrices*, *transition_matrices*,
*discount_factors* **)**

   Container for a stochastic game.

   **Parameters:**

      **payoff_matrices** : *list of array-like*
         One payoff matrix for each state.
         Each payoff matrix should be a nested list or a numpy array with
         dimensions :math:`I \times A_0 \times \dots \times A_{I}`,
         where the first dimension indexes the player
         (:math:`I` denotes the number of players)
         and the remaining dimensions index the action profile
         (:math:`A_i` denotes the number of actions of player :math:`i`).
         Entries denote the payoffs of the corresponding player
         in the corresponding state,
         given the strategy profile is played.

      **transition_matrices** : *list of array-like*
         One transition matrix for each state.
         Each transition matrix should be a nested list or a numpy array with
         dimensions :math:`A_0 \times \dots \times A_I \times S`,
         where the last dimension indexes the destination state
         (:math:`S` denotes the number of states)
         and the remaining dimensions index the action profile.
         Entries denote the probability of transitioning
         from the corresponding state to the destination state,
         given the strategy profile is played.

      **discount_factors** : *float, int, or array-like*
         One discount factor for each player.
         Each discount factor must be in :math:`[0,1)`.
         In case of a single number, a common discount factor is assumed.

Examples
--------

Defining a stochastic game with two states, two players and two actions each:
Matching Pennies with random switching of roles.

>>> game = sgamesolver.SGame(payoff_matrices=[[[[1, 0],
...                                             [0, 1]],
...                                            [[0, 1],
...                                             [1, 0]]],
...                                           [[[0, 1],
...                                             [1, 0]],
...                                            [[1, 0],
...                                             [0, 1]]]],
...                          transition_matrices=[[[[0.5, 0.5],
...                                                 [0.5, 0.5]],
...                                                [[0.5, 0.5],
...                                                 [0.5, 0.5]]],
...                                               [[[0.5, 0.5],
...                                                 [0.5, 0.5]],
...                                                [[0.5, 0.5],
...                                                 [0.5, 0.5]]]],
...                          discount_factors=[0.9, 0.9])

Attributes
----------

=================  =========================================================
num_states         Number of states.
num_players        Number of players.
nums_actions       Number of actions for each player in each state.
num_actions_max    Maximum number of actions over states and players.
num_actions_total  Total number of actions summed across states and players.
action_mask        Mask to facilitate normalization of payoffs.
payoffs            Payoff for each state, player and strategy profile.
payoff_min         Minimum payoff over states, players and action profiles.
payoff_max         Maximum payoff over states, players and action profiles.
transitions        State transition probabilities for each player.
phi                State transition probabilities.
state_labels       Label for each state.
player_labels      Label for each player.
action_labels      Label for each action of each player in each state.
=================  =========================================================

Methods
-------

======================================================================================  ==================================================
check_equilibrium(strategy_profile)                                                     Calculate epsilon-equilibriumness.
centroid_strategy([zeros])                                                              Generate the centroid strategy profile.
flatten_strategies(strategies)                                                          Convert nested strategy profile to flat array.
flatten_values(values)                                                                  Convert nested state-player values to flat array.
from_table(table)                                                                       Define SGame from table.
get_values(strategy_profile)                                                            Calculate state-player values for strateg profile.
one_shot_game(payoff_matrix)                                                            Define a one-shot game.
random_game(num_states, num_players, ...)                                               Define a random stochastic game.
random_strategy([zeros, seed])                                                          Generate a random strategy profile.
random_weights([low, high, zeros, seed])                                                Generate a random set of strategy weights.
to_table()                                                                              Convert SGame to table.
:ref:`unflatten_strategies(strategies_flat[, zeros]) <sgame_unflatten_strategies>`      Convert flat strategy profile to nested array.
unflatten_values(values_flat)                                                           Convert flat state-player values to nested array.
:ref:`weighted_centroid_strategy(weights[, zeros]) <sgame_weighted_centroid_strategy>`  Generate a weighted centroid strategy profile.
======================================================================================  ==================================================
