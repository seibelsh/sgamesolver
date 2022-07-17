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

Storing the state has two advantages:

(a) it allows to pause the computation,  e.g. to reboot, and restart, or to
    transfer to another machine without having to start from 
    the beginning again.
(b) It allows to start from the same position with different parameter sets, 
    in particular when trying to navigate through a difficult, badly 
    conditioned area.

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
    script that defined the game and set any parameters.)

Note that the created file is human readable and can be opened with any editor.
It contains a description field for comments or things to remember.

Storing the path
----------------

If path storing is enabled, the solver will keep a record
of past states (updated after each successful step). This
enables 

(a) to return to any of the previous states later on; for example
    to adjust parameters and start again from there, if a difficult
    spot is encountered.

(b) to later plot, analyze, or save the path the solver has taken. 
    This might be of interest in its own right (e.g. when anaylzing the
    QRE correpsondence of a game). It can also help with troubleshooting,
    as explained in SECTION.

Path storing has to be activated manually; this can be done any time 
after the solver has been set up:

.. code-block:: python

    import sgamesolver
    game = sgamesolver.SGame.random_game(8, 4, 4, seed=42)
    homotopy = sgamesolver.homotopy.LogTracing(game)
    homotopy.solver_setup()

    homotopy.solver.start_storing_path()


(By default, the solver path will store 1000 past states;
whenever that number has been reached, all but every 
10th are discarded, and recording resumes normally. To if you want to change
this number, use e.g.
 ``homotopy.solver.start_storing_path(num_steps=10000)`` )


Returning to a past step on the path
************************************

If path storing has been enabled, it is possible to return to past
steps via

.. code-block:: 

    # continues the example above
    homotopy.solver.max_steps = 200
    homotopy.solve()
    homotopy.solver.return_to_step(step_no = 123)

You could now change aparameters and call ``.solve()`` again to start
from this step. Note that you could also save this specific solver state for 
later use (see above) -- note that the path itself is not stored 
when doing that.

Plotting the path
*****************

The path can be plotted from the homotopy object
(which, unlike the solver, is aware of the meaning of the variables, 
thus can split the plot into states etc.):abbr:

.. code-block:: 

    # continues the example above
    homotopy.plot_path()

By default, this uses arc length s as x-axis; to use step number instead,
call ``.plot_path(x_axis="step")``. You can also zoom in, 
either on a specific range of s or range of step number:


.. code-block:: 

    # continues the example above
    homotopy.plot_path(s_range=(500,700))
    # or:
    homotopy.plot_path(step_range=(125,175))

