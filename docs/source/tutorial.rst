Tutorial
========

Installation
------------

To use sGameSolver, first install it into your preferred
Python environment using pip:

.. code-block:: console

   (.venv) $ pip install sgamesolver

Solving a 2x2 normal-form game
------------------------------

To define a one-shot game, use the
:py:meth:`SGame.one_shot_game` method.

To solve a specified :py:class:`SGame`, choose one of the
implemented :doc:`homotopies` and apply the :py:meth:`.solve` method.

Simple example: |wiki_link|.

.. |wiki_link| raw:: html

   <a href="https://en.wikipedia.org/wiki/Prisoner%27s_dilemma" target="_blank">Prisoner's Dilemma</a>

.. table::

   +---------------+---------------+------------+
   |               | **cooperate** | **defect** |
   +---------------+---------------+------------+
   | **cooperate** | -1, -1        | -3, 0      |
   +---------------+---------------+------------+
   | **defect**    |  0, -3        | -2, -2     |
   +---------------+---------------+------------+

Both players defecting is the unique equilibrium.

.. code-block:: python

   import numpy as np
   from sgamesolver import SGame
   from sgamesolver.homotopy import QRE

   # prisoner's dilemma
   payoff_matrix = np.array([[[-1, -3],
                              [ 0, -2]],
                             [[-1,  0],
                              [-3, -2]]])

   # payoff_matrix.shape = (2,2,2)
   # indices: [player, action_1, action_2]

   # define game
   game = SGame.one_shot_game(payoff_matrix=payoff_matrix)

   # choose homotopy: quantal response equilibrium
   homotopy = QRE(game=game)

   # solve
   homotopy.solver_setup()
   homotopy.solve()

   print(homotopy.equilibrium)

   >>> +++++++ state0 +++++++
   >>> player0: v=-2.00, s=[0.000 1.000]
   >>> player1: v=-2.00, s=[0.000 1.000]

| Both players play the second action *defect* with probability one.
| Expected payoffs are -2.
