import sgamesolver
import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import gridspec
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


# %% log tracing: searching prior space


runs = 100
strategies = np.zeros(shape=(runs, 24, 2, 12), dtype=np.float64)

for run in range(runs):
    rho = game.random_strategy(seed=run)
    rho[np.isnan(rho)] = 0  # prior: transform NaN to 0
    homotopy = sgamesolver.homotopy.LogTracing(game, rho=rho)
    homotopy.solver_setup()
    homotopy.solver.verbose = 0  # make silent
    homotopy.solve()
    strategies[run] = homotopy.equilibrium.strategies.round(4)
    print(f"done run {run+1}/{runs}")


num_states = 24
num_players = 2
num_actions = 12
marginal_costs = 0
price_grid = np.linspace(0, 1.1, 12)

states = [(player_to_move, np.array(A_j))
          for player_to_move in np.arange(num_players)
          for A_j in itertools.product(np.arange(num_actions), repeat=num_players-1)]


def get_stateID(state): 
    for k in range(num_states):
        if states[k][0] == state[0] and (states[k][1] == state[1]).all():
            return k
    return np.nan


def plot_eq(strategy: np.ndarray, T: int = 30) -> plt.figure:

    # simulate price paths
    a_sim = np.zeros((T+1, num_players), dtype=np.int64)   # paths of actions

    # initial prices: firm 1: p_max, firm 2: p_max-p_step, ...
    for i in range(num_players):
        a_sim[0, i] = num_actions - 1 - i

    # simulation
    for t in range(T):
        a_sim[t+1, :] = a_sim[t, :]
        i = t % num_players
        a_not_i = np.delete(a_sim[t, :], i)
        s = get_stateID((i, a_not_i))
        # a_sim[t+1, i] = np.random.choice(range(num_actions), size=1, p=strategy[s, i, :])[0]  # random action
        a_sim[t+1, i] = np.argmax(np.random.multinomial(1, strategy[s, i, :]))  # most likely action
    p_sim = price_grid[a_sim]   # paths of prices

    # plot best responses and simulation of price paths
    fig = plt.figure(figsize=(12, 4))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.8])

    # 1) best responses
    ax1 = fig.add_subplot(gs[0])
    ax1.set_title('Best Responses', fontsize=14)
    ax1.set_xlabel(r'$p_{2}(p_{1})$', fontsize=12)
    ax1.set_ylabel(r'$p_{1}(p_{2})$', fontsize=12)
    ax1.set_xlim(price_grid.min() - 0.1, price_grid.max() + 0.1)
    ax1.set_ylim(price_grid.min() - 0.1, price_grid.max() + 0.1)

    # grid
    ax1.hlines(price_grid, price_grid - 1, price_grid.max() + 1, colors='black', linestyles='dashed', lw=0.5, alpha=0.3)
    ax1.vlines(price_grid, price_grid - 1, price_grid.max() + 1, colors='black', linestyles='dashed', lw=0.5, alpha=0.3)

    # 45° line
    ax1.plot([price_grid.min() - 1, price_grid.max() + 1], [price_grid.min() - 1, price_grid.max() + 1],
             color='black', linestyle='dotted', lw=1, alpha=1)

    # firm 1
    for a2 in range(num_actions):
        for a1 in range(num_actions):
            ax1.plot(price_grid[a2], price_grid[a1], alpha=strategy[a2, 0, a1], linestyle='None', marker='o',
                     markerfacecolor='white', markeredgecolor='C0', markersize=6)
    # firm 2
    for a1 in range(num_actions):
        for a2 in range(num_actions):
            ax1.plot(price_grid[a2], price_grid[a1], alpha=strategy[num_actions+a1, 1, a2], linestyle='None',
                     marker='x', color='C1', markersize=6)

    ax1.legend(handles=[Line2D([0], [0], linestyle='None', marker='o', markerfacecolor='white', markeredgecolor='C0',
                               markersize=6, label='firm 1'),
                        Line2D([0], [0], linestyle='None', marker='x', color='C1', markersize=6, label='firm 2')],
               loc=(0.2, 0.75))

    # 2) price path simulation
    ax2 = fig.add_subplot(gs[1])
    ax2.set_title('Price Path Simulation', fontsize=14)
    ax2.set_xlabel(r'time $t$', fontsize=12)
    ax2.set_ylabel(r'price $p_{i,t}$', fontsize=12)
    ax2.set_xlim(-1, T+1)
    ax2.set_ylim(price_grid.min() - 0.1, price_grid.max() + 0.1)

    ax2.hlines(price_grid, -1, T+1, colors='black', linestyles='dashed', lw=0.5, alpha=0.3)
    ax2.vlines(range(0, T+1, 5), price_grid.min() - 1, price_grid.max() + 1, colors='black', linestyles='dashed',
               lw=0.5, alpha=0.3)

    ax2.hlines([marginal_costs], -1, T+1, colors='black', linestyles='solid', lw=1, alpha=1)
    ax2.text(T+1, marginal_costs, ' MC', horizontalalignment='left', verticalalignment='center')

    ax2.step(range(T+1), p_sim, where='post')

    plt.show()

    return fig


run = 0
fig = plot_eq(strategy=strategies[0])

fig.savefig('docs/source/img/sequential_price_competition_search_priors_random.svg', bbox_inches='tight')
