Quantal Response Equilibrium (QRE)
==================================

The idea of quantal response equilibrium is to make stationary equilibrium "noisy".
In a quantal response equilibrium, players play fully mixed strategies and
the higher the long-term payoff associated with a given action,
the larger its probability.

The noisiness is governed by precision :math:`\lambda\in\mathbb{R}_0^+`
which also serves as homotopy parameter.
At :math:`\lambda=0`, precision is zero
and the quantal response equilibrium is fully noisy
in the sense that all available actions are played with the same probability
regardless of the associated payoffs.
The higher :math:`\lambda` the less noisy the equilibrium.
In the limit :math:`\lambda\rightarrow\infty`, precision becomes infinite
and a stationary equilibrium is obtained:
Only actions with the highest possible payoff are played
while the probability of playing inferior actions tends to zero.

For further details, see section :doc:`quantal_response_equilibrium`.

The QRE homotopy can be initialized through the class :py:class:`sgamesolver.homotopy.QRE`.
It is parameter-free and does not require additional primitives.
Specifying the QRE homotopy for a given ``game`` (see section :doc:`defining_games`)
amounts to

.. code-block::

    homotopy = sgamesolver.homotopy.QRE(game)
