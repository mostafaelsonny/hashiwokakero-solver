# Backtracking Solver Implementation

## Purpose

The Backtracking solver searches for a valid Hashiwokakero solution using
recursive depth-first search. It follows the shared Data Model and the
Algorithm Interface contract.

## Inputs

The solver interface is:

```python
solve_backtracking(puzzle, candidate_bridges, config=None)
```

- `puzzle` follows the shared Puzzle model: `rows`, `cols`, and `islands`.
- `candidate_bridges` is the canonical ordered candidate list for the puzzle.
- `config` may provide `max_states`, `timeout_ms`, and `value_order`.

The solver preserves the candidate list order and does not reorder, filter, or
mutate it. Candidate index `i` always maps to the candidate at index `i` in
that list.

## Search State

`BacktrackingState` tracks the mutable search data:

- `assignments`: one entry per candidate.
  - `None` means the candidate has not been decided.
  - `0`, `1`, and `2` are explicit bridge-count assignments.
- `current_degree`: the sum of assigned bridge counts touching each island.
- `remaining_capacity`: the maximum additional degree available from
  undecided incident candidates.
- `required_bridges`: each island's target degree.

Assigning a candidate, including assigning zero, removes its maximum possible
contribution from `remaining_capacity`. Undo restores the previous assignment,
degrees, and capacities.

## Recursive Search

The solver applies recursive depth-first search in canonical candidate order.
For each candidate, it tries values according to `value_order`. The default
order is `[1, 2, 0]`.

After each assignment, the solver applies three pruning rules:

1. **Upper degree bound:** reject the branch if an island's current degree
   exceeds its `required_bridges`.
2. **Lower capacity bound:** reject the branch if an island's current degree
   plus remaining capacity is less than its `required_bridges`.
3. **Geometric crossing:** when the current candidate is assigned a positive
   count, reject the branch if an already-assigned positive candidate that
   crosses it is selected.

Crossing relationships are precomputed as candidate-index pairs. During search,
the solver checks only candidates that cross the candidate currently being
assigned.

The solver does not prune disconnected partial networks. An unassigned bridge
may still connect separate components.

Every attempted assignment is undone before trying the next value or returning
to the caller.

## Final Validation

When all candidates are assigned, the solver converts the assignments into the
shared Solution representation:

```python
{"bridge_counts": {"E1": 1, "E2": 0}}
```

It then calls `core.solution_validator.validate_solution`. A result is marked
`SOLVED` only when the report has `valid == True`.

A complete assignment that fails validation, including one with correct island
degrees but multiple connected components, is rejected and the search
continues.

## Termination Statuses

The solver returns the status values defined by the Algorithm Interface:

- `SOLVED`: a complete assignment passed final validation.
- `UNSATISFIABLE`: the complete search space was exhausted without a valid
  solution.
- `LIMIT_REACHED`: the configured state or time limit stopped the search
  before exhaustion.
- `INVALID_INPUT`: the puzzle, candidate list, or configuration could not be
  processed.

## Metrics

The result includes:

- `runtime_ms`: elapsed execution time measured with a monotonic clock.
- `explored_states`: recursive search states visited.
- `backtracks`: failed branches restored before continuing.
- `pruned_degree_upper`: branches rejected by the upper degree bound.
- `pruned_degree_lower`: branches rejected by the remaining-capacity bound.
- `pruned_crossing`: branches rejected because of a selected crossing.

Metrics are part of the solver result and do not modify the shared Data Model.

## Tests

Run the Search State and Backtracking Solver tests with:

```powershell
python -m pytest tests\test_backtracking_state.py tests\test_backtracking_solver.py -q
```

The tests cover:

- The canonical P1 solution.
- Rejection of degree-complete but disconnected assignments.
- Valid double-bridge solutions.
- Upper-degree and lower-capacity pruning.
- Geometric crossing pruning.
- Exhaustive unsatisfiable search.
- Search-limit handling.
- State rollback after failed branches.
- The standardized result structure and metrics.
