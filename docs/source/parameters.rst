Solver parameters
=================

Setting parameters
------------------

Solver parameters can be changed either by setting the attribute directly, 
or by calling the method ``set_parameters`` of the solver, passing a set
of parameters as a dictionary or as keyword arguments. 

.. code-block:: python

    import sgamesolver
    game = sgamesolver.SGame.random_game(3, 3, 3)
    qre = sgamesolver.homotopy.QRE(game)
    qre.solver_setup()

    # directly set the attributes:
    qre.solver.verbose = 3
    qre.solver.ds_min = 1e-8
    qre.solver.max_steps = 1000

    # equivalently, call the method .set_parameters with kwargs:
    qre.solver.set_parameters(verbose=3, ds_min=1e-8, max_steps=1000)
    # ... or a dictionary as argument:
    parameters = {'verbose': 3, 'ds_min': 1e-8, 'max_steps': 1000}
    qre.solver.set_parameters(parameters)

Using ``set_parameters`` has the advantage that an error lets you know if 
invalid parameters were entered, e.g. due to a typo:

>>> qre.solver.set_parameters(versobe=3)
ValueError: "versobe" is not a valid parameter.

Default values for most parameters depend on the chosen homotopy -- they are stored as
attribute ``.default_parameters``. After setting up a homotopy, you can have a look at 
them as follows:

>>> print(qre.default_parameters)
{'convergence_tol': 1e-07,
 'corrector_tol': 1e-08,
 ...
}

There is a second set of parameters for each homotopy, ``.robust_parameters``,
which are chosen to be a bit slower, but potentially more stable. You can print them in 
the same way, or set all of them as follows:

>>> qre.solver.set_parameters(qre.robust_parameters)

General 
-------

verbose: int
    Determines how much information the solver displays during computation:

    :0: Silent; no reporting at all.
    :1: Current progress is reported continuously. This is the default.
    :2: In addition reports special occurrences, e.g. orientation reversals.
    :3: Further reports failed corrector loops; for parameter tuning or debugging.

max_steps: int
    Maximum number of predictor-corrector steps the solver will perform before
    reporting failure. (It is then possible to increase max_steps and continue.)


Convergence
-----------

The following two parameters are used to determine if a solution has been found 
and continuation is completed successfully:

t_target: float
    Value of the homotopy parameter t which the solver will attempt to reach.
convergence_tol: float
    Desired tolerance; used to check whether convergence is achieved.

Together, these govern the convergence criterion for the solver:

1. If ``t_target`` is finite, the solver will try to find a solution to H(x, t)=0 
   with \|t-t_target\| < convergence_tol.
   For example, in the logarithmic tracing
   homotopy, stationary equilibria are solutions at t=1, so that t_target defaults to 1 there. 
   This mode is also used to compute quantal response equilibria for 
   specific values of t (usually called λ in the context of QRE).   
2. If t_target is ``np.inf``, the solver will increase t without bounds, but
   continuously check whether *all other* variables x have converged. The criterion is then
   \|x_old - x_new\|/\|t_old - t_new\| < convergence_tol. This mode is used in QRE,
   where the homotopy path only asymptotically approaches an actual equilibrium.  

distance_function: callable, optional
    Distance function used for the convergence criterion if t_target is ``np.inf`` (see 2. above).
    For example, the QRE homotopy is implemented in logarithmized strategies,
    which diverge to `-\infty` as a strategy converges to 0. To account for this, 
    QRE uses a distance function which reverts the logarithmization for the convergence check.
    (distance_function is for specific use cases and probably nothing most users would want 
    to change.)


Corrector step
--------------

After each predictor step, a corrector step follows, which in turn consists of a 
sequence of Newton iterations, which are governed by the following parameters:

corrector_tol
    Convergence criterion for the corrector step: Iteration ends successfully once 
    H(y_corr) < corrector_tol.
corrector_steps_max: int
    Failure criterion for the corrector step: Maximum number of allowed iterations.
corrector_distance_max: float
    Failure criterion for the corrector step: 
    If for any iteration, \|y_new - y_old\| > corrector_distance_max * ds, the corrector
    step fails. 
corrector_ratio_max: float
    Failure criterion for the corrector step: 
    If for any iteration, \|y_new - y_old\|/\|y_old - y_old_old\| > corrector_ratio_max, the corrector
    step fails. Thus, a lower number requires faster convergence rates.

quasi_newton: bool
    If true (the default), corrector steps will be quasi-Newton: The Jacobian and its 
    inverse are only computed for the first iteration, and then re-used on all further iterations. 
    Otherwise, full Newton iterations are used, i.e. the Jacobian is evaluated at each iteration.
    (See Allgower and Georg for details.) Convergence rate is slower for quasi-Newton, so that
    more iterations are necessary; but usually, the decreased computational burden more than 
    compensates for that. 

bifurcation_angle_min: float
    Used to detect heuristically whether a bifurcation point is crossed and 
    a sign swap necessary.



Step size control
-----------------

ds_initial: float
    Step size that is set when the solver is set up.
ds_min : float
    Minimum step size.
ds_max : float
    Maximum step size.
ds_inflation_factor : float
    Factor used when step size is increased.
ds_deflation_factor : float
    Factor used when step size is decreased.
ds_inflation_min_consecutive_successes: int
    Step size is increased only if at least this many consecutive steps avoided a falling corrector
ds_inflation_max_corrector_steps: int
    If the corrector step is successful, but the required number of iterations
    exceeded this number, step size is kept constant rather than increased.


After a succesful predictor-corrector step, step size is increased, provided it is not 
already at ds_max and the criteria associated with the last 2 parameters are also met.
If a corrector fails, step size is decreased and the predictor-corrector step repeated.
If steps size is already at ds_min and the step fails, the solver will report failure instead.

Conservative values can increase solver stability -- especially in areas where the Jacobian 
is ill-conditioned (often near bifurcations, or where multiple paths are close to each other, 
where segment jumping might be a concern).
Of course, they also slow down progress. One way to go about this is to start rather aggressive 
and adjust in areas where problems are observed.


.. |br| raw:: html

      <br>
