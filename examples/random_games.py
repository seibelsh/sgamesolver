import sgamesolver
from examples._helpers import solve_game


game = sgamesolver.SGame.random_game(num_states=62, num_players=2, num_actions=4, seed=42)
homotopy = sgamesolver.homotopy.QRE(game=game)
homotopy.solver_setup()
homotopy.solve()
print(homotopy.equilibrium)


# %% common discount factors and actions


game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                     num_actions=4, delta=0.95, seed=42)
solve_game(game)


# %% randomized discount factors and actions


game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                     num_actions=[3, 5], delta=[0.92, 0.98])
solve_game(game)


# %% specific individual discount factors and actions


game = sgamesolver.SGame.random_game(num_states=2, num_players=3,
                                     num_actions=[[3, 4, 5],
                                                  [4, 5, 3]],
                                     delta=[0.94, 0.95, 0.96])
solve_game(game)
