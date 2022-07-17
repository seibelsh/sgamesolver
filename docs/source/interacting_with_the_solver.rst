Interacting with the solver
===========================

This section introduces some ways to interact with the solver
which performs the numerical path tracking
via :doc:`predictor-corrector iterations <predictor_corrector_procedure>`.

The solver's basic usage is simple:
First, set up a game, choose a homotopy and,
if desired, make any last adjustments to the *homotopy* parameters:

.. code-block:: python

    import sgamesolver
    game = sgamesolver.SGame.random_game(3, 3, 3)
    homotopy = sgamesolver.homotopy.LogTracing(game)
    homotopy.eta = 0.1

Next, set up the solver by calling :py:meth:`~.solver_setup`:

.. code-block:: python

    homotopy.solver_setup()

:py:meth:`~.solver_setup` essentially does two things:
It computes the starting point ``y0``
(which is why you should fix homotopy parameters beforehand)
and it instantiates a solver,
an object of class :py:class:`HomContSolver`
which is responsible for the path tracking algorithm.
You can access it via the attribute :py:attr:`~.solver` of your homotopy:

>>> print(homotopy.solver)
<sgamesolver.homcont.HomContSolver object at 0x000001FC9481FDC0>

Now would be a good time to make adjustments to the
:doc:`solver parameters <solver_parameters>` if desired.
Then, it will ideally be sufficient to just let it run its course:

.. code-block:: python

    homotopy.solve()

However, there might be situations in which you'd like to
interact with the solver during the solution procedure.

Saving and loading the solver state
-----------------------------------

The state is updated at the end of each predictor-corrector step.
It essentially consists of

- ``y`` before the next predictor step
- current step size ``ds``
- some additional variables
  (orientation, total path length traveled, step number, consecutive successes)

Importantly, these quantities together completely determine future behavior:
Returning to a previous state and re-starting the solver
will reproduce the exact same results
(assuming no parameter changes, of course).

The solver state can be saved to a text file
using the method :py:meth:`~.save_file`:

>>> homotopy.solver.save_file('example.txt')
Current state saved as example.txt.

You can then always return to that solver state later
by invoking the method :py:meth:`~.load_file`:

>>> homotopy.solver.load_file('example.txt')
State successfully loaded from example.txt.

.. warning ::
    The solver state does **not** include (i) solver parameters or (ii) the
    game and homotopy parameters. If you want to restart from the saved state later on,
    you need to ensure that these can be recreated (e.g. by keeping the
    script that defined the game.)

Note that the created file is human readable and can be opened with any editor.
It contains a description field for comments or things to remember.

Storing the path
----------------

TBD
