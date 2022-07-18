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


# %% solving games


game = sgamesolver.SGame.random_game(3, 3, 3, seed=123)
homotopy = sgamesolver.homotopy.LogTracing(game)

homotopy.solver_setup()
homotopy.solve()
# ==================================================
# Start homotopy continuation
# Step   140: t =  1.000 ↑, s =  328.1, ds =  1.840120
# Step   140: Continuation successful. Total time elapsed: 0:00:01
# End homotopy continuation
# ==================================================
# An equilibrium was found via homotopy continuation.

homotopy.solver_setup()
homotopy.solver.verbose = 0
homotopy.solve()

homotopy.solver_setup()
homotopy.solver.start_storing_path()
homotopy.solve()
homotopy.plot_path()

fig = homotopy.plot_path()
fig.savefig("docs/source/img/random_game_path_s.svg")

homotopy.plot_path(x_axis='t')

homotopy.plot_path(x_axis='step')


# %% interacting with the solver


game = sgamesolver.SGame.random_game(64, 2, 4, seed=31)

homotopy = sgamesolver.homotopy.LogTracing(game)
homotopy.eta = 0.1
homotopy.solver_setup()

homotopy.solve()

# saving and loading solver state:

homotopy.solver.save_file('example.txt')
# Current state saved as example.txt.

homotopy.solver.load_file('example.txt')
# State successfully loaded from example.txt.


# storing the path:

game = sgamesolver.SGame.random_game(8, 4, 4, seed=42)
homotopy = sgamesolver.homotopy.LogTracing(game)
homotopy.solver_setup()

homotopy.solver.start_storing_path(max_steps=25000)

homotopy.solver.max_steps = 200
homotopy.solve()

homotopy.solver.return_to_step(step_no=123)
# Returning to step 122.


# plotting the path:

fig = homotopy.plot_path()
fig.savefig("docs/source/img/random_game_path_arc_length.svg")

homotopy.plot_path()
homotopy.plot_path(x_axis='t')
homotopy.plot_path(x_axis='step')
homotopy.plot_path(s_range=(500, 700))
homotopy.plot_path(step_range=(125, 175))
