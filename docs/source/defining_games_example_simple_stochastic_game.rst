Example: Simple stochastic game
===============================

Consider the following dynamic variation of Rock Paper Scissors.
Two players play Rock Paper Scissors repeatedly and incorporate "scissor loading".
Having solely played scissors in the previous round (while the opponent has not)
wins a tie on scissors in the next round.
If both players have played scissors,
neither of them gets the tie-breaking scissors advantage.

The dynamic variation of Rock Paper Scissors features three states:

.. math:: s \in \begin{cases} 0 & \text{neutral state} \\ 1 & \text{player 0 has loaded scissors} \\ 2 & \text{player 1 has loaded scissors} \end{cases}

The corresponding payoffs are given by

+---------+----------+--------+-------+-------------+
|                    | player1                      |
+                    +--------+-------+-------------+
|                    | rock   | paper | scissors    |
+---------+----------+--------+-------+-------------+
| player0 | rock     | 0, 0   | -1, 1 | 1, -1       |
+         +----------+--------+-------+-------------+
|         | paper    | 1, -1  | 0, 0  | -1, 1       |
+         +----------+--------+-------+-------------+
|         | scissors | -1, 1  | 1, -1 | X(s), -X(s) |
+---------+----------+--------+-------+-------------+

with

.. math:: X(s) = \begin{cases} 0 & \text{if } s=0 \\ 1 & \text{if } s=1 \\ -1 & \text{if } s=2 \end{cases}

This game can be defined by submitting payoffs, transitions
and discount factors to :py:class:`SGame`.

.. code-block:: python

    import sgamesolver
    import numpy as np

    payoff_matrices = [  # state0:
                       np.array([[[0, -1,  1],
                                  [1,  0, -1],
                                  [-1, 1,  0]],
                                 [[0,  1, -1],
                                  [-1, 0,  1],
                                  [1, -1,  0]]]),
                         # state1:
                       np.array([[[0, -1,  1],
                                  [1,  0, -1],
                                  [-1, 1,  1]],    # player0 wins tie on Scissors
                                 [[0,  1, -1],
                                  [-1, 0,  1],
                                  [1, -1, -1]]]),  # player1 loses tie on Scissors
                         # state2:
                       np.array([[[0, -1,  1],
                                  [1,  0, -1],
                                  [-1, 1, -1]],    # player0 loses tie on Scissors
                                 [[0,  1, -1],
                                  [-1, 0,  1],
                                  [1, -1,  1]]])]  # player1 wins tie on Scissors

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

The list ``payoff_matrices`` contains one payoff matrix for each state.
Each payoff matrix is a NumPy array with dimensions
:math:`I \times A_0 \times \dots \times A_{I}`,
where the first dimension indexes the player and
:math:`A_i` denotes the number of actions of player :math:`i`.

The list ``transition_matrices`` contains one transition matrix for each state.
Each transition matrix is a NumPy array with dimensions
:math:`A_0 \times \dots \times A_2 \times S`,
where the last dimension indexes the destination state.

The argument ``discount_factors`` can either be common discount factor
:math:`\delta \in [0,1)` or an array with dimension :math:`I`
containing one discount factor :math:`\delta_i \in [0,1)`
for each player :math:`i`.
Here, a common discount factor is chosen.

As an alternative to submitting arrays for payoffs, transitions and
discount factors, a game table can be provided.

=======  =========  =========  =========  =========  ===========  ==========  ==========
state    a_p0       a_p1       u_p0       u_p1       phi_neutral  phi_adv_p0  phi_adv_p1
=======  =========  =========  =========  =========  ===========  ==========  ==========
delta                          0.95       0.95
neutral  rock       rock       0          0          1            0           0
neutral  rock       paper      -1         1          1            0           0
neutral  rock       scissors   1          -1         0            0           1
neutral  paper      rock       1          -1         1            0           0
neutral  paper      paper      0          0          1            0           0
neutral  paper      scissors   -1         1          0            0           1
neutral  scissors   rock       -1         1          0            1           0
neutral  scissors   paper      1          -1         0            1           0
neutral  scissors   scissors   0          0          1            0           0
adv_p0   rock       rock       0          0          1            0           0
adv_p0   rock       paper      -1         1          1            0           0
adv_p0   rock       scissors   1          -1         0            0           1
adv_p0   paper      rock       1          -1         1            0           0
adv_p0   paper      paper      0          0          1            0           0
adv_p0   paper      scissors   -1         1          0            0           1
adv_p0   scissors   rock       -1         1          0            1           0
adv_p0   scissors   paper      1          -1         0            1           0
adv_p0   scissors   scissors   1          -1         1            0           0
adv_p1   rock       rock       0          0          1            0           0
adv_p1   rock       paper      -1         1          1            0           0
adv_p1   rock       scissors   1          -1         0            0           1
adv_p1   paper      rock       1          -1         1            0           0
adv_p1   paper      paper      0          0          1            0           0
adv_p1   paper      scissors   -1         1          0            0           1
adv_p1   scissors   rock       -1         1          0            1           0
adv_p1   scissors   paper      1          -1         0            1           0
adv_p1   scissors   scissors   -1         1          1            0           0
=======  =========  =========  =========  =========  ===========  ==========  ==========

The game table specifies for each state and action profile
the corresponding payoffs and state transitions.
Additionally, the first row specifies the discount factors for each player.
Here, the players have been named *p0* and *p1*,
states are named *neutral*, *adv_p0* and *adv_p1*,
and actions are labeled *rock*, *paper* and *scissors*.

To import the game table, use the :py:meth:`SGame.from_table` method.
It accepts xlsx, xls, csv, txt, and dta files.

.. code-block:: python

    import sgamesolver
    game = sgamesolver.SGame.from_table('path/to/table.xlsx')
