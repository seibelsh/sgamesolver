sgamesolver.SGame.unflatten_strategies
======================================

.. _sgame_unflatten_strategies:

**sgamesolver.SGame.unflatten_strategies(** *strategies_flat*,
*zeros=False* **)**

   Convert a flat array containing a strategy profile
   (or parameters of same shape)
   to an array with shape *(num_states, num_players, num_actions_max)*,
   padded with NaNs or zeros.

   **Parameters:**

      **strategies_flat** : *np.ndarray*
         1D array containing a flattened strategy profile.

      **zeros** : *bool, default False*
         Whether the strategy profile should be padded with zeros or NaNs.

Examples
--------

Description

>>> Code
