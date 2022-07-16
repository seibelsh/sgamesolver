Homotopy method
===============

For any stochastic games, the necessary and sufficient conditions
for stationary equilibrium can be expressed as a
(potentially high-dimensional and nonlinear) system of equations.

sGameSolver relies on a solution method called
:doc:`homotopy continuation <homotopy_continuation>`
for the system of equations characterizing equilibrium.

Numerically, homotopy continuation is performed by a
:ref:`predictor-corrector procedure <predictor_corrector_procedure>`.

.. toctree::
    :hidden:

    homotopy_continuation
    predictor_corrector_procedure
