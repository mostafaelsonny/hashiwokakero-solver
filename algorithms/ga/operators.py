"""GA / MA shared genetic operators (Sprint 2 - S2-07).

Provides modular, constraint-preserving evolutionary operators:
  * tournament_selection: k-way tournament using lexicographical multi-objective fitness.
  * uniform_crossover: gene-by-gene 50/50 selection strictly preserving chromosome length.
  * mutate: per-gene mutation replacing current value with a different value from {0, 1, 2}.
  * get_elites: extracts top E individuals as isolated deep copies (no mutation aliasing).

These operators are designed to be imported directly by Memetic Algorithm (M5).
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    Fitness = Tuple[int, int, int]

VALID_GENES = (0, 1, 2)


def tournament_selection(
    population: List[List[int]],
    fitnesses: List["Fitness"],
    k: int = 3,
    rng: Optional[random.Random] = None,
) -> List[int]:
    """Select one individual from population via k-way tournament selection.

    Competitors are chosen uniformly at random. The individual with the lowest
    (best) lexicographical fitness wins. Returns a fresh copy of the chromosome.

    Args:
        population: List of candidate chromosomes.
        fitnesses: Parallel list of fitness tuples (degree_error, crossings, connectivity).
        k: Tournament size (default: 3).
        rng: Optional random.Random instance for deterministic execution.

    Raises:
        ValueError: If population is empty, lengths mismatch, or k < 1.
    """
    if not population:
        raise ValueError("Cannot perform tournament selection on an empty population.")
    if len(population) != len(fitnesses):
        raise ValueError(
            f"Population size ({len(population)}) does not match fitnesses size ({len(fitnesses)})."
        )
    if k < 1:
        raise ValueError(f"Tournament size k must be >= 1, got {k}.")

    sample_size = min(k, len(population))
    sampler = rng.sample if rng is not None else random.sample
    contestant_indices = sampler(range(len(population)), sample_size)

    best_idx = min(contestant_indices, key=lambda idx: fitnesses[idx])
    return list(population[best_idx])


def uniform_crossover(
    parent1: List[int],
    parent2: List[int],
    rng: Optional[random.Random] = None,
) -> List[int]:
    """Construct one offspring by selecting each gene from parent1 or parent2 with equal probability.

    Strictly preserves parent length, gene domain, and edge-index mapping.

    Args:
        parent1: First parent chromosome.
        parent2: Second parent chromosome.
        rng: Optional random.Random instance for determinism.

    Returns:
        New offspring chromosome (List[int]).

    Raises:
        ValueError: If parents have unequal lengths.
    """
    if len(parent1) != len(parent2):
        raise ValueError(
            f"Parent chromosomes must have equal length, got {len(parent1)} and {len(parent2)}."
        )

    rand = rng.random if rng is not None else random.random
    return [p1 if rand() < 0.5 else p2 for p1, p2 in zip(parent1, parent2)]


def mutate(
    chromosome: List[int],
    mutation_rate: Optional[float] = None,
    rng: Optional[random.Random] = None,
) -> List[int]:
    """Mutate genes with probability mutation_rate.

    When a gene mutates, it is replaced by a randomly chosen DIFFERENT value from {0, 1, 2}.
    Returns a new mutated chromosome list (does not mutate input).

    Args:
        chromosome: Input gene list.
        mutation_rate: Probability of mutation per gene (default: 1 / len(chromosome)).
        rng: Optional random.Random instance for determinism.

    Returns:
        New mutated chromosome (List[int]).

    Raises:
        ValueError: If mutation_rate is outside [0.0, 1.0] or gene value is invalid.
    """
    length = len(chromosome)
    if length == 0:
        return []

    p_mut = (1.0 / length) if mutation_rate is None else mutation_rate
    if not (0.0 <= p_mut <= 1.0):
        raise ValueError(f"mutation_rate must be between 0.0 and 1.0, got {mutation_rate}.")

    rand = rng.random if rng is not None else random.random
    choice = rng.choice if rng is not None else random.choice

    mutated = list(chromosome)
    for i in range(length):
        gene = mutated[i]
        if gene not in VALID_GENES:
            raise ValueError(f"Invalid gene value {gene!r} at index {i}. Must be in {VALID_GENES}.")
        if rand() < p_mut:
            options = [val for val in VALID_GENES if val != gene]
            mutated[i] = choice(options)

    return mutated


def get_elites(
    population: List[List[int]],
    fitnesses: List["Fitness"],
    elitism_count: int = 2,
) -> List[List[int]]:
    """Extract top E individuals according to best (lowest) lexicographical fitness.

    Returns isolated deep copies of chromosomes to prevent downstream mutation aliasing.

    Args:
        population: Current population.
        fitnesses: Parallel list of fitness tuples.
        elitism_count: Number of elite individuals to preserve (default: 2).

    Returns:
        List of copied chromosomes for the elite individuals.

    Raises:
        ValueError: If elitism_count < 0 or lengths mismatch.
    """
    if elitism_count < 0:
        raise ValueError(f"elitism_count must be non-negative, got {elitism_count}.")
    if len(population) != len(fitnesses):
        raise ValueError(
            f"Population size ({len(population)}) does not match fitnesses size ({len(fitnesses)})."
        )
    if elitism_count == 0 or not population:
        return []

    count = min(elitism_count, len(population))
    sorted_indices = sorted(range(len(population)), key=lambda idx: fitnesses[idx])
    return [list(population[idx]) for idx in sorted_indices[:count]]
