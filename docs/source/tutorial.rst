Tutorial
========

.. _installation:

Installation
------------

To use sGameSolver, first install it using pip:

.. code-block:: console

   $ pip install sgamesolver

Solving a 2x2 normal-form game
------------------------------

To define a one-shot game, use the
:py:func:`sgame.one_shot_game(payoff_matrix)` function:

The ``payoff_matrix`` parameter should be array-like with dimensions ...

For example: `Prisoner's Dilemma <https://en.wikipedia.org/wiki/Prisoner%27s_dilemma>`_

>>> import numpy as np

>>> from sgamesolver import SGame
>>> from sgamesolver.homotopy import QRE

>>> payoff_matrix = payoff_matrix = np.array([[[-1, -3],
                                               [ 0, -2]],
                                              [[-1,  0],
                                               [-3, -2]]])

>>> # define game
>>> game = SGame.one_shot_game(payoff_matrix=payoff_matrix)

>>> # choose homotopy: quantal response equilibrium
>>> homotopy = QRE(game=game)

>>> # solve
>>> homotopy.solver_setup()
>>> homotopy.solve()

>>> print(homotopy.equilibrium)
>>> +++++++ state0 +++++++
>>> player0: v=-2.00, s=[0.000 1.000]
>>> player1: v=-2.00, s=[0.000 1.000]
