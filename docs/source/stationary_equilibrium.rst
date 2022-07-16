Stationary equilibrium
======================

A stationary equilibrium is a Nash equilibrium
in which players may condition their actions
only on the current state of the game,
not on past actions.

(Remark: If all states are *payoff-relevant*,
a stationary equilibrium is often also called Markov perfect equilibrium.)

More formally, a stationary strategy :math:`\sigma_i(s)` for player :math:`i`
is a function :math:`\sigma_i: S \rightarrow \Delta(A_{si})`
on the domain of states, mapping state :math:`s`
to a probability distribution :math:`\mathbb{P}`
over state-specific actions :math:`A_{si}`
such that :math:`\sigma_i(s,a_{si})=\mathbb{P}(a_{si}|s)`.
A stationary equilibrium is a Nash equilibrium in stationary strategies.

Due to Bellman's principle of optimality,
stationary equilibria admit a recursive representation.
A stationary strategy profile
:math:`\boldsymbol{\sigma}=(\sigma_{sia})_{s\in S,i\in I, a\in A_{si}}`
together with state-player values
:math:`\boldsymbol{V}=(V_{si})_{s\in S,i\in I}`
constitutes a stationary equilibrium if and only if

.. math:: \sigma_{si} \; \in \; \underset{\sigma_{si}\in\Delta(A_{si})}{\arg\max} \;\; V_{si}
.. math:: \text{s.t. } \quad V_{si} \; = \; u_{si}(\boldsymbol{\sigma}_s) + \delta_i \sum\limits_{s'\in S} \phi_{s\rightarrow s'}(\boldsymbol{\sigma}_s) \, V_{s'i}

for all states :math:`s\in S` and players :math:`i\in I`.

Finding a stationary equilibrium amounts to solving the above maximization
(which is generally difficult).
