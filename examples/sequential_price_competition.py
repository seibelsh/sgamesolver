import sgamesolver
import numpy as np
import pandas as pd
import itertools
from examples._helpers import solve_game, assert_games_equal


# %% alternating moves: sequential price competition


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


# %% arrays


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

game = sgamesolver.SGame(payoff_matrices=payoff_matrices,
                         transition_matrices=transition_matrices,
                         discount_factors=common_discount_factor)

solve_game(game)

print(game.to_table())


# %% game table


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


game2 = sgamesolver.SGame.from_table(game_table)

assert_games_equal(game, game2)
