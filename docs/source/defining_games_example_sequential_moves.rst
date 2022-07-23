Example: Stochastic game with sequential moves
==============================================

sGameSolver allows for stochastic games with different actions
across states and players.
An extreme case of differing actions across states are stochastic games
with sequential moves.
In such games, only one of the players can move in any given state,
while the remaining players have only one action, namely do nothing.

A famous example of a stochastic game with sequential moves is
the price competition game by
`Maskin and Tirole (1988) <https://www.jstor.org/stable/1911701>`_.

There are two firms,
each producing a homogeneous product at zero marginal cost.
The two firms compete on price to maximize the net present value
of profits given a common discount factor.
Time runs in discrete periods and firms take turns to set their prices.
In odd periods, firm 0 sets its price and firm 1's price is locked in,
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

Some preparation:

.. code-block:: python

    import numpy as np
    import itertools

    NUM_PLAYERS = 2
    MARGINAL_COSTS = 0
    PRICE_GRID = np.linspace(0, 1.1, 12)

    def demand_fun(price: float) -> float:
        return 2 - price

    def profit_fun(prices: np.ndarray) -> np.ndarray:
        # number of firms at minimum price, market shares and demand
        num_players_at_min_price = (prices == prices.min()).sum()
        market_shares = [1/num_players_at_min_price if price == prices.min() else 0 for price in prices]
        demand = np.array([market_shares[player] * demand_fun(price) for player, price in enumerate(prices)])
        return (prices - MARGINAL_COSTS) * demand

    # state space [(player_to_move, competitor_prices)]
    state_space: list[tuple[int, np.ndarray]] = []
    for player in range(NUM_PLAYERS):
        for other_prices in itertools.product(PRICE_GRID, repeat=NUM_PLAYERS - 1):
            state_space.append((player, np.array(other_prices)))

    def get_prices(state: tuple[int, np.ndarray], price: float) -> np.ndarray:
        player, other_prices = state
        return np.insert(other_prices, player, price)

    def get_next_state(state: tuple[int, np.ndarray], price: float) -> np.ndarray:
        player, other_prices = state
        prices = get_prices(state, price)
        next_player = (player + 1) % NUM_PLAYERS
        next_other_prices = np.delete(prices, next_player)
        return (next_player, next_other_prices)

Now we can define a game table or the corresponding arrays.

.. tabs::

    .. group-tab:: Table

        The full game table has 289 rows.
        We abbreviate it here.

        ========  =========  =========  =========  =========  ========
        state     a_player0  a_player1  u_player0  u_player1  to_state
        ========  =========  =========  =========  =========  ========
        delta                           0          0
        (0, 0)    0          0          0          0          (1, 0)
        (0, 0)    0.1        0          0          0          (1, 0.1)
        ...       ...        0          0          0          ...
        (0, 0)    1.1        0          0          0          (1, 1.1)
        (0, 0.1)  0          0.1        0          0          (1, 0)
        (0, 0.1)  0.1        0.1        0.95       0.95       (1, 0.1)
        ...       ...        0.1        0          0.19        ...
        (0, 0.1)  1.1        0.1        0          0.19       (1, 1.1)
        ...       ...        ...        ...        ...        ...
        (0, 1.1)  0          1.1        0          0          (1, 0)
        (0, 1.1)  0.1        1.1        0.19       0          (1, 0.1)
        ...       ...        1.1        ...        ...        ...
        (0, 1.1)  1.1        1.1        0.495      0.495      (1, 1.1)
        (1, 0)    0          0          0          0          (0, 0)
        (1, 0)    0          0.1        0          0          (0, 0.1)
        ...       0          ...        0          0          ...
        (1, 0)    0          1.1        0          0          (0, 1.1)
        (1, 0.1)  0.1        0          0          0          (0, 0)
        (1, 0.1)  0.1        0.1        0.95       0.95       (0, 0.1)
        ...       0.1        ...        0.19       0          ...
        (1, 0.1)  0.1        1.1        0.19       0          (0, 1.1)
        ...       ...        ...        ...        ...        ...
        (1, 1.1)  1.1        0          0          0          (0, 0)
        (1, 1.1)  1.1        0.1        0          0.19       (0, 0.1)
        ...       1.1        ...        ...        ...        ...
        (1, 1.1)  1.1        1.1        0.495      0.495      (0, 1.1)
        ========  =========  =========  =========  =========  ========

        The game table can be generated in Python as follows.

        .. code-block:: python

            import pandas as pd

            common_discount_factor = 0.95
            game_table = pd.DataFrame(data=[['delta'] + ['']*NUM_PLAYERS + [common_discount_factor]*NUM_PLAYERS + [np.nan]],
                                      columns=['state', 'a_p0', 'a_p1', 'u_p0', 'u_p1', 'to_state'])

            for state in state_space:
                player, other_prices = state

                for price in PRICE_GRID:
                    prices = get_prices(state, price)
                    payoffs = profit_fun(prices)
                    next_state = get_next_state(state, price)

                    new_row = pd.DataFrame(data=[[str(state)] + [str(p) for p in prices] + list(payoffs) + [str(next_state)]],
                                           columns=['state', 'a_p0', 'a_p1', 'u_p0', 'u_p1', 'to_state'])

                    game_table = pd.concat([game_table, new_row], ignore_index=True)

        As always, the game table can be imported by calling :py:meth:`~.SGame.from_table`:

        .. code-block:: python

            import sgamesolver

            # import Pandas DataFrame:
            game = sgamesolver.SGame.from_table(game_table)
            # or Excel file:
            game = sgamesolver.SGame.from_table('path/to/table.xlsx')

    .. group-tab:: Arrays

        .. code-block:: python

            def make_payoff_matrix(state: tuple[int, np.ndarray]) -> np.ndarray:
                player, other_prices = state

                # player can choose a price, other players have only one dummy action
                a_dims = np.ones(NUM_PLAYERS, dtype=np.int32)
                a_dims[player] = len(PRICE_GRID)
                payoff_matrix = np.nan * np.ones((NUM_PLAYERS,) + tuple(a_dims))

                for idx, price in enumerate(PRICE_GRID):
                    prices = get_prices(state, price)
                    payoffs = profit_fun(prices)

                    action_profile = np.zeros(NUM_PLAYERS, dtype=np.int32)
                    action_profile[player] = idx

                    for p in range(NUM_PLAYERS):
                        payoff_matrix[(p,) + tuple(action_profile)] = payoffs[p]

                return payoff_matrix


            def make_transition_matrix(state: tuple[int, np.ndarray]) -> np.ndarray:
                player, other_prices = state

                a_dims = np.ones(NUM_PLAYERS, dtype=np.int32)
                a_dims[player] = len(PRICE_GRID)
                transition_matrix = np.zeros(tuple(a_dims) + (len(state_space),))

                for idx, price in enumerate(PRICE_GRID):
                    next_state = get_next_state(state, price)
                    transition_probs = [1 if s == next_state else 0 for s in state_space]

                    action_profile = np.zeros(NUM_PLAYERS, dtype=np.int32)
                    action_profile[player] = idx

                    for s in range(len(state_space)):
                        transition_matrix[tuple(action_profile) + (s,)] = transition_probs[s]

                return transition_matrix


            payoff_matrices = [make_payoff_matrix(state) for state in state_space]
            transition_matrices = [make_transition_matrix(state) for state in state_space]
            common_discount_factor = 0.95

        The :py:class:`~.SGame` class can then be initialized as usual:

        .. code-block:: python

            import sgamesolver

            game = sgamesolver.SGame(payoff_matrices=payoff_matrices,
                                     transition_matrices=transition_matrices,
                                     discount_factors=common_discount_factor)
