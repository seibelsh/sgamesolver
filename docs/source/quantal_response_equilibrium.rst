Quantal Response Equilibrium (QRE)
==================================

In the quantal response framework, first introduced by McKelvey and Palfrey (1995, 1998),
players are assumed to perceive payoffs only with some noise.
In the resulting quantal response equilibrium, players' actions appear stochastic and
the probability of playing a particular strategy is related to its true payoff.
This idea can be generalized to stochastic games
by treating players in different states as independent.
For some particular noise distribution, logit quantal response emerges
and the resulting logit quantal response equilibrium can be specified in closed from.

A stationary strategy profile
:math:`\boldsymbol{\sigma}=(\sigma_{sia})_{s\in S,i\in I, a\in A_{si}}`
together with state-player values :math:`\boldsymbol{V}=(V_{si})_{s\in S,i\in I}`
constitutes a logit Markov quantal response equilibrium if and only if

.. math:: \sigma_{sia} = \frac{ \exp(\lambda\,U_{si}(\boldsymbol{\sigma}_{a,-i},\boldsymbol{V}_i)) }{ \sum\limits_{a'\in A_{si}} \exp(\lambda\,U_{sia'}(\boldsymbol{\sigma}_{a,-i},\boldsymbol{V}_i)) }
.. math:: V_{si} = U_{si}(\boldsymbol{\sigma}_{s},\boldsymbol{V}_{i})

where

.. math:: U_{sia}(\boldsymbol{\sigma}_{s,-i},\boldsymbol{V}_{i}) = u_{si}(a,\boldsymbol{\sigma}_{s,-i} + \delta_{i} \sum\limits_{s'\in S} \phi_{s\rightarrow s'} (a,\boldsymbol{\sigma}_{s,-i})\,V_{s'i})
.. math:: U_{si}(\boldsymbol{\sigma}_{s},\boldsymbol{V}_{i}) = u_{si}(a,\boldsymbol{\sigma}_{s} + \delta_{i} \sum\limits_{s'\in S} \phi_{s\rightarrow s'} (\boldsymbol{\sigma}_{s})\,V_{s'i})

The parameter :math:`\lambda\geq0` can be interpreted
as the precision of the perception of payoffs.
If :math:`\lambda=0`, the equilibrium is fully noisy and mixing is uniform over actions.
If a quantal response equilibrium converges as :math:`\lambda\rightarrow\infty`,
the limiting point is a stationary equilibrium.

The idea of the QRE homotopy (first introduced by Turocy (2005, 2010))
is to start at :math:`\lambda=0` with the centroid strategy profile
and then let :math:`\lambda\rightarrow\infty`.
Alternatively, sGameSolver can also compute QRE for finite values of :math:`\lambda`,
see section :doc:`qre_for_multiple_lambdas`.

Further details on the construction of the QRE homotopy can be found in
`Eibelshäuser/Poensgen (2019) <https://dx.doi.org/10.2139/ssrn.3314404>`_.

References
----------

Eibelshäuser, S. and D. Poensgen (2019):
*Markov Quantal Response Equilibrium and a Homotopy Method
for Computing and Selecting Markov Perfect Equilibria of Stochastic Games*.
https://dx.doi.org/10.2139/ssrn.3314404

McKelvey, R.D. and T.R. Palfrey (1995):
*Quantal Response Equilibria for Normal Form Games*,
Games and Economic Behavior, vol. 10, pp. 6-38.
https://www.sciencedirect.com/science/article/pii/S0899825685710238

McKelvey, R.D. and T.R. Palfrey (1998):
*Quantal Response Equilibria for Extensive Form Games*,
Experimental Economics, vol. 1, pp. 9-41.
https://link.springer.com/article/10.1023/A:1009905800005

Turocy, T.L. (2005):
*A Dynamic Homotopy Interpretation of the Logistic Quantal Response Equilibrium*,
Games and Economic Behavior, vol. 51, pp. 243-263.
https://www.sciencedirect.com/science/article/pii/S0899825604000739

Turocy, T.L. (2010):
*Computing Sequential Equilibria Using Agent Quantal Response Equilibria*,
Economic Theory, vol. 42, pp. 255-269.
https://link.springer.com/article/10.1007/s00199-009-0443-3
