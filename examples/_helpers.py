import sgamesolver
import numpy as np


def solve_game(game: sgamesolver.SGame, printout: bool = False) -> None:
    homotopy = sgamesolver.homotopy.QRE(game=game)
    homotopy.solver_setup()
    homotopy.solver.verbose = 0
    homotopy.solve()
    if printout:
        print(homotopy.equilibrium)


def assert_games_equal(game1: sgamesolver.SGame, game2: sgamesolver.SGame) -> None:
    assert np.allclose(game1.u, game2.u)
    assert np.allclose(game1.phi, game2.phi)
    assert np.allclose(game1.delta, game2.delta)
