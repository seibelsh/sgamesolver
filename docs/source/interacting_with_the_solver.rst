Interacting with the solver
===========================

This section introduces some ways to interact 
with the solver which performs the numerical path tracking.
The basic usage is simple. First, set up a game, choose a homotopy and, if
desired, make any last adjustments to *homotopy* parameters:

>>> game = sgamesolver.SGame ...
>>> logtracing = sgamesolver.homotopy.LogTracing(game)
>>> logtracing.eta = 0.1

Next, set up the solver by calling ``.solver_setup``:

>>> logtracing.solver_setup()

``solver_setup`` essentially does 2 things: It computes the starting point ``y0`` 
(which is why you should fix homotopy parameters beforehand); and
it instantiates a solver, an object of class ``HomContSolver`` which is
responsible for the path tracking algorithm. You can access it via the 
attribute ``.solver`` of your homotopy:

>>> print(logtracing.solver)
<sgamesolver.homcont.HomContSolver object at 0x000001FC9481FDC0>

Now would be a good time to make adjustments to :doc:`parameters` if desired.
Then, it will ideally be sufficient to just let it run its course:

>>> logtracing.solve()

However, there might be situations in which you'd like to interact
with it during solution.

Saving and loading the solver state
-----------------------------------

The state is always updated at the end of each predictor-corrector step. 
it essentially consists of 

(a) ``y`` before the next predictor step
(b) current step size ``ds``
(c) some additional variables 
    (orientation, total path length traveled, step number, consecutive successes)

Importantly, these quantities together completely determine future behavior:
Returning to a previous state and re-starting the solver will reproduce the exact same results
(assuming no parameter changes, of course).

The solver state can be saved to a file using the method ``.save_file``:

>>> homotopy.solver.save_file("example.txt")
Current state saved as example.txt.

You can then always return to that state later:

>>> homotopy.solver.load_file("example.txt")
State successfully loaded from example.txt.

.. Warning ::
    The solver state does **not** include (i) solver parameters or (ii) the
    game and homotopy parameters. If you want to restart from the saved state later on,
    you need to ensure that these can be recreated (e.g. by keeping the
    script that defined the game.)

Note that the created file is human readable and can be opened with any editor.
It contains a description field for comments or things to remember.

Storing the path
----------------


