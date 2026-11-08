"""Solvers. All three use the SAME core engine and return the SAME result shape.

Result shape:
  {"status": <one of the STATUS_* constants>,
   "solution": Solution | None,
   "stats": {...}}              # time, explored states, backtracks / generations, fitness ...
Rule: never return STATUS_SOLUTION_FOUND unless core.solution_validator says valid.
"""
STATUS_SOLUTION_FOUND = "Solution Found"
STATUS_NO_SOLUTION_EXISTS = "No Solution Exists"  # ONLY Backtracking, only after a complete search
STATUS_SEARCH_LIMIT_REACHED = "Search Limit Reached"
STATUS_NO_VALID_SOLUTION = "No Valid Solution Found Within Search Limits"  # GA / MA failure
STATUS_INVALID_INPUT = "Invalid Input"
