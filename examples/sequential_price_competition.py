import sgamesolver
import numpy as np
import itertools
from examples._helpers import solve_game


# %% alternating moves: sequential price competition


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

solve_game(game)

game_table = game.to_table()
