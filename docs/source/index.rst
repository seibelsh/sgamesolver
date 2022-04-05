Welcome! This is the documentation for sGameSolver.
===================================================

**sGameSolver** - A homotopy-based solver for stochastic games.

First Steps
-----------

Installation
~~~~~~~~~~~~

To use sGameSolver, first install it into your preferred
Python environment using pip:

.. code-block:: console

   (.venv) $ pip install sgamesolver

Solving random game
~~~~~~~~~~~~~~~~~~~

To solve a random stochastic game, use

.. code-block:: python

   import dsgamesolver

   # step 1: define game
   game = dsgamesolver.SGame.random_game(num_states=5, num_players=3, num_actions=5, delta=0.95)

   # step 2: choose homotopy (here: Quantal Response Equilibrium)
   homotopy = dsgamesolver.homotopy.QRE(game=game)

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
   :maxdepth: 2
   :caption: Tutorial
   :name: tutorial

   defining_games
   choosing_homotopy
   solving_games

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Advanced Examples
   :name: advanced_examples

   qre_for_multiple_lambdas
   log_tracing_searching_prior_space
   starting_solver_at_equilibrium

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Homotopies
   :name: homotopies

   quantal_response_equilibrium
   logarithmic_tracing_procedure

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Solver
   :name: solver

   how_solver_works
   parameters
   troubleshooting

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Advanced Topics
   :name: advanced_topics

   cython
   symmetries
