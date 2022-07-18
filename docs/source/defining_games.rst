Defining games
==============

In sGameSolver, stochastic games can be defined using the
:py:class:`sgamesolver.SGame` class.

Defining a stochastic game requires three inputs:

1. payoffs
2. transitions
3. discount factors

There are two distinct formats in which stochastic games can be specified:
Either as **table** or in the form of NumPy **arrays**.
In terms of functionality, both formats are absolutely equivalent:
anything that can be done in one can also be done in the other.
However, they differ a bit in usability.

The tabular format is more human-readable
and will probably be more intuitive for many users.
It also has the advantage that languages or programs other than python
can easily be used to define a game,
for example Excel, Stata, R
- or just about any program that can produce data tables.
This makes sGameSolver more accessible
if you have little experience with Python.

The array format on the other hand is closer to
the internal (and mathematical) representation of stochastic games.
It is also more parsimonious and therefore better suited
to handle very large games,
where the tabular format may quickly result in file sizes
in the order of gigabytes.

You can find a complete description of the syntax of both formats below.
The examples in this tutorial further demonstrate how to enter specific games
- each of them covering both possible formats.


.. tabs::

    .. group-tab:: Table

        In the tabular format, the complete description of the game is passed as a single table,
        which contains all information on players, states, action sets, utility functions, state
        transition functions and discount factors.

        The table itself can be passed to sGameSolver either as a :py:mod:`pandas` dataframe,
        or as a file in one of the following formats:

        - .csv (comma separated values in plain text)
        - .xls or .xlsx (Microsoft excel)
        - .dta (stata data file)

        If you would like to use some other program to create the table,
        e.g. R, use the program's export functionality to one of these formats,
        or import your file to a pandas dataframe first, and then pass it to sGameSolver.

        To load a game from a table, use the method :py:meth:`SGame.from_table`.
        The argument can either be a pandas dataframe, or a string that contains the
        (absolute or relative) path to the file you'd like to load. For example:

        .. code-block:: python

            import sgamesolver
            game = sgamesolver.SGame.from_table("C:/path/to/my_game_file.csv")

        Here is an example of a game with 2 states, 2 players and 2 actions each,
        defined in the tabular format.

        ======  =========  =========  =========  =========  ==========  ==========
        state   a_player0  a_player1  u_player0  u_player1  phi_state0  phi_state1
        ======  =========  =========  =========  =========  ==========  ==========
        delta                         0          0
        state0  action0    action0    1          2          1           0
        state0  action0    action1    3          4          0.5         0.5
        state0  action1    action0    5          6          0.5         0.5
        state0  action1    action1    7          8          1           0
        state1  action0    action0    8          7          0           0
        state1  action0    action1    6          5          0.5         0.5
        state1  action1    action0    4          3          0.5         0.5
        state1  action1    action1    2          1          0           0
        ======  =========  =========  =========  =========  ==========  ==========

        Each row (save the first, which will be discussed below)
        corresponds to one action profile in one state, and specifies
        payoffs and state transitions which result from it.

        Specifically:

        - The column "state" contains the label of the current state.

        - A set of columns of the named "a\_{player label}", one for each player,
          which together specify the action profile the row refers to.

          - If your players are called "p0", "p1", and "p2", these columns
            are headed "a\_p0", "a\_p1", "a\_p2"; if your players are "firm" and
            "consumer", "a\_firm" and "a\_consumer", etc.

        - A set of columns "u\_{player label}", specifying the instantaneous
          utility to the respective player from said action set.

          - The player labels need to match exactly those from the
            "a\_"-columns.

        - A set of columns "phi\_{state label}", one for each state. These
          columns indicate the probability of reaching that state next if
          the given action profile is played in the current state.

          - Note that each state appearing in the state column must have a
            phi-column.
          - If the game has deterministic transitions,
            a shorter syntax is available: see details below.

        - Finally, the table must have one row used to specify discount
          factors. This row has "delta" in the state column, and each
          player's discount factor in their "u\_"-column. All other
          fields should be empty.

        Some more details:

        - General remarks

          - All columns and rows can be in arbitrary order.
            (But note that sGameSolver will order players by
            the order of their "a\_"-columns, and states and actions by the
            order their labels first appear in the state / "a\_" columns.)
          - The table can have arbitrary additional columns, which will
            just be ignored. (You might find it helpful to store
            additional variables used to compute u or phi.)
          - All numbers will be converted to double precision when
            converting the table to a game; the format of the table cells
            does not matter (e.g. excel string-formatted fields are fine,
            as long as the entered values follow the usual decimal format).

        - State column

          - You can use any strings you would like as labels for the individual states.
          - You could e.g. number them "s0", "s1", "s2".
          - ... or, give them more descriptive names such as "high demand", "low demand",
          - ... or even "d=0", "d=0.1", ...
          - However, it must be possible to create the "phi\_-{state label}"
            columns headers. (E.g., in stata, "p=1/3" would not be a
            possible state label, because "phi_p=1/3" is not a legal
            column name in stata. In excel or csv, this would be fine.)

        - Action columns

          - Again, any string is permissible for the action labels.
          - There is no limit on their length, but some functions of
            sGameSolver will truncate action labels to 5 characters
            (e.g. when printing equilibria).
          - The action labels of different players or the same player
            in different states can match, but
            of course do not have to.
          - If a player has no decision to make in a specific state, you can just leave
            their "a\_"-field empty, or write something like
            "do nothing" if you prefer.
          - (Technically, a player being inactive in a state
            is implemented as them having a singleton action set.)

        - State transitions

          - As mentioned, there is an alternative syntax if all transitions
            are deterministic: You can then
            replace all "phi\_"-columns by a single column called "to_state"
            which just contains the label of the resulting state.
            The section on the dynamic variation of the Rock Paper Scissors game
            (see :doc:`defining_games_example_simple_stochastic_game`)
            discusses both options.
            But don't mix formats: sGameSolver will raise an error if
            it finds both types of columns.
          - Note that if using the "phi\_"-format, each state appearing in
            the state column *must* have a corresponding "phi\_"-column.
          - Also note that sGameSolver does not enforce a sum-to-1
            condition. Sums smaller than 1 are actually fine: the
            remaining probability just indicates the chance for
            the game to end after the respective action profile.
            (Sums larger than 1 may mean that values aren't
            well-defined and should be avoided.)


    .. group-tab:: Arrays

        In the array format, utility and transition functions
        are passed to sGameSolver as numpy arrays. When using this format,
        states, players and actions are primarily represented by their index
        (i.e. 0, 1, 2, ... Keep in mind Python is 0-indexed.
        It is possible to specify labels for each, but this is more
        of an afterthought.) Thus, when using this format you should
        first decide on a way to enumerate your states,
        players, and the action sets of all players in all states.
        The information should then be arranged as follows.

        **Payoffs** are passed as a list of numpy arrays, the first
        corresponding to state0, the second to state 1 etc.:

        .. code-block:: python

          u_list = [u_state0, u_state1, ...]

        The first index of each of these arrays refers to the player;
        the second to the action of player0; the third to the section of
        player1 etc. If the game has P players, and player0 has A0 actions
        in the respective state etc., then the array should have P+1
        dimensions with shape (P, A0, A1, ...). Suppose that P is 3.
        Then, for example, the element
        u_state0[1, 3, 2, 0] corresponds to the utility of player1 if
        player0 plays action3, player1 plays action2, and player3 plays
        action0. Of course, the number of actions of
        each player may differ from state to state; sGameSolver will
        infer them from the shape of the arrays. If a player has
        no decision to make in some state, the respective dimension
        of the array should be 1 (and not 0); in other words, this
        corresponds to the player having a singleton action set.

        **Transitions** are likewise passed as list of arrays:

        .. code-block:: python

           phi_list = [phi_state0, phi_state1, ...]

        Here, the first list element contains the transition probabilities
        **from** state0 and so on. If the game has S states,
        each array has shape (A0, A1, ..., S), where again A0 refers to the
        number of actions of player0 in the current state. (Of course,
        the numbers of actions of all players must be the same
        between the u- and phi-array of each state.) The last index refers
        to the **to-state** of the respective transition probability.
        phi\_0[1, 2, 4] thus represents the probability to go
        *from* current state0 *to* state4 if player0 plays their action1
        and player2 plays action2. Note that "staying in state0" is
        the same as "transitioning from state0 to state0", e.g. if
        the probability is to be 0.4, you'll need to set phi\_0[1, 2, 0]=0.4.

        Also note that sGameSolver does not enforce a sum-to-1 condition
        over the last dimension of the phi-arrays.
        Sums smaller than 1 are actually fine: the remaining probability
        just indicates the chance for the game to end after the respective
        action profile. (Sums larger than 1 may mean that values
        aren't well-defined and should be avoided.)

        The final piece needed to define a game are **discount factors**.
        These can be passed as a list or numpy array,
        with one entry for each player.
        If all players share the same discount factor, you can
        alternatively just pass a single float.

        .. code-block:: python

           delta = [.95, .85]
           # or, if all players discount with e.g. .9:
           delta = .9

        Once all these objects are in place, you can create the game as
        follows:

        .. code-block:: python

           game = sgamesolver.SGame(u_list, phi_list, delta)


        Finally, once the game has been created, you can add labels for
        state, players and actions. This is fully optional and only
        used for some output, e.g. when printing equilibria;
        the default labels just enumerate all three.
        For states and players, labels are always a list
        of strings of the respective length:

        .. code-block:: python

           # assuming two players and three states:
           game.state_labels = ["low", "medium", "high"]
           game.player_labels = ["buyer", "seller"]

        For actions, there are currently two possibilities:
        Either you provide a single list of strings, which
        will be used for all states and players (the list should
        have as length at least the maximum number of actions of
        any single agent.) Or you provide a nested list of
        strings with depth 3 (a list-of-lists-of-lists-of-strings);
        the outermost list corresponds to states, the next to players,
        and then the inner to
        actions. For example, ``action_lists[0][1][2]``
        should be the label
        of action2 of player1 in state0.

        .. code-block:: python

           # single list:
           game.action_labels = ["p=0", "p=.1", "p=.2", ] # etc

           # nested lists:
           game.action_labels = [[["a_0_0_0", "a_0_0_1"],
                                  ["a_0_1_0", "a_0_1_1"]],
                                  #etc
                                  ]


        Note that while there is no limit on length for action labels,
        some functionality (e.g.
        equilibrium output) will truncate them to five characters.


.. toctree::
    :titlesonly:

    defining_games_example_simple_stochastic_game
    defining_games_example_random_stochastic_games
    defining_games_example_one_shot_games
    defining_games_example_sequential_moves
