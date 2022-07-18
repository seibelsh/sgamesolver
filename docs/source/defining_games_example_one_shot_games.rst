Example: One-shot games
=======================

A one-shot game (normal form game) is a stochastic game
with only one state (:math:`\boldsymbol{\phi}=\boldsymbol{1}`)
and full discounting (:math:`\boldsymbol{\delta}=\boldsymbol{0}`).
Any one-shot game is fully specified
by its payoff matrix :math:`\boldsymbol{u}`.

A famous example is the Prisoner's Dilemma:

+---------+-----------+-----------+--------+
|                     | player1            |
+                     +-----------+--------+
|                     | cooperate | defect |
+---------+-----------+-----------+--------+
| player0 | cooperate | 2, 2      | 0, 3   |
+         +-----------+-----------+--------+
|         | defect    | 3, 0      | 1, 1   |
+---------+-----------+-----------+--------+


.. tabs::

    .. group-tab:: Table

        The game is fully defined by the following game table.

        ======  =========  =========  =========  =========  ==========
        state   a_player0  a_player1  u_player0  u_player1  phi_state0
        ======  =========  =========  =========  =========  ==========
        delta                         0          0
        state0  cooperate  cooperate  2          2          0
        state0  cooperate  defect     0          3          0
        state0  defect     cooperate  3          0          0
        state0  defect     defect     1          1          0
        ======  =========  =========  =========  =========  ==========

        The game table specifies for each state and action profile
        the corresponding payoffs and state transitions.
        Additionally, the first row specifies the discount factors for each player.

        To import the game table, use the :py:meth:`SGame.from_table` method.

        .. code-block:: python

            import sgamesolver
            game = sgamesolver.SGame.from_table('path/to/table.xlsx')

    .. group-tab:: Arrays

        One-shot games can be conveniently defined using the
        :py:meth:`SGame.one_shot_game` method.

        .. code-block:: python

            import sgamesolver
            import numpy as np

            payoff_matrix = np.array([[[2, 0],
                                       [3, 1]],
                                      [[2, 3],
                                       [0, 1]]])

            game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

            # optional: overwrite action labels
            game.action_labels = ['cooperate', 'defect']

        The ``payoff_matrix`` should be an array of dimension *num_players + 1*,
        the first dimension indexing the player and
        the remaining dimensions indexing the strategy profile.
        Here, ``payoff_matrix`` has shape (2, 2, 2)
        with indices [player, action_0, action_1].
