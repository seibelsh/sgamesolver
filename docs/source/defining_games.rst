Defining games
==============

Stochastic games
----------------

A *stochastic game* is a sequence of normal-form games.
Each period, the corresponding normal-form game is characetrized by a *state*.
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

In sGameSolver, stochastic games can be defined using the
:py:class:`SGame` class.
Defining a stochastic game requires three inputs:
payoffs :math:`\boldsymbol{u}`, transitions :math:`\boldsymbol{\phi}`
and discount factors :math:`\boldsymbol{\delta}`
(their dimensions define states, players and actions).
These can either be submitted as arrays or as Excel-like tables.

Example 1: One-shot games
-------------------------

A one-shot game (normal-form game) is a stochastic game with only one state
and full discounting (:math:`\delta=0`).
Any one-shot game is fully specified by its payoff matrix.

A famous example is the Prisoner's Dilemma:

+---------+-----------+-----------+--------+
|                     | player1            |
+                     +-----------+--------+
|                     | cooperate | defect |
+---------+-----------+-----------+--------+
| player0 | cooperate | 2, 2      | 0, 3   |
+         +-----------+-----------+--------+
|         | defect    | 3, 0      | 1, 1   |
+---------+-----------+-----------+--------+

To define this one-shot game conveniently, use the
:py:meth:`SGame.one_shot_game` method.

.. code-block:: python

    import sgamesolver
    import numpy as np

    payoff_matrix = np.array([[[2, 0],
                               [3, 1]],
                              [[2, 3],
                               [0, 1]]])

    # payoff_matrix.shape = (2,2,2)
    # indices: [player, action_0, action_1]

    game = sgamesolver.SGame.one_shot_game(payoff_matrix=payoff_matrix)

    # optional: overwrite action labels
    game.action_labels = ['cooperate', 'defect']

The ``payoff_matrix`` should be an array of dimension *num_players + 1*,
the first dimension indexing the player and
the remaining dimensions indexing the strategy profile.

Alternatively, the game can be imported from a game table as follows.

.. code-block:: python

    import sgamesolver
    import numpy as np
    import pandas as pd

    game_table = pd.DataFrame(data=[['delta', '', '', 0, 0, np.nan],
                                    ['state0', 'cooperate', 'cooperate', 2, 2, 0],
                                    ['state0', 'cooperate', 'defect', 0, 3, 0],
                                    ['state0', 'defect', 'cooperate', 3, 0, 0],
                                    ['state0', 'defect', 'defect', 1, 1, 0]],
                              columns=['state', 'a_player0', 'a_player1',
                                       'u_player0', 'u_player1', 'phi_state0'])

    game = sgamesolver.SGame.from_table(table=game_table)

The game table specifies for each state and action profile
the corresponding payoffs and state transitions.
Additionally, the first row specifies the discount factors for each player.

======  =========  =========  =========  =========  ==========
state   a_player0  a_player1  u_player0  u_player1  phi_state0
======  =========  =========  =========  =========  ==========
delta                         0          0
state0  cooperate  cooperate  2          2          0
state0  cooperate  defect     0          3          0
state0  defect     cooperate  3          0          0
state0  defect     defect     1          1          0
======  =========  =========  =========  =========  ==========

Even more conveniently, the game table can also be provided as an
xlsx, xls, csv, txt, or dta file.
To import a game table, use the :py:meth:`SGame.from_table` method.

.. code-block:: python

    import sgamesolver

    game = sgamesolver.SGame.from_table('path/to/table.xlsx')

Example 2: Random stochastic games
----------------------------------

To conveniently define a random stochastic game, use the
:py:meth:`SGame.random_game` method.

.. code-block:: python

    import sgamesolver

    game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                         num_actions=4, delta=0.95, seed=42)

If ``num_actions`` is a single integer,
the same number of action is assumed for all players in all states.
Likewise, if ``delta`` is a single number,
it is interpreted as the common discount factor for all players.
Finally, passing a ``seed`` makes the random game replicable.

If ``num_actions`` or ``delta`` are lists/tuples of length two,
the two entries are understood as [min, max] values and
actions respectively discount factors are randomized from that range.

.. code-block:: python

    import sgamesolver

    game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                         num_actions=[3, 5], delta=[0.92, 0.98])

If ``num_actions`` is an array of shape [num_states, num_players],
it specifies the number of actions for each state-player.
Likewise, if ``delta`` is an array of length num_players,
it specifies individual discount factors for each player.

.. code-block:: python

    import sgamesolver
    import numpy as np

    game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                         num_actions=np.array([[3, 4, 5],
                                                               [4, 5, 3]]),
                                         delta=[0.94, 0.95, 0.96])

Example 3: Stochastic games
---------------------------

Consider the following dynamic variation of Rock Paper Scissors.
Two players play Rock Paper Scissors repeatedly and incorporate "scissor loading".
Having solely played scissors in the previous round (while the opponent has not)
wins a tie on scissors in the next round.
If both players have played scissors,
neither of them gets the tie-breaking scissors advantage.

The dynamic variation of Rock Paper Scissors features three states:

.. math:: s \in \begin{cases} 0 & \text{neutral state} \\ 1 & \text{player 0 has loaded scissors} \\ 2 & \text{player 1 has loaded scissors} \end{cases}

The corresponding payoffs are given by

+---------+----------+--------+-------+-------------+
|                    | player1                      |
+                    +--------+-------+-------------+
|                    | rock   | paper | scissors    |
+---------+----------+--------+-------+-------------+
| player0 | rock     | 0, 0   | -1, 1 | 1, -1       |
+         +----------+--------+-------+-------------+
|         | paper    | 1, -1  | 0, 0  | -1, 1       |
+         +----------+--------+-------+-------------+
|         | scissors | -1, 1  | 1, -1 | X(s), -X(s) |
+---------+----------+--------+-------+-------------+

with

.. math:: X(s) = \begin{cases} 0 & \text{if } s=0 \\ 1 & \text{if } s=1 \\ -1 & \text{if } s=2 \end{cases}

This game can be defined by submitting payoffs, transitions
and discount factors to :py:class:`SGame`.

.. code-block:: python

    import sgamesolver
    import numpy as np

    payoff_matrices = [  # state0:
                       np.array([[[0, -1,  1],
                                  [1,  0, -1],
                                  [-1, 1,  0]],
                                 [[0,  1, -1],
                                  [-1, 0,  1],
                                  [1, -1,  0]]]),
                         # state1:
                       np.array([[[0, -1,  1],
                                  [1,  0, -1],
                                  [-1, 1,  1]],    # player0 wins tie on Scissors
                                 [[0,  1, -1],
                                  [-1, 0,  1],
                                  [1, -1, -1]]]),  # player1 loses tie on Scissors
                         # state2:
                       np.array([[[0, -1,  1],
                                  [1,  0, -1],
                                  [-1, 1, -1]],    # player0 loses tie on Scissors
                                 [[0,  1, -1],
                                  [-1, 0,  1],
                                  [1, -1,  1]]])]  # player1 wins tie on Scissors

    # transitions identical for each state
    transition_matrices = [np.array([[[1, 0, 0],
                                      [1, 0, 0],
                                      [0, 0, 1]],
                                     [[1, 0, 0],
                                      [1, 0, 0],
                                      [0, 0, 1]],
                                     [[0, 1, 0],
                                      [0, 1, 0],
                                      [1, 0, 0]]])] * 3

    common_discount_factor = 0.95

    game = sgamesolver.SGame(payoff_matrices=payoff_matrices,
                             transition_matrices=transition_matrices,
                             discount_factors=common_discount_factor)

    # optional: overwrite action labels
    game.action_labels = ['rock', 'paper', 'scissors']

The list ``payoff_matrices`` contains one payoff matrix for each state.
Each payoff matrix is a numpy array with dimensions
:math:`I \times A_0 \times \dots \times A_{I}`,
where the first dimension indexes the player and
:math:`A_i` denotes the number of actions of player :math:`i`.

The list ``transition_matrices`` contains one transition matrix for each state.
Each transition matrix is a numpy array with dimensions
:math:`A_0 \times \dots \times A_2 \times S`,
where the last dimension indexes the destination state.

The argument ``discount_factors`` can either be common discount factor
:math:`\delta \in [0,1)` or an array with dimension :math:`I`
containing one discount factor :math:`\delta_i \in [0,1)`
for each player :math:`i`.
Here, a common discount factor is chosen.

As an alternative to submitting arrays for payoffs, transitions and
discount factors, a game table can be provided.

=======  =========  =========  =========  =========  ===========  ==========  ==========
state    a_p0       a_p1       u_p0       u_p1       phi_neutral  phi_adv_p0  phi_adv_p1
=======  =========  =========  =========  =========  ===========  ==========  ==========
delta                          0.95       0.95
neutral  rock       rock       0          0          1            0           0
neutral  rock       paper      -1         1          1            0           0
neutral  rock       scissors   1          -1         0            0           1
neutral  paper      rock       1          -1         1            0           0
neutral  paper      paper      0          0          1            0           0
neutral  paper      scissors   -1         1          0            0           1
neutral  scissors   rock       -1         1          0            1           0
neutral  scissors   paper      1          -1         0            1           0
neutral  scissors   scissors   0          0          1            0           0
adv_p0   rock       rock       0          0          1            0           0
adv_p0   rock       paper      -1         1          1            0           0
adv_p0   rock       scissors   1          -1         0            0           1
adv_p0   paper      rock       1          -1         1            0           0
adv_p0   paper      paper      0          0          1            0           0
adv_p0   paper      scissors   -1         1          0            0           1
adv_p0   scissors   rock       -1         1          0            1           0
adv_p0   scissors   paper      1          -1         0            1           0
adv_p0   scissors   scissors   1          -1         1            0           0
adv_p1   rock       rock       0          0          1            0           0
adv_p1   rock       paper      -1         1          1            0           0
adv_p1   rock       scissors   1          -1         0            0           1
adv_p1   paper      rock       1          -1         1            0           0
adv_p1   paper      paper      0          0          1            0           0
adv_p1   paper      scissors   -1         1          0            0           1
adv_p1   scissors   rock       -1         1          0            1           0
adv_p1   scissors   paper      1          -1         0            1           0
adv_p1   scissors   scissors   -1         1          1            0           0
=======  =========  =========  =========  =========  ===========  ==========  ==========

Here, the players have been named *p0* and *p1*,
states are named *neutral*, *adv_p0* and *adv_p1*,
and actions are labeled *rock*, *paper* and *scissors*.

To import the game table, use the :py:meth:`SGame.from_table` method.

.. code-block:: python

    import sgamesolver

    game = sgamesolver.SGame.from_table('path/to/table.xlsx')

Example 4: Stochastic games with sequential moves
-------------------------------------------------

sGameSolver allows for stochastic games with different actions
across states and players.
An extreme case of differing actions across states are stochastic games
with sequential moves.
In such games, only one of the players can move in any given state,
while the remaining players have only one action, namely do nothing.

A famous example of a stochastic game with sequential moves is the
price competition game by Maskin and Tirole (1988).

There are two firms,
each producing a homogeneous product at zero marginal cost.
The two firms compete on price to maximize the net present value
of profits given a common discount factor.
Time runs in discrete periods and firms take turns to set their prices.
In odd periods, firm 1 sets its price and firm 2's price is locked in,
and vice versa in even periods.
Each period, firms face market demand :math:`d(p) = 2 - p`
which goes to the firm with the lowest price.
In case of equal prices, demand is split evenly.
Finally, firms choose prices from a grid
:math:`P = \{0.0, 0.1, ..., 1.0, 1.1\}`.

A state :math:`s` in this game is a tuple :math:`s = (i, p_{-i})`
consisting of the firm :math:`i` next to set its price
and the price :math:`p_{-i}` currently locked in by the other firm.

Actions are state-dependent: Firm :math:`i` currently moving
can choose any price from the grid while the other firm :math:`-i`
has no choice but to stick to its price.

Finally, state transitions are given by price choices.
If firm :math:`i` in state :math:`s = (i, p_{-i})` chooses price :math:`p_i`,
the next state will be :math:`s' = (-i, p_i)` with the other firm :math:`-i`
reacting to the price :math:`p_i` of firm :math:`i`.

The game can be implemented in sGameSolver as follows.

.. code-block:: python

    import sgamesolver
    import numpy as np
    import itertools

    num_players = 2     # number of firms
    MC = 0              # marginal costs

    # price grid
    p_min = 0
    p_step = 0.1
    p_max = 1 + p_step
    num_prices = int(1 + (p_max-p_min) / p_step)
    P = np.linspace(p_min, p_max, num_prices)

    # demand function
    def d(p):
        return 2-p

    # profit function
    def Pi(p):
        # number of firms at minimum price, market shares and demand
        N = (p == p.min()).sum()
        shares = [1/N if p_i == p.min() else 0 for p_i in p]
        D = np.array([shares[i] * d(p_i) for i, p_i in enumerate(p)])
        return (p - MC) * D

    # state space [(player_to_move, competitor_prices)]
    states = []
    for i in range(num_players):
        for a_not_i in itertools.product(
                range(num_prices), repeat=num_players-1):
            states.append((i, np.array(a_not_i)))
    num_states = len(states)
    stateIDs = np.arange(num_states)
    state_dict = dict(zip(stateIDs, states))

    # functions for convenience
    def get_state(stateID):
        return state_dict[stateID]

    def get_stateID(state):
        for s, state_ in state_dict.items():
            if state_ == state:
                return s
        return None

    def payoff_matrix(s):
        i, a_not_i = get_state(s)
        # dimensions of action profile a in state s
        #   player i can choose a price
        #   other players have only one dummy action
        a_dims = np.ones(num_players, dtype=np.int32)
        a_dims[i] = len(P)
        a_dims = tuple(a_dims)
        matrix = np.nan * np.ones((num_players,) + a_dims)
        for j in range(num_players):
            for a_profile in np.ndindex(a_dims):
                # insert action of player i into action profile
                a = np.insert(a_not_i, i, a_profile[i])
                prices = P[a]
                matrix[(j,)+a_profile] = Pi(prices)[j]
        return matrix

    # vector of transition probabilities given action profile
    def transition_probs(s, a_profile):
        i, a_not_i = get_state(s)
        a = np.insert(a_not_i, i, a_profile[i])
        i_next = (i + 1) % num_players
        a_not_i_next = np.delete(a, i_next)
        s_next = get_stateID((i_next, a_not_i_next))
        probs = np.zeros(num_states)
        probs[s_next] = 1
        return probs

    # full transition matrix
    def transition_matrix(s):
        i, a_not_i = get_state(s)
        a_dims = np.ones(num_players, dtype=np.int32)
        a_dims[i] = num_prices
        a_dims = tuple(a_dims)
        matrix = np.nan * np.ones(a_dims + (num_states,))
        for a in np.ndindex(a_dims):
            matrix[a] = transition_probs(s, a)
        return matrix

    payoff_matrices = [payoff_matrix(s) for s in range(num_states)]
    transition_matrices = [transition_matrix(s) for s in range(num_states)]
    common_discount_factor = 0.95

    game = sgamesolver.SGame(payoff_matrices=payoff_matrices,
                            transition_matrices=transition_matrices,
                            discount_factors=common_discount_factor)


References
----------

Maskin, Eric, and Jean Tirole (1988):
"A Theory of Dynamic Oligopoly, II: Price Competition, Kinked Demand Curves, and Edgeworth Cycles.",
*Econometrica*, 56.3, 571-599.
