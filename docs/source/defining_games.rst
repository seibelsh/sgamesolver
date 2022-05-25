Defining games
==============

For all subsequent code examples, the following imports are assumed.

.. code-block:: python

    import numpy as np
    import sgamesolver

Use the :py:class:`sGame` class to define any stochastic game.

.. code-block:: python

    game = sGame(payoff_matrices: List[np.ndarray],
                 transition_matrices: List[np.ndarray],
                 discount_factors: Union[np.ndarray, float, int])

The list ``payoff_matrices`` contains one payoff matrix for each state.
Each payoff matrix should be array-like with
dimensions :math:`N \times A_0 \times \dots \times A_{N-1}`,
where :math:`N` denotes the number of players
and :math:`A_n` denotes the number of actions of player :math:`n=0,...,N-1`.

The list ``transition_matrices`` contains one transition matrix for each state.
Each transition matrix should be array-like with
dimensions :math:`A_0 \times \dots \times A_{N-1} \times S`,
where the last dimension indexes the destination state and
:math:`S` denotes the number of states.

The argument ``discount_factors`` can either be common discount factor
:math:`\delta \in [0,1)` or array-like with dimension :math:`N`
containing one discount factor :math:`\delta_n \in [0,1)` per player.

Example 1: Random stochastic game
---------------------------------

TBC

Example 2: One-shot game
------------------------

A one-shot game (normal-form game) is a stochastic game with only one state
and full discounting (:math:`\delta=0`).

To define a one-shot game conveniently, use the
:py:meth:`SGame.one_shot_game` method.

The ``payoff_matrix`` should be array-like with


TBC

.. code-block:: python

    payoff_matrix = np.array([[[2, 0],
                           [3, 1]],
                          [[2, 3],
                           [0, 1]]])

# payoff_matrix.shape = (2,2,2)
# indices: [player, action_0, action_1]

# define game
game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

# choose homotopy: quantal response equilibrium
homotopy = sgamesolver.homotopy.QRE(game=game)

# solve
homotopy.solver_setup()
homotopy.solve()

Example 3: Repeated game
------------------------

TBC

Example 4: Markov decision problem
----------------------------------

TBC

Example 5: Stochastic game
--------------------------
