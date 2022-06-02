Welcome! This is the documentation for sGameSolver.
===================================================

**sGameSolver** - A homotopy-based solver for stochastic games.

Installation
------------

To use sGameSolver, first install it into your preferred
Python environment using pip:

.. code-block:: console

   (.venv) $ pip install sgamesolver

Solving a random game
---------------------

To solve a random stochastic game, use

.. code-block:: python

   import sgamesolver

   # step 1: define game (here: random game)
   game = sgamesolver.SGame.random_game(num_states=5, num_players=3, num_actions=5, delta=0.95)

   # step 2: choose homotopy (here: quantal response equilibrium)
   homotopy = sgamesolver.homotopy.QRE(game=game)

   # step 3: solve
   homotopy.solver_setup()
   homotopy.solve()

   print(homotopy.equilibrium)

Next Steps
----------

Get started with the :doc:`Tutorial <defining_games>`.

Find the project on `GitHub <https://github.com/seibelsh/sgamesolver>`_.


.. toctree::
   :hidden:
   :caption: Tutorial

   defining_games
   choosing_homotopy
   solving_games

.. toctree::
   :hidden:
   :caption: Advanced Examples

   qre_for_multiple_lambdas
   log_tracing_searching_prior_space
   starting_solver_at_equilibrium

.. toctree::
   :hidden:
   :caption: Homotopies

   quantal_response_equilibrium
   logarithmic_tracing_procedure

.. toctree::
   :hidden:
   :caption: Solver

   how_solver_works
   parameters
   troubleshooting

.. toctree::
   :hidden:
   :caption: Advanced Topics

   cython
   symmetries


.. toctree::
   :hidden:
   :caption: API Reference

   sgame
   sgame_homotopy
   hom_cont
   hom_path
