Stochastic games
================

A **stochastic game** is a sequence of normal-form games.
Each period, the corresponding normal-form game is characterized by a *state*.
At the beginning of a period, players learn the current state.
Afterwards, they interact and obtain payoffs accordingly.
The next state is then determined stochastically based on players' actions.
The procedure is repeated infinitely
(while including the possibility of terminal nodes).
All players seek to maximize the expected present values of
their payoff streams, choosing their actions to balance
instantaneous payoffs and favorable future states.

A stochastic game is characterized by:

- :math:`S`: finite set of states
- :math:`I`: finite set of players
- | :math:`A_{si}`: action set of player :math:`i` in state :math:`s`;
  | :math:`A_s=\times_{i\in I}A_{si}` denotes the set of action profiles
    in state :math:`s`
- :math:`\boldsymbol{u} = \bigl( u_{si}(\boldsymbol{a}_s) \bigr)_{\boldsymbol{a}_s \in \boldsymbol{A}_s, s \in S, i \in I}`:
  instantaneous payoff functions
  :math:`u_{s,i}: \boldsymbol{A}_s \rightarrow \mathbb{R}`
- | :math:`\boldsymbol{\phi} = \bigl( \phi_{s \rightarrow s'}(\boldsymbol{a}_s) \bigr)_{\boldsymbol{a}_s \in \boldsymbol{A}_s, s,s' \in S}`:
    state transition probabilities;
  | :math:`\phi_{s \rightarrow s'}(\boldsymbol{a}_s)` denotes the probability of
    transitioning from state :math:`s` to :math:`s'`
    if action profile :math:`\boldsymbol{a}_s` is played
- :math:`\boldsymbol{\delta} = \bigl( \delta_i \bigr)_{i \in I}`:
  discount factors for all players

Defining a stochastic game requires three inputs:
payoffs :math:`\boldsymbol{u}`, transitions :math:`\boldsymbol{\phi}`
and discount factors :math:`\boldsymbol{\delta}`
(their dimensions reveal states, players and actions).
