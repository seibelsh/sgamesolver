Quantal response equilibrium (QRE)
==================================

The idea of quantal response equilibrium is
to make stationary equilibrium "noisy".
In a quantal response equilibrium, players play fully mixed strategies and
the higher the long-term payoff associated with a given action,
the larger its probability in the strategy mix.

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


Mathematical formulation
------------------------

In the quantal response framework, first introduced by
`McKelvey and Palfrey (1995) <https://www.sciencedirect.com/science/article/pii/S0899825685710238>`_
and
`McKelvey and Palfrey (1998) <https://link.springer.com/article/10.1023/A:1009905800005>`_,
players are assumed to perceive payoffs only with some noise.
In the resulting **quantal response equilibrium**,
players' actions appear stochastic and
the probability of playing a particular strategy is related to its true payoff.
This idea can be generalized to stochastic games
by treating players in different states as independent.
For some particular noise distribution, logit quantal response emerges
and the resulting logit quantal response equilibrium
can be specified in closed from.

A stationary strategy profile
:math:`\boldsymbol{\sigma}=(\sigma_{sia})_{s\in S,i\in I, a\in A_{si}}`
together with state-player values
:math:`\boldsymbol{V}=(V_{si})_{s\in S,i\in I}`
constitutes a **logit Markov quantal response equilibrium** if and only if

.. math:: \sigma_{sia} = \frac{ \exp(\lambda\,U_{si}(\boldsymbol{\sigma}_{a,-i},\boldsymbol{V}_i)) }{ \sum\limits_{a'\in A_{si}} \exp(\lambda\,U_{sia'}(\boldsymbol{\sigma}_{a,-i},\boldsymbol{V}_i)) }
.. math:: V_{si} = U_{si}(\boldsymbol{\sigma}_{s},\boldsymbol{V}_{i})

where

.. math:: U_{sia}(\boldsymbol{\sigma}_{s,-i},\boldsymbol{V}_{i}) = u_{si}(a,\boldsymbol{\sigma}_{s,-i} + \delta_{i} \sum\limits_{s'\in S} \phi_{s\rightarrow s'} (a,\boldsymbol{\sigma}_{s,-i})\,V_{s'i})
.. math:: U_{si}(\boldsymbol{\sigma}_{s},\boldsymbol{V}_{i}) = u_{si}(a,\boldsymbol{\sigma}_{s} + \delta_{i} \sum\limits_{s'\in S} \phi_{s\rightarrow s'} (\boldsymbol{\sigma}_{s})\,V_{s'i})

The parameter :math:`\lambda\geq0` can be interpreted
as the **precision** of the perception of payoffs.
If :math:`\lambda=0`, the equilibrium is fully noisy
and mixing is uniform over actions.
If a quantal response equilibrium converges
as :math:`\lambda\rightarrow\infty`,
the limiting point is a stationary equilibrium.

The QRE homotopy (first introduced by
`Turocy (2005) <https://www.sciencedirect.com/science/article/pii/S0899825604000739>`_
and
`Turocy (2010) <https://link.springer.com/article/10.1007/s00199-009-0443-3>`_)
starts at :math:`\lambda=0` with the centroid strategy profile
and then lets :math:`\lambda\rightarrow\infty`.
Alternatively, sGameSolver can also compute QRE
for finite values of :math:`\lambda`,
see section :doc:`qre_for_multiple_lambdas`.

Further details on the construction of the QRE homotopy can be found in
`Eibelshäuser/Poensgen (2019) <https://dx.doi.org/10.2139/ssrn.3314404>`_.
