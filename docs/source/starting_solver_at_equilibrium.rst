Starting the solver at some equilibrium
=======================================

Stochastic games often feature a vast multiplicity of stationary equilibria.
For almost all games, the number of equilibria is odd.
Typically, in terms of homotopy paths,
one equilibrium is connected to the unique starting point
while the remaining equilibria (an even number of them)
are pairwise connected by auxiliary paths.
This typical situation is depicted in :numref:`connected_equilibria`.

.. _connected_equilibria:
.. figure:: img/tikz-figure6.svg
    :width: 600
    :alt: connected equilibria
    :align: center

    Three equilibria: Equilibrium 1 is connected to the starting point,
    and equilibria 2 and 3 are connected to each other.

By default, sGameSolver traces out the equilibrium
connected to the starting point.
If some other equilibrium is known, however,
the solver can also start at this equilibrium
and follow the auxiliary path to the connected equilibrium.

Example: Stag hunt
------------------

Consider the following version of the stag hunt game.

+---------+------+--------+------+
|                | player1       |
+                +--------+------+
|                |  stag  | hare |
+---------+------+--------+------+
| player0 | stag | 10, 10 | 1, 8 |
+         +------+--------+------+
|         | hare |  8,  1 | 5, 5 |
+---------+------+--------+------+

This game has three equilibria, all symmetric:

1. the payoff-dominant equilibrium (stag, stag),
2. the risk-dominant equilibrium (hare, hare),
3. and a mixed equilibrium
   :math:`\bigl((\frac{2}{3},\frac{1}{3}),(\frac{2}{3},\frac{1}{3})\bigr)`
   in which both players play stag with probability :math:`\frac{2}{3}`
   and hare with probability :math:`\frac{1}{3}`.

The game can be implemented and solved
with the logarithmic tracing homotopy as follows.

.. code-block:: python

    import sgamesolver
    import numpy as np

    payoff_matrix = np.array([[[10, 1],
                               [8, 5]],
                              [[10, 8],
                               [1, 5]]])
    game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)
    game.action_labels = ['stag', 'hare']

    homotopy = sgamesolver.homotopy.LogTracing(game)
    homotopy.solver_setup()
    homotopy.solve()

sGameSolver finds the risk-dominant equilibrium (hare, hare) in this case.

>>> print(homotopy.equilibrium)
+++++++++ state0 +++++++++
                     stag  hare
player0 : v=5.00, σ=[0.000 1.000]
player1 : v=5.00, σ=[0.000 1.000]

Let's start at the mixed equilibrium.

>>> strategies = np.array([[[2/3, 1/3],
                            [2/3, 1/3]]])

Check if it's indeed an equilibrium.

>>> print(game.check_equilibrium(strategies))
[[8.8817842e-16, 0.0000000e+00]]

All close to zero, check.

Now let's find the corresponding values

>>> values = game.get_values(strategies)
>>> print(values)
array([[7., 7.]])

and construct a new starting point.

>>> y0 = homotopy.sigma_V_t_to_y(strategies, values, 1)
>>> print(homotopy.H(y0))
array([-8.88178420e-16,  0.00000000e+00, -1.77635684e-15, -8.88178420e-16,
       -5.55111512e-17, -5.55111512e-17])

Again all close to zero, check.

Finally, let's start the solver at the new starting point.

.. code-block:: python

    homotopy.solver_setup()
    homotopy.solver.y = y0
    homotopy.solver.sign *= -1  # going "backwards"
    homotopy.solve()

Indeed, the solver delivers the remaining equilibrium (stag, stag).

>>> print(homotopy.equilibrium)
+++++++++ state0 +++++++++
                      stag  hare
player0 : v=10.00, σ=[1.000 0.000]
player1 : v=10.00, σ=[1.000 0.000]
