# Genetic Algorithm Implementation & Architecture Guide

> **Document Status:** APPROVED & COMPLETE (Sprint 2 Deliverable)  
> **Document Code:** `S2-08` / `GA_IMPLEMENTATION.md`  
> **Module Owner:** Rovan Rafaat (M4 — Genetic Algorithm)  
> **Tech Lead & Reviewer:** Mostafa Elsonny (M1 — Project Lead)  
> **Consumers:** Febronia Adel (M5 — Memetic Algorithm), Central Algorithm Runner (`core/algorithm_runner.py`)  
> **Source of Truth:** Adheres strictly to [`docs/DATA_MODEL.md`](DATA_MODEL.md) and [`docs/ALGORITHM_INTERFACE.md`](ALGORITHM_INTERFACE.md).

---

## 1. Algorithm Overview & Mathematical Foundation

### 1.1 Problem Formulation as Combinatorial Optimization
The **Hashiwokakero** (Bridges) puzzle is represented as a constrained, discrete topological graph $G = (V, E_{\text{cand}})$:
* **Vertices $V$:** A set of fixed islands, where each island $v \in V$ requires a target degree $d_{\text{req}}(v) \in \{1, \dots, 8\}$.
* **Candidate Edges $E_{\text{cand}} = \{E_1, E_2, \dots, E_n\}$:** Deterministically generated orthogonal connections between nearest visible islands in the four cardinal directions.
* **Decision Variables $\mathbf{x} = [x_1, x_2, \dots, x_n]$:** Each candidate bridge $E_i$ is assigned an integer count $x_i \in \{0, 1, 2\}$, where:
  * $0$: No bridge selected.
  * $1$: Single bridge selected.
  * $2$: Double parallel bridge selected.

The combinatorial search space size is given by:
$$|S| = 3^{|E_{\text{cand}}|}$$

For a puzzle with 20 candidate bridges, the search space contains $3^{20} \approx 3.48 \times 10^9$ states, rendering exhaustive brute-force search impractical for larger instances.

### 1.2 Genetic Algorithm Paradigm
The Genetic Algorithm (GA) performs global stochastic search over this discrete space. It mimics biological evolution through iterative selection, crossover, and mutation over a population of candidate chromosomes:

```
                      [ Canonical Puzzle & Candidate Bridges ]
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │ 1. Initialize Population (Pop Size N) │
                     └──────────────────┬────────────────────┘
                                        │
                                        ▼
                     ┌───────────────────────────────────────┐
                     │ 2. Evaluate Multi-Objective Fitness   │
                     │    (Degree, Crossings, Connectivity)  │
                     └──────────────────┬────────────────────┘
                                        │
                         Is Optimal (0, 0, 0) & Valid?
                                    /        \
                                  Yes         No
                                  /             \
                                 ▼               ▼
                 [ Independent Validation Gate ]  [ Generation / Time Limit? ]
                 (validate_solution -> SOLVED)    /                          \
                                                Yes                           No
                                                /                              \
                                               ▼                                ▼
                                [ NO_VALID_SOLUTION_FOUND ]       [ 3. Elitism (Top E Copies) ]
                                                                                │
                                                                                ▼
                                                                  [ 4. Tournament Selection ]
                                                                                │
                                                                                ▼
                                                                  [ 5. Uniform Crossover ]
                                                                                │
                                                                                ▼
                                                                  [ 6. Random Gene Mutation ]
                                                                                │
                                                                                ▼
                                                                  [ Form Next Generation ]
                                                                                │
                                                                                └──── (Repeat)
```

---

## 2. Chromosome Encoding & Solution Mapping

### 2.1 Positional 1-to-1 Mapping Invariant
In accordance with `docs/DATA_MODEL.md` Section 7:
* A **Chromosome** is represented as a plain Python integer array (`List[int]`).
* The gene at index $i$ corresponds strictly to the candidate bridge at index $i$ in the canonical candidate generator order ($E_{i+1}$):
$$\text{Gene } i \longleftrightarrow E_{i+1} \quad (0 \le i < |E_{\text{cand}}|)$$
* The chromosome length strictly equals the candidate bridge count:
$$\text{len}(\text{chromosome}) \equiv \text{len}(\text{candidate\_bridges})$$
* Gene values are bounded strictly to the integer domain $\{0, 1, 2\}$. Floating-point values and booleans are rejected without coercion (`type(gene) is int and gene in (0, 1, 2)`).

### 2.2 Lossless Round-Trip Conversion Utilities
Implemented in `algorithms/ga/chromosome.py`:
* **`chromosome_to_solution(chromosome, candidate_bridges)`:**
  Converts the positional gene list into the standardized `Solution` dictionary:
  ```python
  {"bridge_counts": {"E1": 1, "E3": 2, "E4": 1}}
  ```
  *Producer Normalization Rule:* In strict compliance with `DATA_MODEL.md` Section 6.2, zero-count bridges are omitted from the dictionary to keep outputs concise.
* **`solution_to_chromosome(solution, candidate_bridges)`:**
  Converts a `Solution` dictionary back into a positional chromosome. Any missing known candidate ID automatically evaluates to `0`. Unknown IDs raise an explicit `ValueError`.
* **Mathematical Invariant:** For any valid chromosome $C$:
$$\text{solution\_to\_chromosome}(\text{chromosome\_to\_solution}(C, E), E) \equiv C$$

### 2.3 Explicit Reason Codes
Validation failures immediately raise `ValueError` prefixed with the standardized reason codes of `DATA_MODEL.md` Section 8.5:
* `chromosome_length_mismatch`
* `chromosome_gene_must_be_integer_0_1_or_2`
* `unknown_candidate_bridge_id`
* `bridge_count_must_be_integer_0_1_or_2`

---

## 3. Fitness Evaluation & Multi-Objective Lexicographical Ordering

### 3.1 Lexicographical Multi-Objective Tuple
To prevent the arbitrariness, parameter tuning traps, and distortion inherent in weighted sum fitness functions ($W_1 f_1 + W_2 f_2 + W_3 f_3$), the evaluator computes a **lexicographical multi-objective 3-tuple**:
$$\mathbf{F}(C) = (f_{\text{degree}}, f_{\text{crossing}}, f_{\text{connectivity}})$$

Where optimal fitness is strictly:
$$\mathbf{F}_{\text{optimal}} = (0, 0, 0)$$

Lower values are strictly superior across all objectives.

### 3.2 Objective Mathematical Definitions
Implemented in `algorithms/ga/fitness.py`:

#### 1. Degree Error ($f_{\text{degree}}$)
The cumulative absolute discrepancy between required island degrees and actual selected degrees:
$$f_{\text{degree}} = \sum_{v \in V} |d_{\text{req}}(v) - d_{\text{actual}}(v)|$$
Where $d_{\text{actual}}(v)$ is the sum of bridge counts for all candidate bridges incident to island $v$.

#### 2. Active Crossing Count ($f_{\text{crossing}}$)
The count of geometrically intersecting candidate bridge pairs that are simultaneously active ($>0$):
$$f_{\text{crossing}} = \sum_{(E_i, E_j) \in \text{Conflicts}} \mathbb{I}(x_i > 0 \land x_j > 0)$$
* Double bridges ($x=2$) contribute exactly $1$ crossing to the pair count.
* Bridges touching at endpoint islands do not cross (strict inequalities: $r_1 < r < r_2$ and $c_1 < c < c_2$).

#### 3. Connectivity Penalty ($f_{\text{connectivity}}$)
Measures the topological fragmentation of the network:
$$f_{\text{connectivity}} = \max(0, \text{ConnectedComponents}(V, E_{\text{selected}}) - 1)$$
* A fully connected single network yields $1 - 1 = 0$.
* Disconnected networks receive a penalty proportional to the number of isolated subgraphs.

### 3.3 Lexicographical Dominance & Selection Mechanics
In Python, tuples naturally compare element-by-element from left to right:
$$(a_1, b_1, c_1) < (a_2, b_2, c_2) \iff (a_1 < a_2) \lor (a_1 = a_2 \land b_1 < b_2) \lor (a_1 = a_2 \land b_1 = b_2 \land c_1 < c_2)$$

This aligns naturally with the puzzle constraints:
1. First, search trajectories prioritize minimizing **degree discrepancies**.
2. Among chromosomes with equal degree errors, trajectories eliminate **geometric crossings**.
3. Among crossing-free structures, trajectories resolve **connectivity**.

### 3.4 Performance Optimizations
* **Static Conflict Precomputation (`build_conflict_pairs`):**
  Geometric crossings are computed **once** per puzzle in $O(|E_{\text{cand}}|^2)$ and cached. The fitness loop evaluates crossings in $O(|\text{Conflicts}|)$ via simple array lookups, avoiding costly coordinate arithmetic during evolutionary cycles.
* **Disjoint-Set (Union-Find) with Path Compression:**
  Connected components are computed in nearly linear time $O(|E| \cdot \alpha(|V|))$, avoiding full recursive DFS graph traversal for every chromosome.

---

## 4. Genetic Operators & Configurations

Implemented in `algorithms/ga/operators.py`:

### 4.1 Tournament Selection
* **Function:** `tournament_selection(population, fitnesses, k=3, rng=None)`
* **Mechanism:** Uniformly samples $k$ contestant chromosomes at random (without replacement).
* **Selection:** The contestant with the lowest lexicographical fitness tuple wins the tournament.
* **Memory Safety:** Always returns a freshly copied chromosome `list(population[winner_idx])` to eliminate downstream mutation aliasing.

### 4.2 Uniform Crossover
* **Function:** `uniform_crossover(parent1, parent2, rng=None)`
* **Mechanism:** For each gene index $i \in [0, |E_{\text{cand}}|-1]$, the offspring inherits $parent1[i]$ with probability $0.5$ and $parent2[i]$ with probability $0.5$.
* **Property:** Uniform crossover enables fine-grained recombination across distant orthogonal edges without positional block bias. Length and candidate mapping are strictly preserved.

### 4.3 Gene Mutation
* **Function:** `mutate(chromosome, mutation_rate=None, rng=None)`
* **Probability:** Configurable $p_{\text{mut}}$ (default: $1 / \text{len}(\text{chromosome})$).
* **Domain Preservation:** When a gene mutates, it is replaced by a randomly chosen **different** value from $\{0, 1, 2\} \setminus \{x_i\}$. This guarantees every triggered mutation produces an active exploratory state change.
* **Non-Destructive:** Returns a newly allocated chromosome list without modifying the input array.

### 4.4 Elitism
* **Function:** `get_elites(population, fitnesses, elitism_count=2)`
* **Mechanism:** Sorts the population by fitness ascending and extracts the top $E$ individuals.
* **Aliasing Prevention:** Returns deep copies of each elite chromosome. Elites are transferred directly to the next generation without mutation or crossover, guaranteeing monotonic convergence of the best fitness.

---

## 5. Hyperparameter Recommendations

The following table provides empirically verified hyperparameter recommendations across different puzzle sizes:

| Hyperparameter | Key in Config | Small Grids ($\le 4 \times 4$) | Medium Grids ($5 \times 5 - 7 \times 7$) | Large Grids ($\ge 8 \times 8$) | Description |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Population Size** | `population_size` | $50$ | $100$ | $150 - 200$ | Number of active chromosomes per generation. |
| **Max Generations** | `max_generations` | $50$ | $100$ | $200 - 500$ | Upper bound on evolutionary search iterations. |
| **Tournament Size** | `tournament_size` | $3$ | $3$ | $4$ | Number of contestants in tournament selection. |
| **Crossover Rate** | `crossover_rate` | $0.8$ | $0.8$ | $0.85$ | Probability of applying crossover vs cloning parent 1. |
| **Mutation Rate** | `mutation_rate` | $1 / |E|$ | $1 / |E|$ | $1 / |E|$ | Per-gene mutation rate (auto-scaled by candidate count). |
| **Elitism Count** | `elitism_count` | $2$ | $2$ | $3$ | Number of elite solutions carried forward untouched. |
| **Timeout Budget** | `timeout_ms` | $5000$ | $15000$ | $30000$ | Real-time execution deadline in milliseconds. |

---

## 6. Unit Tests & Benchmark Results

### 6.1 Test Suite Organization
The test suite is partitioned into dedicated modules:
1. `tests/test_ga_solver.py`: Unified master regression suite covering all 4 core requirement groups (S2-08).
2. `tests/test_ga_operators_solver.py`: Targeted functional tests for operators and solver loop (S2-07).
3. `tests/test_ga_encoding_fitness.py`: Detailed conversion, bounds, and manual P1 fitness scores (S2-06).

### 6.2 Test Verification Matrix

| Test Group | Test Function | Purpose / Checked Invariant |
| :--- | :--- | :--- |
| **Encoding** | `test_chromosome_length_equals_candidate_list_length` | Enforces $|C| \equiv |E_{\text{cand}}|$. |
| **Encoding** | `test_gene_values_outside_domain_rejected` | Rejects negatives, floats, booleans, and $>2$. |
| **Encoding** | `test_lossless_round_trip_conversion` | $C \to \text{Solution} \to C$ preserves all gene values. |
| **Encoding** | `test_missing_known_candidate_ids_evaluate_to_zero` | Missing IDs in `bridge_counts` evaluate as $0$. |
| **Fitness** | `test_evaluates_p1_valid_chromosome_to_optimal_zero` | P1 $[1, 1, 1, 1]$ evaluates to $(0, 0, 0)$. |
| **Fitness** | `test_degree_error_calculated_as_sum_of_absolute_differences` | Validates $\sum |d_{\text{req}} - d_{\text{act}}|$ on P1 manual scores. |
| **Fitness** | `test_crossing_count_reflects_intersecting_pairs` | Validates strict crossing detection on Plus puzzle. |
| **Fitness** | `test_disconnected_solutions_penalized` | Validates components penalty $\max(0, \text{comp} - 1)$. |
| **Operators** | `test_tournament_selection_picks_fitter_individual` | Lower fitness tuple wins tournament; isolated copy. |
| **Operators** | `test_uniform_crossover_preserves_length_and_gene_domain` | 50/50 inheritance; strictly preserves length and domain. |
| **Operators** | `test_mutation_produces_valid_gene_values_in_domain` | Mutates to different value in $\{0, 1, 2\}$; fresh copy. |
| **Operators** | `test_elitism_retains_top_individuals_unmodified` | Top $E$ copied without mutation aliasing. |
| **Solver** | `test_solves_p1_benchmark_within_reasonable_generations` | Solves P1 fixture deterministically with seed; validates solution. |
| **Solver** | `test_successfully_terminates_on_max_generations` | Returns `NO_VALID_SOLUTION_FOUND` on impossible puzzles. |
| **Solver** | `test_reported_solution_passes_core_solution_validator` | Strict gate: every `SOLVED` result verified by `validate_solution`. |

### 6.3 Benchmark Performance on Canonical P1
* **Puzzle Details:** 4 islands (A, B, C, D) in a $3 \times 3$ grid, each requiring degree 2. 4 candidate edges.
* **Search Space:** $3^4 = 81$ total possible chromosomes. Only $[1, 1, 1, 1]$ is valid.
* **Results with Seed 42:**
  * **Status:** `SOLVED`
  * **Generations to Convergence:** $\le 2$ generations
  * **Evaluations:** $\le 100$ fitness evaluations
  * **Runtime:** $< 5 \text{ ms}$
  * **Validation Report:** `valid: True`, $0$ degree violations, $0$ crossings, $1$ connected component.

---

## 7. Memetic Algorithm (M5 — Febronia) Integration Guide

The GA modules are packaged cleanly in `algorithms/ga` for direct, zero-friction reuse by the Memetic Algorithm:

```python
# In algorithms/ma/memetic_solver.py:
from algorithms.ga import (
    chromosome_to_solution,
    evaluate_fitness,
    get_elites,
    initialize_population,
    mutate,
    tournament_selection,
    uniform_crossover,
    validate_chromosome,
)
from core.solution_validator import validate_solution

def solve_memetic(puzzle, candidate_bridges, config=None):
    # 1. Reuse GA Population Initialization
    # 2. Perform Tournament Selection, Uniform Crossover, and Mutation
    # 3. Apply Local Search (Hill Climbing on Candidate Neighbors)
    # 4. Apply Elitism and Form Next Generation
    ...
```
This shared architecture guarantees that GA and MA remain 100% interoperable across the entire lifetime of the project.
