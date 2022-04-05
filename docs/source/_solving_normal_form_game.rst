Solving a 2x2 normal-form game
==============================

To define a one-shot game, use the
:py:meth:`SGame.one_shot_game` method.

To solve a specified :py:class:`SGame`, choose one of the
implemented :doc:`Homotopies </quantal_response_equilibrium>`
and apply the :py:meth:`.solve` method.

Simple example: |stag_hunt_wiki|.

.. |stag_hunt_wiki| raw:: html

   <a href="https://en.wikipedia.org/wiki/Stag_hunt" target="_blank">Stag Hunt</a>

.. table::

   +----------+----------+----------+
   |          | **Stag** | **Hare** |
   +----------+----------+----------+
   | **Stag** | 5, 5     | 0, 4     |
   +----------+----------+----------+
   | **Hare** | 4, 0     | 2, 2     |
   +----------+----------+----------+

There are three symmetric Nash equilibria in this game:
Two equilibria in pure strategies,
the payoff-dominant equilibrium (Stag, Stag)
and the risk-dominant equilibrium (Hare, Hare),
as well as a third equilibrium in mixed strategies.

sGameSolver can solve the game as follows.

.. code-block:: python

   import numpy as np
   import sgamesolver

   # stag hunt
   payoff_matrix = np.array([[[5, 0],
                              [4, 2]],
                             [[5, 4],
                              [0, 2]]])

   # payoff_matrix.shape = (2,2,2)
   # indices: [player, action_1, action_2]

   # define game
   game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

   # choose homotopy: quantal response equilibrium
   homotopy = sgamesolver.homotopy.QRE(game=game)

   # solve
   homotopy.solver_setup()
   homotopy.solve()

   print(homotopy.equilibrium)

Output:

.. code-block:: console

   >>> +++++++ state0 +++++++
   >>> player0: v= 2.00, s=[0.000 1.000]
   >>> player1: v= 2.00, s=[0.000 1.000]

Both players play the second action *Hare* with probability one,
expected payoffs are 2.
Hence, QRE selects the risk dominant equilibrium here.
