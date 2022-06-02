How the solver works
====================

For any stochastic games, the necessary and sufficient conditions
for stationary equilibrium can be expressed as a
(potentially high-dimensional and nonlinear) system of equations.

sGameSolver relies on a solution method called
:ref:`homotopy continuation <homotopy_continuation>`
for the system of equations characterizing equilibrium.

Numerically, homotopy continuation is performed by a
:ref:`predictor-corrector procedure <predictor_corrector_procedure>`.

.. toctree::
    :hidden:

    how_solver_works_homotopy_continuation
    how_solver_works_predictor_corrector_procedure
    how_solver_works_references
