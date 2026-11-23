# Algorithm Interface & Result Contract — Hashiwokakero Solver

> **Document Status:** APPROVED & FROZEN (Sprint 2 Architecture Contract)  
> **Document Code:** `S2-01` / `ALGORITHM_INTERFACE.md`  
> **Owner:** Mostafa Elsonny (M1 — Project Manager & Tech Lead)  
> **Consumers & Module Owners:**  
> - Monzer Hassan (M2 — Core Graph Engine)  
> - Ebrahim / El general (M3 — Validation & Backtracking Solver)  
> - Rovan Rafaat (M4 — Genetic Algorithm)  
> - Febronia Adel (M5 — Memetic Algorithm)  
> **Scope:** Defines the authoritative, frozen callable interfaces, input/output structures, result envelopes, status semantics, and metrics contracts across Backtracking, Genetic Algorithm (GA), Memetic Algorithm (MA), and the Unified Central Algorithm Runner.  
> **Single Source of Truth:** Extends and strictly adheres to [`docs/DATA_MODEL.md`](file:///d:/FACULTY/Artificial%20Intelligence/project/hashiwokakero-solver/docs/DATA_MODEL.md).

---

## 1. Architectural Purpose & Executive Summary

In Sprint 2, the team transitions from structural modeling to the concurrent implementation of **three distinct problem-solving paradigms**:
1. **Backtracking Solver (Deterministic / Exact Search)** — Systematic tree search with forward constraint propagation and state restoration.
2. **Genetic Algorithm (Stochastic / Evolutionary)** — Population-based global exploration utilizing lexicographical multi-objective fitness.
3. **Memetic Algorithm (Hybrid Evolutionary + Local Search)** — Evolutionary cycle augmented with problem-aware hill-climbing neighborhood optimization.

To ensure seamless interchangeability, zero integration friction, and bulletproof communication between the backend engine, the API (`api/main.py`), and the React UI (`frontend/`), **all algorithms must conform to a single, standardized callable interface and return an identical, typed result contract.**

```
                                 [ User / UI Request ]
                                           │
                                           ▼
                                 [ POST /solve (API) ]
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │     core.algorithm_runner.run_algorithm      │
                    └──────────────────────────────────────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
             [ 1. Validate Puzzle Model ]           [ If Invalid: Return ]
                        │                          [ status="INVALID_INPUT" ]
                        ▼
             [ 2. Generate Candidate Bridges ]
                 (Canonical Order E1..En)
                        │
                        ▼
             [ 3. Dispatch to Selected Solver ]
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
  solve_backtracking solve_genetic  solve_memetic
  (Exact / M3)       (Stochastic/M4)(Hybrid / M5)
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
             [ 4. Raw Solver Result ]
                        │
                        ▼
       [ 5. Independent Final Validation Gate ]
         (core.solution_validator.validate_solution)
                        │
                        ▼
             [ 6. Standard Solver Result ]
                        │
                        ▼
                [ UI Visualization ]
```

---

## 2. Frozen Foundational Rules (Non-Negotiable)

Every algorithm developer (M3, M4, M5) must adhere to these frozen axioms:

1. **`docs/DATA_MODEL.md` is Frozen:** Field names (`required_bridges`, `rows`, `cols`, `islands`, `bridge_counts`) are fixed. No algorithm may modify, rename, or alias these fields.
2. **Deterministic Candidate Ordering ($E_1 \dots E_n$):**
   - Candidate bridges are generated **once** per puzzle by `core.candidate_generator.generate_candidate_edges`.
   - Ordering is canonical: Islands sorted by `(row, col)`; for each island, Horizontal rightwards candidate added first, then Vertical downwards candidate.
   - IDs are sequentially numbered: `E1, E2, ..., En`.
   - **CRITICAL:** Solvers **MUST NEVER** re-sort, filter, mutate, or re-index this candidate list. Positional arrays (such as Chromosomes or Backtracking assignment vectors) must map index $i$ to candidate bridge at index $i$ ($E_{i+1}$).
3. **Solution Representation:**
   - A solution is strictly `{"bridge_counts": {"E1": count, ...}}`.
   - Allowed counts are strictly `0`, `1`, or `2`.
   - Missing known candidate IDs evaluate implicitly to `0`.
4. **Validation Gate:**
   - No algorithm may declare a solution valid without passing `core.solution_validator.validate_solution`.
5. **Zero Unhandled Exceptions:**
   - Solvers must catch internal failures and return standard failure results rather than crashing the execution runner.

---

## 3. Standardized Callable Interfaces

Each algorithm must expose a standalone solver function matching the exact signature below in its respective module:

### 3.1 Backtracking Solver Signature
- **Module:** `core/backtracking_solver.py`
- **Owner:** Ebrahim (M3)

```python
from typing import Dict, List, Optional, Any
from core.models import Puzzle, CandidateBridge

def solve_backtracking(
    puzzle: Puzzle,
    candidate_bridges: List[CandidateBridge],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute exhaustive depth-first backtracking search with constraint pruning.

    Args:
        puzzle: Canonical Puzzle TypedDict with rows, cols, and islands.
        candidate_bridges: Deterministically ordered list of CandidateBridge objects (E1..En).
        config: Optional configuration dictionary (limits, heuristics).

    Returns:
        Standard Solver Result dictionary adhering to SolverResult schema.
    """
```

### 3.2 Genetic Algorithm Solver Signature
- **Module:** `algorithms/ga/genetic_solver.py`
- **Owner:** Rovan (M4)

```python
from typing import Dict, List, Optional, Any
from core.models import Puzzle, CandidateBridge

def solve_genetic(
    puzzle: Puzzle,
    candidate_bridges: List[CandidateBridge],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute Genetic Algorithm evolution loop using multi-objective tournament selection.

    Args:
        puzzle: Canonical Puzzle TypedDict with rows, cols, and islands.
        candidate_bridges: Deterministically ordered list of CandidateBridge objects (E1..En).
        config: Optional hyperparameters (population_size, max_generations, seed, etc.).

    Returns:
        Standard Solver Result dictionary adhering to SolverResult schema.
    """
```

### 3.3 Memetic Algorithm Solver Signature
- **Module:** `algorithms/ma/memetic_solver.py`
- **Owner:** Febronia (M5)

```python
from typing import Dict, List, Optional, Any
from core.models import Puzzle, CandidateBridge

def solve_memetic(
    puzzle: Puzzle,
    candidate_bridges: List[CandidateBridge],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute Memetic Algorithm evolution loop augmented with in-loop Hill Climbing local search.

    Args:
        puzzle: Canonical Puzzle TypedDict with rows, cols, and islands.
        candidate_bridges: Deterministically ordered list of CandidateBridge objects (E1..En).
        config: Optional hyperparameters (GA params + local search frequency, steps, etc.).

    Returns:
        Standard Solver Result dictionary adhering to SolverResult schema.
    """
```

### 3.4 Central Algorithm Runner Signature
- **Module:** `core/algorithm_runner.py`
- **Owner:** Mostafa (M1)

```python
from typing import Dict, Optional, Any
from core.models import Puzzle

def run_algorithm(
    puzzle: Puzzle,
    algorithm_name: str,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Single central gateway for dispatching, executing, and independently validating any algorithm.

    Supported algorithm_name values (case-insensitive):
      - 'backtracking' | 'bt'
      - 'genetic' | 'ga'
      - 'memetic' | 'ma'

    Returns:
        Standard Solver Result dictionary adhering to SolverResult schema.
    """
```

---

## 4. Configuration Schema (`config`)

The `config` parameter is an optional dictionary. If omitted (`None`), the algorithm **MUST** load its verified default configuration. Solvers must ignore unrecognized keys and validate value ranges defensively.

### 4.1 Backtracking Configuration

| Key | Type | Default | Valid Range | Description |
| :--- | :--- | :---: | :---: | :--- |
| `max_states` | `int` | `100000` | $\ge 1$ | Maximum decision states to visit before aborting with `LIMIT_REACHED`. |
| `timeout_ms` | `int` | `10000` | $\ge 100$ | Maximum real runtime budget in milliseconds before aborting. |
| `value_order`| `List[int]` | `[1, 2, 0]`| Permutation of `{0, 1, 2}` | Search value heuristic branch order. Defaults to bridges first (`[1, 2, 0]`). |

### 4.2 Genetic Algorithm Configuration

| Key | Type | Default | Valid Range | Description |
| :--- | :--- | :---: | :---: | :--- |
| `population_size` | `int` | `100` | $10 \le N \le 1000$ | Number of individual chromosomes in the population. |
| `max_generations` | `int` | `100` | $1 \le G \le 5000$ | Maximum evolutionary generations before terminating. |
| `tournament_size` | `int` | `3` | $2 \le k \le 10$ | Tournament selection sample size. |
| `crossover_rate`  | `float` | `0.8` | $0.0 \le p_c \le 1.0$ | Probability of applying uniform crossover between parents. |
| `mutation_rate`   | `float` | `None` (auto: $1/N$) | $0.0 \le p_m \le 1.0$ | Per-gene mutation probability. Defaults to $1 / \text{len}(E)$. |
| `elitism_count`   | `int` | `2` | $0 \le E \le 10$ | Number of fittest individuals preserved unconditionally. |
| `seed`            | `int` | `None` | Any int | Random seed for deterministic regression testing. |
| `timeout_ms`      | `int` | `15000` | $\ge 500$ | Absolute timeout budget in milliseconds. |

### 4.3 Memetic Algorithm Configuration

MA inherits all GA parameters above, plus the following Local Search parameters:

| Key | Type | Default | Valid Range | Description |
| :--- | :--- | :---: | :---: | :--- |
| `ls_frequency` | `int` | `1` | $\ge 1$ | Apply local search every $N$ generations (default 1 = every generation). |
| `ls_max_steps` | `int` | `10` | $1 \le S \le 50$ | Maximum hill-climbing improvement iterations per individual. |
| `ls_candidates_count` | `int` | `2` | $1 \le K \le 10$ | Number of elite/top individuals subjected to local search per generation. |

---

## 5. Standard Solver Result Contract

Every algorithm function and the Algorithm Runner must return a dictionary strictly matching the following schema.

### 5.1 JSON Schema Specification

```json
{
  "status": "SOLVED",
  "solution": {
    "bridge_counts": {
      "E1": 1,
      "E2": 1,
      "E3": 1,
      "E4": 1
    }
  },
  "validation_report": {
    "valid": true,
    "degree_violations": [],
    "crossings": [],
    "connected_components": 1,
    "invalid_values": []
  },
  "metrics": {
    "runtime_ms": 14.2,
    "explored_states": 42
  }
}
```

### 5.2 Python Type Definition (`core/models.py`)

```python
from typing import TypedDict, Literal, Optional, Dict, Any
from core.models import Solution, ValidationReport

SolverStatus = Literal[
    "SOLVED",
    "UNSATISFIABLE",
    "LIMIT_REACHED",
    "NO_VALID_SOLUTION_FOUND",
    "INVALID_INPUT"
]

class SolverResult(TypedDict):
    status: SolverStatus
    solution: Optional[Solution]
    validation_report: Optional[ValidationReport]
    metrics: Dict[str, Any]
```

---

## 6. Status Enum Semantics (Zero Ambiguity)

The `status` string enum conveys the exact computational outcome. Conflating these statuses is a critical contract violation.

```
                  ┌───────────────────────────────┐
                  │ How Did the Algorithm Finish? │
                  └──────────────┬────────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
[ Found Valid Solution ]  [ Search Space Exhausted ]  [ Resource Limit Reached ]
     │                           │                           │
     ▼                           ▼                           ▼
 status="SOLVED"         Is it Backtracking?          Is it Backtracking?
                             ┌───┴───┐                   ┌───┴───┐
                            Yes      No                 Yes      No
                             │       │                   │       │
                             ▼       ▼                   ▼       ▼
                        status=    (Illegal!)       status=    status=
                    "UNSATISFIABLE"             "LIMIT_REACHED" "NO_VALID_SOLUTION_FOUND"
```

### 6.1 `SOLVED`
- **Definition:** The algorithm successfully discovered a complete bridge configuration that was verified by `validate_solution` with `report["valid"] == True`.
- **Field Requirements:**
  - `solution`: Must be non-null `Solution` containing the bridge counts.
  - `validation_report`: Must be non-null `ValidationReport` where `valid: True`.

### 6.2 `UNSATISFIABLE`
- **Definition:** Exhaustive Backtracking searched the entire state space and proved with **mathematical certainty** that no valid bridge assignment exists for this puzzle.
- **RESTRICTION:** **GA and MA MUST NEVER return `UNSATISFIABLE`.** Stochastic algorithms sample only a tiny subset of the search space; failure to find a solution is never mathematical proof of impossibility.
- **Field Requirements:**
  - `solution`: `None`.
  - `validation_report`: `None`.

### 6.3 `LIMIT_REACHED`
- **Definition:** Backtracking reached its configured budget threshold (`max_states` or `timeout_ms`) before completing the search tree. The puzzle might still be solvable if given more resources.
- **Field Requirements:**
  - `solution`: `None`.
  - `validation_report`: `None`.

### 6.4 `NO_VALID_SOLUTION_FOUND`
- **Definition:** Genetic Algorithm or Memetic Algorithm exhausted its generation budget (`max_generations`) or time limit without producing an individual whose fitness is `(0, 0, 0)` and whose candidate passes `validate_solution`.
- **Field Requirements:**
  - `solution`: `None` (or optionally the best-so-far candidate if requested by diagnostics, but `status` remains `NO_VALID_SOLUTION_FOUND`).
  - `validation_report`: `None` (or report of the best-so-far candidate showing remaining violations).

### 6.5 `INVALID_INPUT`
- **Definition:** The input `puzzle` or `candidate_bridges` failed structural validation (e.g. negative dimensions, islands with identical coordinates, degrees outside $[1, 8]$, or out-of-bounds coordinates).
- **Field Requirements:**
  - `solution`: `None`.
  - `validation_report`: `None`.
  - `metrics`: Contains error details, e.g., `{"error": "Duplicate island coordinate (0, 2)"}`.

### 6.6 Status Field Requirements Matrix

| `status` | `solution` | `validation_report` | Applicable Algorithms |
| :--- | :---: | :---: | :--- |
| `"SOLVED"` | `dict` (valid) | `dict` (`valid: True`) | Backtracking, GA, MA |
| `"UNSATISFIABLE"` | `None` | `None` | **Backtracking ONLY** |
| `"LIMIT_REACHED"` | `None` | `None` | **Backtracking ONLY** |
| `"NO_VALID_SOLUTION_FOUND"` | `None` | `None` (or best-effort) | **GA, MA ONLY** |
| `"INVALID_INPUT"` | `None` | `None` | All (triggered by runner/validator) |

---

## 7. Metrics Specification

The `metrics` dictionary captures execution telemetry. All keys must use standard types (integers, floats, lists) to ensure JSON-serializability.

### 7.1 Mandatory Core Metric
- `runtime_ms` (`float`): Elapsed execution time in milliseconds measured via `time.perf_counter()`. Mandatory for all solvers and all statuses.

### 7.2 Solver-Specific Metrics

#### Backtracking Metrics
- `explored_states` (`int`): Total decision nodes visited in the search tree.
- `backtracks` (`int`): Count of state restorations executed after hitting a dead end or constraint violation.
- `pruned_degree_upper` (`int`, optional): Branches pruned by upper bound degree check.
- `pruned_degree_lower` (`int`, optional): Branches pruned by remaining capacity check.
- `pruned_crossing` (`int`, optional): Branches pruned by geometric crossing conflict.

#### Genetic Algorithm (GA) Metrics
- `generations` (`int`): Total generations completed before termination.
- `evaluations` (`int`): Total fitness evaluations performed.
- `best_fitness` (`List[int]`): 3-tuple represented as a list `[degree_violations, active_crossings, connectivity_penalty]`.
- `population_size` (`int`): Active population size.

#### Memetic Algorithm (MA) Metrics
- Inherits all GA metrics above (`generations`, `evaluations`, `best_fitness`).
- `local_search_calls` (`int`): Total times the Hill Climbing routine was executed.
- `local_search_improvements` (`int`): Total times a local search move strictly improved an individual's fitness.
- `avg_ls_steps_per_call` (`float`, optional): Average steps taken before reaching a local optimum.

---

## 8. Chromosome & Solution Conversion Rules (GA & MA)

GA and MA manipulate positional integer arrays (`List[int]`). To ensure zero translation error:

1. **Mapping Invariant:**
   $$\text{Gene at index } i \longleftrightarrow \text{CandidateBridge at index } i \text{ in canonical generator order}$$
   $$\text{Length of chromosome} \equiv \text{len(candidate\_bridges)}$$
2. **Lossless Conversion Functions:**
   Every solver module must import and use the standard converters from `algorithms/ga/chromosome.py`:
   - `chromosome_to_solution(chromosome: List[int], candidate_bridges: List[CandidateBridge]) -> Solution`
   - `solution_to_chromosome(solution: Solution, candidate_bridges: List[CandidateBridge]) -> List[int]`
3. **Lexicographical Multi-Objective Fitness Evaluation:**
   Fitness is evaluated via `algorithms/ga/fitness.py` returning a 3-tuple `(degree_error, crossing_count, connectivity_penalty)`:
   - $\text{degree\_error} = \sum_{\text{islands}} | \text{required} - \text{actual} |$
   - $\text{crossing\_count} = \text{number of intersecting candidate pairs with both counts } > 0$
   - $\text{connectivity\_penalty} = \max(0, \text{connected\_components} - 1)$
   - Target fitness is strictly `(0, 0, 0)`.

---

## 9. Independent Validation & The Algorithm Runner Guard

The **Unified Algorithm Runner** (`core/algorithm_runner.py`) provides an indispensable security boundary between algorithms and client callers (API/UI).

```python
# Central Runner Enforcement Workflow:
def run_algorithm(puzzle: Puzzle, algorithm_name: str, config: Optional[dict] = None) -> SolverResult:
    # Step 1: Baseline Structural Validation
    if not is_structurally_valid(puzzle):
        return {"status": "INVALID_INPUT", "solution": None, "validation_report": None, "metrics": {}}

    # Step 2: Canonical Candidate Generation
    candidate_bridges = generate_candidate_edges(puzzle["islands"])

    # Step 3: Dispatch Execution
    solver_fn = resolve_algorithm(algorithm_name)
    raw_result = solver_fn(puzzle, candidate_bridges, config)

    # Step 4: Independent Validation Gate
    if raw_result["status"] == "SOLVED":
        solution = raw_result.get("solution")
        if not solution:
            raw_result["status"] = "NO_VALID_SOLUTION_FOUND"
        else:
            # RUN INDEPENDENT FINAL VALIDATION
            report = validate_solution(puzzle, solution)
            raw_result["validation_report"] = report
            if not report["valid"]:
                # The algorithm returned an invalid solution claiming it was SOLVED!
                # Safeguard: downgrade status to prevent UI corruption
                raw_result["status"] = "NO_VALID_SOLUTION_FOUND"
                raw_result["metrics"]["validation_override"] = "Solution failed independent validation"

    return raw_result
```

---

## 10. Canonical P1 Verification Example

To verify adherence across all three algorithm modules during Sprint 2, the standard benchmark fixture **P1** must yield the following canonical outputs:

### Input Puzzle P1
- Grid: $3 \times 3$
- Islands: $A(0,0)=2, B(0,2)=2, C(2,0)=2, D(2,2)=2$
- Canonical Candidates: $E_1(A-B), E_2(A-C), E_3(B-D), E_4(C-D)$

### Expected Canonical Output (`status: "SOLVED"`)

```json
{
  "status": "SOLVED",
  "solution": {
    "bridge_counts": {
      "E1": 1,
      "E2": 1,
      "E3": 1,
      "E4": 1
    }
  },
  "validation_report": {
    "valid": true,
    "degree_violations": [],
    "crossings": [],
    "connected_components": 1,
    "invalid_values": []
  },
  "metrics": {
    "runtime_ms": 4.15,
    "explored_states": 8
  }
}
```

---

## 11. Acceptance Checklist for Module Owners

Before opening a PR for `S2-04` (Backtracking), `S2-07` (GA), or `S2-10` (MA), verify:

- [ ] Solver function accepts exactly `(puzzle, candidate_bridges, config=None)`.
- [ ] Solver never re-sorts, filters, or mutates `candidate_bridges`.
- [ ] Return value strictly matches the `SolverResult` dictionary schema.
- [ ] Status is one of the 5 allowed enum values.
- [ ] GA and MA solvers never return `UNSATISFIABLE`.
- [ ] Runtime is tracked in milliseconds (`runtime_ms`) using monotonic clock.
- [ ] P1 benchmark puzzle runs end-to-end and returns canonical solution `{"E1": 1, "E2": 1, "E3": 1, "E4": 1}`.
- [ ] All unit and regression tests pass cleanly under `pytest`.
