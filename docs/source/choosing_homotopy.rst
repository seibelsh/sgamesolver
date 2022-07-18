Choosing a homotopy
===================

After having defined the stochastic game of interest,
the next step is to choose a suitable homotopy.

In sGameSolver, the following homotopies are implemented:

1. :ref:`Quantal response equilibrium (QRE) <QRE>`
2. :ref:`Logarithmic tracing procedure <LogTracing>`


.. _QRE:

Quantal response equilibrium (QRE)
----------------------------------

For background information on the QRE homotopy,
see section :doc:`quantal_response_equilibrium`.

The QRE homotopy is parameter-free and
does not require additional primitives.
Importantly, it respects symmetries:
If the game is symmetric,
the QRE homotopy will only find symmetric equilibria,
never asymmetric ones.
In our experience, the QRE homotopy is numerically robust
and able to solve any game (that fits into working memory).

The QRE homotopy can be initialized through the class
:py:class:`sgamesolver.homotopy.QRE`.
Specifying the QRE homotopy for a given ``game`` of class
:py:class:`sgamesolver.SGame` (see section :doc:`defining_games`)
amounts to

.. code-block::

    homotopy = sgamesolver.homotopy.QRE(game)


.. _LogTracing:

Logarithmic tracing procedure
-----------------------------

For background information on the logarithmic tracing homotopy,
see section :doc:`logarithmic_tracing_procedure`.

The logarithmic tracing homotopy can be initialized through the class
:py:class:`sgamesolver.homotopy.LogTracing`.
It depends on three parameters:

1. prior beliefs :math:`\boldsymbol{\rho}=(\rho_{sia})_{s\in S,i\in I, a\in A_{si}}`
2. action-specific logarithmic penalty weights :math:`\boldsymbol{\nu}=(\nu_{sia})_{s\in S,i\in I, a\in A_{si}} > \boldsymbol{0}`
3. general logarithmic penalty weight :math:`\eta>0`

.. TODO: maybe a word on eta_fix

Unless specified otherwise,
the prior belief defaults to the centroid strategy profile
while all penalty weights are set to one.
In this case, specifying the logarithmic tracing homotopy
for a given ``game`` of class :py:class:`sgamesolver.SGame`
(see section :doc:`defining_games`) amounts to

.. code-block::

    homotopy = sgamesolver.homotopy.LogTracing(game)


Prior beliefs
*************

By default, the prior belief :math:`\boldsymbol{\rho}` is chosen to be
the centroid strategy profile.

.. code-block::

    homotopy = sgamesolver.homotopy.LogTracing(game, rho='centroid')

Alternatively, a (uniformly) random prior can be drawn at initialization.

.. code-block::

    homotopy = sgamesolver.homotopy.LogTracing(game, rho='random')

This is particularly helpful when searching the prior space
for different equilibria,
see section :doc:`log_tracing_searching_prior_space`.

Finally, a custom prior can be specified.
The prior must be submitted in the form of a 3-dimensional array
(with indices [state, player, action])
of the same shape as a strategy profile.
If the game in question features different numbers of actions
across states or players,
the action dimension must equal the largest number of actions
and nonexisting actions in other states must be submitted with value zero.

Let's take the
:doc:`dynamic version of Rock Paper Scissors <defining_games_example_simple_stochastic_game>`
again as an example.
Suppose we would like to start from the prior
that both players play rock in all three states.
This can be submitted as follows.

.. code-block::

    import numpy as np

    rho = np.array([  # state0
                    [[1, 0, 0],    # player0
                     [1, 0, 0]],   # player1
                      # state1
                    [[1, 0, 0],    # player0
                     [1, 0, 0]],   # player1
                      # state2
                    [[1, 0, 0],    # player0
                     [1, 0, 0]]])  # player1

    homotopy = sgamesolver.homotopy.LogTracing(game, rho=rho)


Logarithmic penalty weights
***************************

Even though the defaults
:math:`\boldsymbol{\nu}=\boldsymbol{1}` and :math:`\eta=1`
work very well in our experience,
users have the option to set different values.
Here is an example again for the
:doc:`dynamic version of Rock Paper Scissors <defining_games_example_simple_stochastic_game>`.

.. code-block::

    import numpy as np

    nu = np.array([  # state0
                   [[1, 2, 3],    # player0
                    [1, 2, 3]],   # player1
                     # state1
                   [[1, 2, 3],    # player0
                    [1, 2, 3]],   # player1
                     # state2
                   [[1, 2, 3],    # player0
                    [1, 2, 3]]])  # player1

    homotopy = sgamesolver.homotopy.LogTracing(game, nu=nu, eta=0.5)
