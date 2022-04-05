Solving a 2x2 normal-form game
==============================

To define a one-shot game, use the
:py:meth:`SGame.one_shot_game` method.

To solve a specified :py:class:`SGame`, choose one of the
implemented :doc:`Homotopies </quantal_response_equilibrium>`
and apply the :py:meth:`.solve` method.

Simple example: |prisoners_dilemma_wiki|.

.. |prisoners_dilemma_wiki| raw:: html

   <a href="https://en.wikipedia.org/wiki/Prisoner%27s_dilemma" target="_blank">Prisoner's Dilemma</a>

.. table::

   +---------------+---------------+------------+
   |               | **cooperate** | **defect** |
   +---------------+---------------+------------+
   | **cooperate** | 2, 2          | 0, 3       |
   +---------------+---------------+------------+
   | **defect**    | 3, 0          | 1, 1       |
   +---------------+---------------+------------+

Both players defecting is the unique equilibrium.

.. code-block:: python

   import numpy as np
   import sgamesolver

   # prisoner's dilemma
   payoff_matrix = np.array([[[2, 0],
                              [3, 1]],
                             [[2, 3],
                              [0, 1]]])

   # payoff_matrix.shape = (2,2,2)
   # indices: [player, action_1, action_2]

   # define game
   game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

   # choose homotopy: quantal response equilibrium
   homotopy = sgamesolver.QRE(game=game)

   # solve
   homotopy.solver_setup()
   homotopy.solve()

   print(homotopy.equilibrium)

Output:

.. code-block:: console

   >>> +++++++ state0 +++++++
   >>> player0: v=1.00, s=[0.000 1.000]
   >>> player1: v=1.00, s=[0.000 1.000]

| Both players play the second action *defect* with probability one.
| Expected payoffs are 1.
