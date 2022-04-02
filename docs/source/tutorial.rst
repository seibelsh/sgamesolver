Tutorial
========

Installation
------------

To use sGameSolver, first install it into your preferred
python environment using pip:

.. code-block:: console

   (.venv) $ pip install sgamesolver

Solving a 2x2 normal-form game
------------------------------

To define a one-shot game, use the
:py:meth:`SGame.one_shot_game` method.

The ``payoff_matrix`` should be array-like with
dimensions :math:`N \times A_1 \times \dots \times A_N`,
where :math:`N` denotes the number of players
and :math:`A_n` denotes the number of actions of player :math:`n=1,...,N`.

To solve a specified :py:class:`SGame`, choose one of the
implemented :doc:`homotopies` and apply the :py:meth:`.solve` method.

Simple example: |wiki_link|.

.. |wiki_link| raw:: html

   <a href="https://en.wikipedia.org/wiki/Prisoner%27s_dilemma" target="_blank">Prisoner's Dilemma</a>

| Two players, each with two actions: *cooperate* and *defect*.
| Both defecting is the unique equilibrium.

.. code-block:: python

   import numpy as np
   from sgamesolver import SGame
   from sgamesolver.homotopy import QRE

   # prisoner's dilemma
   payoff_matrix = np.array([[[-1, -3],
                              [ 0, -2]],
                             [[-1,  0],
                              [-3, -2]]])

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
