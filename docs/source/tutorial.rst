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
``sgame.one_shot_game(payoff_matrix)`` function:

The ``payoff_matrix`` parameter should be array-like with dimensions ...

For example:

>>> import numpy as np
>>> from sgamesolver import sgame
>>> payoff_matrix = np.array([[...]])
>>> my_game = sgame.one_shot_game(payoff_matrix)

TBC
