Logarithmic tracing procedure
=============================

In the **linear tracing procedure**, first introduced by
`Harsanyi (1975) <https://link.springer.com/article/10.1007/BF01766187>`_
and
`Harsanyi/Selten (1988) <https://mitpress.mit.edu/books/general-theory-equilibrium-selection-games>`_
and later generalized to stochastic games by
`Herings/Peeters (2004) <https://dx.doi.org/10.2139/ssrn.357201>`_,
the game in question is augmented with a *set of prior beliefs*
about players' strategies as additional primitive.
The procedure then performs a gradual transformation
of these priors into equilibrium beliefs.
Specifically, a set of auxiliary games is defined
using a homotopy parameter :math:`t\in[0,1]`.
For :math:`t=0`, all players choose their optimal strategy in best response
only to the prior belief about what the other players play.
For :math:`t\in(0,1)`, players optimize against a convex combination
of prior and best responses of other players.
For :math:`t=1`, players optimize only against others' best responses,
beliefs are thus consistent and and equilibrium is reached.

The **logarithmic tracing procedure** applies the exact same logic,
but additionally features logarithmic penalty terms
which fade out as :math:`t\rightarrow1`.
For :math:`t\in[0,1)`, these penalty terms make it artificially costly
to play actions with zero probability,
leading to fully mixed best responses in the corresponding auxiliary games.

Consider an auxiliary game with prior beliefs
:math:`\boldsymbol{\rho}=(\rho_{sia})_{s\in S,i\in I, a\in A_{si}}`
and homotopy parameter :math:`t\in[0,1]`.
A stationary strategy profile
:math:`\boldsymbol{\sigma}=(\sigma_{sia})_{s\in S,i\in I, a\in A_{si}}`
together with state-player values
:math:`\boldsymbol{V}=(V_{si})_{s\in S,i\in I}`
constitutes a stationary equilibrium in the auxiliary game if and only if

.. math:: \sigma_{si} \; \in \; \underset{\sigma_{si}\in\Delta(A_{si})}{\arg\max} \;\; V_{si}
.. math:: \text{s.t. } \quad V_{si} \; = \; \bar{u}^t_{si}(\boldsymbol{\sigma}_s) + \delta_i \sum\limits_{s'\in S} \bar{\phi}^t_{s\rightarrow s'}(\boldsymbol{\sigma}_s) \, V_{s'i} + (1-t) \, \eta \sum\limits_{a\in A_{si}} \nu_{sia} \log(\sigma_{sia})

for all states :math:`s\in S` and players :math:`i\in I`, where

.. math:: \bar{u}^t_{si}(\boldsymbol{\sigma}_{s}) \; = \; t \, u_{si}(\boldsymbol{\sigma}_{si}, \boldsymbol{\sigma}_{s,-i}) + (1-t) \, u_{si}(\boldsymbol{\sigma}_{si}, \boldsymbol{\rho}_{s,-i})
.. math:: \bar{\phi}^t_{s\rightarrow s'}(\boldsymbol{\sigma}_{s}) \; = \; t \, \phi_{s\rightarrow s'}(\boldsymbol{\sigma}_{si}, \boldsymbol{\sigma}_{s,-i}) + (1-t) \, \phi_{s\rightarrow s'}(\boldsymbol{\sigma}_{si}, \boldsymbol{\rho}_{s,-i})

and where :math:`\eta>0` and
:math:`\boldsymbol{\nu}=(\nu_{sia})_{s\in S,i\in I, a\in A_{si}} > \boldsymbol{0}`
denote general and action-specific logarithmic penalty weights, respectively.
(In our experience, simply using :math:`\eta=0` and
:math:`\boldsymbol{\nu}=\boldsymbol{0}` works fine.)

The equilibrium found by the logarithmic tracing procedure
*crucially depends on the chosen prior belief* :math:`\boldsymbol{\rho}`.

- A natural choice for the prior is the **centroid** strategy profile
  (uniform mixing over available actions),
  which is also used in the original work by Harsanyi and Selten.
- Alternatively, depending on the application, a **specific** prior
  different from the centroid might be reasonable.
- Finally, sGameSolver also allows to use **random** strategy profiles
  as priors.

By using the procedure repeatedly with different prior beliefs,
one can potentially find **multiple different equilibria**.
If the prior space is searched systematically,
one can find all equilibria with a basin of attraction of given size,
see section :doc:`log_tracing_searching_prior_space`.

Further details on the construction of the logarithmic tracing homotopy can be found in
`Eibelshäuser/Klockmann/Poensgen/v.Schenk (2022) <https://dx.doi.org/10.2139/ssrn.3748830>`_.
