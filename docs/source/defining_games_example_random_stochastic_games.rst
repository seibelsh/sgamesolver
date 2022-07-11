Example: Random stochastic games
================================

To conveniently define a random stochastic game, use the
:py:meth`SGame.random_game` method.

1. Common discount factors and actions
--------------------------------------

.. code-block:: python

    import sgamesolver
    game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                         num_actions=4, delta=0.95, seed=42)

If ``num_actions`` is a single integer,
the same number of action is assumed for all players in all states.
Likewise, if ``delta`` is a single number,
it is interpreted as the common discount factor for all players.
Finally, passing a ``seed`` makes the random game replicable.

2. Randomized discount factors and actions
------------------------------------------

.. code-block:: python

    import sgamesolver
    game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                         num_actions=[3, 5], delta=[0.92, 0.98])

If ``num_actions`` or ``delta`` are lists/tuples of length two,
the two entries are understood as [min, max] values and
actions respectively discount factors are randomized from that range.

3. Specific individual discount factors and actions
---------------------------------------------------

.. code-block:: python

    import sgamesolver
    import numpy as np
    game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                         num_actions=np.array([[3, 4, 5],
                                                               [4, 5, 3]]),
                                         delta=[0.94, 0.95, 0.96])

If ``num_actions`` is an array of shape [num_states, num_players],
it specifies the number of actions for each state-player.
Likewise, if ``delta`` is an array of length num_players,
it specifies individual discount factors for each player.
