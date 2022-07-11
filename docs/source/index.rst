sGameSolver
===========
  
Stochastic Game Solver, short: **sGameSolver**, is a python package to compute 
stationary or Markov perfect equilibria of stochastic games, using the 
homotopy continuation method.

Some useful links:

- Source code is hosted on `GitHub <https://github.com/davidpoensgen/sgamesolver>`_.
- Also on GitHub is an `issue tracker <https://github.com/davidpoensgen/sgamesolver/issues>`_
  for bug reports and feature requests.
- Python package is hosted on `PyPI <https://pypi.org/project/sgamesolver>`_.

..
   - Documentation is found on `ReadTheDocs <https://sgamesolver.readthedocs.io>`_.

sGameSolver is free and open source, under the MIT license. 
If you use the program for any published research, please cite 
`Eibelshäuser/Poensgen (2019) <https://dx.doi.org/10.2139/ssrn.3316631>`_.

.. note::
   These docs are work in progress and currently under construction.

Installation
------------

sGameSolver is hosted on PyPI, so installation is usually as simple as

.. code-block:: console

   pip install sgamesolver

Usage
-----

Solving a stochastic game is done in three steps: 

1. Define a game.
2. Pick a homotopy function.
3. Set up and run the solver.

.. code-block:: python

   import sgamesolver
   game = sgamesolver.SGame.random_game(64, 2, 4, seed=42)
   qre = sgamesolver.homotopy.QRE(game)
   qre.solver_setup()
   qre.solve()
   print(qre.equilibrium)

A quick rundown of these steps:

1. Set up a stochastic game
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   game = sgamesolver.SGame.random_game(64, 2, 4, seed=42)

Stochastic games are represented by the class :py:class:`SGame`. 
For this quick example, we are using the method :py:meth:`random_game` to randomize
a game with 64 states, 2 players, and 4 actions per player and state.
(Setting a seed just makes the result reproducible.) 

Of course, you probably didn't come here to solve a random game, 
but have a specific game in mind.
Section :doc:`Defining games <defining_games>` contains instructions
and examples on how to create an :py:class:`SGame`
which represents the stochastic game you want to solve.
(By the way, sGameSolver can also solve normal form games, sequential games,
repeated games, and also finite Markov decision problems
– each of these is just a simple case of a stochastic game.)

2. Select and set up a homotopy function for your game
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   qre = sgamesolver.homotopy.QRE(game)

sGameSolver uses the **homotopy method** to solve stochastic games,
a general technique to solve systems of non-linear equations. 
In short, the idea is as follows:
Instead of solving some very hard problem directly
(in our case: finding an equilibrium),
a continuous transformation is applied to the system,
yielding a related, but much simpler problem, 
for which one can easily obtain a solution.
This transformation is then gradually reversed while tracking the solution,
until arriving at a solution for the original problem
– here, the desired stationary equilibrium. 
(You can find more background in section
:ref:`homotopy continuation <homotopy_continuation>`
– although such knowledge is not necessary for using the program.)

The (mathematical) function used for this transformation is called
**homotopy function**.
In general, there are many possibilities to construct a suitable one.
sGameSolver currently includes two: 
The one we picked for this example, :py:meth:`sgamesolver.homotopy.QRE`,
is based on an extension of quantal response equilibrium to stochastic games
(`Eibelshäuser/Poensgen 2019b <https://dx.doi.org/10.2139/ssrn.3314404>`_).
Some details can be found in section
:doc:`Quantal Response Equilibrium (QRE) <quantal_response_equilibrium>`.
The other, :py:meth:`sgamesolver.homotopy.LogTracing`, implements the 
logarithmic tracing procedure for stochastic games
(`Eibelshäuser/Klockmann/Poensgen/von Schenk 2022 <https://dx.doi.org/10.2139/ssrn.3748830>`_),
also see section
:doc:`Logarithmic Tracing Procedure <logarithmic_tracing_procedure>`.
Which one to pick? In our experience, the former is more robust
while the latter has the advantage that it
allows to search for multiple equilibria. 
More homotopy functions are to come!
In any case, please make sure to cite the paper that 
introduced whichever homotopy you end up using.

3. Let the homotopy solver do its job
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, we will set up the solver and start it:

.. code-block:: python

   qre.solver_setup()
   qre.solve()

Then it's time to lean back and watch for a bit:

.. code-block:: console

   ==================================================
   Start homotopy continuation
   Step    37: t =  3.612 ↑, s =  20.47, ds =  3.418

... until ...

.. code-block:: console

   Step   247: t = 1.147e+04 ↑, s = 9.385e+04, ds =  1000.
   Step   247: Continuation successful. Total time elapsed: 0:00:15
   End homotopy continuation
   ==================================================
   An equilibrium was found via homotopy continuation.

... success!

Ideally, the solver will be able to find a solution
without requiring any further interaction, as in this example.
In cases where this does not work out, check out the section
:doc:`Troubleshooting <troubleshooting>`.

4. Aftermath
~~~~~~~~~~~~

We can now display the solution:

.. code-block:: python

   print(qre.equilibrium)

which outputs equilibrium strategies and values for all 64 states:

.. code-block:: console

   +++++++++ state00 +++++++++
                            a0    a1    a2    a3  
   player0 : v=15.09, σ=[1.000 0.000 0.000 0.000]
   player1 : v=15.63, σ=[0.000 0.000 1.000 0.000]
   +++++++++ state01 +++++++++
                            a0    a1    a2    a3  
   player0 : v=14.76, σ=[0.000 0.961 0.000 0.039]
   player1 : v=15.61, σ=[0.354 0.000 0.000 0.646]
   +++++++++ state02 +++++++++
                            a0    a1    a2    a3  
   player0 : v=14.84, σ=[1.000 0.000 0.000 0.000]
   player1 : v=15.61, σ=[0.000 0.000 1.000 0.000]
   
   ... (abridged here for brevity) ...

   +++++++++ state63 +++++++++
                            a0    a1    a2    a3
   player0 : v=14.92, σ=[0.000 1.000 0.000 0.000]
   player1 : v=15.75, σ=[1.000 0.000 0.000 0.000]

Of course, you now also can access equilibrium strategies (and values) 
as NumPy arrays and use them for further calculations or simulations.

.. code-block:: python

   eq_strat = qre.equilibrium.strategies
   eq_values = qre.equilibrium.values

Next Steps
----------

Get started with the :doc:`Tutorial <defining_games>`.


.. toctree::
   :hidden:
   :caption: Tutorial

   installation
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
   :titlesonly:

   quantal_response_equilibrium
   logarithmic_tracing_procedure

.. toctree::
   :hidden:
   :caption: Solver

   how_solver_works
   interacting_with_the_solver
   parameters
   troubleshooting

..
   .. toctree::
      :hidden:
      :caption: Advanced Topics

      cython
      symmetries

..
   .. toctree::
      :hidden:
      :caption: API Reference

      sgame
      sgame_homotopy
      hom_cont
      hom_path
