Example: Stag hunt
==================

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
3. and an unstable mixed equilibrium
   :math:`\bigl((\frac{2}{3},\frac{1}{3}),(\frac{2}{3},\frac{1}{3})\bigr)`
   in which both players play stag with probability :math:`\frac{2}{3}`
   and hare with probability :math:`\frac{1}{3}`.

The game can be implemented as follows.

.. tabs::

    .. group-tab:: Arrays

        .. code-block:: python

            import sgamesolver
            import numpy as np

            payoff_matrix = np.array([[[10, 1],
                                    [8, 5]],
                                    [[10, 8],
                                    [1, 5]]])
            game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)
            game.action_labels = ['stag', 'hare']

    .. group-tab:: Table

        ======  =========  =========  =========  =========  ==========
        state   a_player0  a_player1  u_player0  u_player1  phi_state0
        ======  =========  =========  =========  =========  ==========
        delta                         0          0
        state0  stag       stag       10         10         0
        state0  stag       hare       1          8          0
        state0  hare       stag       8          1          0
        state0  hare       hare       5          5          0
        ======  =========  =========  =========  =========  ==========

        .. code-block:: python

            import sgamesolver
            import numpy as np

            game = sgamesolver.SGame.from_table('path/to/table.xlsx')

Before searching the prior space,
we need set the number of searches
and initialize a container to keep track
of the equilibrium strategies found by the solver.

.. code-block:: python

    runs = 100
    strategies = np.zeros(shape=(runs, 4), dtype=np.float64)

Here, ``strategies`` is a 2D array with four columns,
corresponding to the probabiliy of player_0 playing stag,
the probability of player_0 playing hare,
the probability of player_1 playing stag
and the probability of player_1 playing hare, respectively.
Each row holds one strategy profile.

Random search
-------------

sGameSolver's logarithmic tracing homotopy class
:py:class:`sgamesolver.homotopy.LogTracing`
has the builtin option to set a random prior.

>>> homotopy = sgamesolver.homotopy.LogTracing(game, rho='random')

Alternatively, one can use the method
:py:meth:`sgamesolver.SGame.random_strategy` to generate a random prior,
which also allows to set a seed.

>>> rho = homotopy.game.random_strategy(seed=run)
>>> homotopy = sgamesolver.homotopy.LogTracing(game, rho=rho)

Performing the prior search, including a progress report,
can done as follows.

.. code-block:: python

    for run in range(runs):
        rho = homotopy.game.random_strategy(seed=run)
        homotopy = sgamesolver.homotopy.LogTracing(game, rho=rho)
        homotopy.solver_setup()
        homotopy.solver.verbose = 0  # make silent
        homotopy.solve()
        strategies[run] = homotopy.equilibrium.strategies[0].flatten().round(4)  # state 0

A quick look at the equilibrium strategies reveals that
the solver found the two equilibria in pure strategies,
(hare, hare) and (stag, stag).

>>> print(np.unique(strategies, axis=0))
[[0. 1. 0. 1.]
 [1. 0. 1. 0.]]

We can translate strategies into equilibrium labels

.. code-block:: python

    def get_eq(strat: np.ndarray) -> str:
        if np.allclose(strat, np.array([0, 1, 0, 1])):
            return 'hare'
        elif np.allclose(strat, np.array([1, 0, 1, 0])):
            return 'stag'
        elif np.allclose(np.array([2/3, 1/3, 2/3, 1/3])):
            return 'mixed'
        else:
            raise ValueError('unknown equilibrium')

    equilibria = np.array([get_eq(strat) for strat in strategies])

and illustrate the equilibrium counts in a bar plot:

.. code-block:: python

    import matplotlib.pyplot as plt

    eq_vals, counts = np.unique(equilibria, return_counts=True)
    pcts = 100 * counts / counts.sum()

    plt.bar(eq_vals, pcts)
    plt.xticks([0, 1, 2], ['(hare, hare)', '(stag, stag)', 'mixed'])
    plt.xlim(-0.6, 2.6)
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.show()

The resulting plot is shown in :numref:`stag_hunt_prior_search_random`.

.. _stag_hunt_prior_search_random:
.. figure:: img/stag_hunt_logtracing_search_priors_random.svg
    :width: 600
    :alt: stag hunt random prior search
    :align: center

    Histogram of equilibria in the stag hunt game, found by random prior search.


Systematic search
-----------------

As an alternative to random search,
one can also work through the prior space systematically.
For example, one can discretize the prior space
into an evently spaced grid
and let the solver run for every prior on the grid.

For the present stag hunt game,
priors are parameterized by two probabilities:
the probability :math:`p` for player_0 to play stag
and the probability :math:`q` for player_1 to play stag.
Let's consider the grid in which each probabilities is taken from
the set :math:`\{0, 0.1, ..., 0.9, 1\}`.
In this case, the above code needs to be adjusted as follows.

.. code-block:: python

    num_probs = 11
    probs = np.linspace(0, 1, num_probs)
    priors = np.array([[[[p, 1-p], [q, 1-q]]] for p in probs for q in probs])
    strategies = np.zeros(shape=(num_probs**2, 4), dtype=np.float64)

    for run, prior in enumerate(priors):
        homotopy = sgamesolver.homotopy.LogTracing(game, rho=prior)
        homotopy.solver_setup()
        homotopy.solver.verbose = 0  # make silent
        homotopy.solve()
        strategies[run] = homotopy.equilibrium.strategies[0].flatten().round(4)  # state 0

As expected, the result looks similar to the randomized prior search above,
see :numref:`stag_hunt_prior_search_systematic`.

.. _stag_hunt_prior_search_systematic:
.. figure:: img/stag_hunt_logtracing_search_priors_systematic.svg
    :width: 600
    :alt: stag hunt systematic prior search
    :align: center

    Histogram of equilibria in the stag hunt game, found by systematic prior search.
