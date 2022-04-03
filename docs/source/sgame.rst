Defining games
==============

Use the :py:class:`sGame` class to define any stochastic game.

TBC

Example 1: One-shot game
------------------------

A one-shot game (normal-form game) is a stochastic game with only one state
and full discounting (:math:`\delta=0`).

To define a one-shot game, use the
:py:meth:`SGame.one_shot_game` method.

The ``payoff_matrix`` should be array-like with
dimensions :math:`N \times A_1 \times \dots \times A_N`,
where :math:`N` denotes the number of players
and :math:`A_n` denotes the number of actions of player :math:`n=1,...,N`.

TBC

Example 2: Repeated game
------------------------

TBC

Example 3: Markov decision problem
----------------------------------

TBC

Example 4: Stochastic game
--------------------------

TBC
