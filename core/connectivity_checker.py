"""S1-06 - Connectivity Checker.  Owner: Ebrahim.  Reviewer: Mostafa.

Spec: docs/VALIDATOR_SPEC.md   (BFS or DFS over ACTUAL bridges only: count > 0)
"""
from __future__ import annotations

from typing import Dict, List, Set

from core.models import CandidateBridge, Island, Solution


def find_connected_components(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> List[List[str]]:
    """Return the connected components as lists of island ids.

    Only edges with a bridge count > 0 connect islands (a candidate edge with 0 does not).
    An island with no bridge is its own component. Output order must be deterministic.
    Components are sorted internally and the outer list is sorted by the first element.
    """
    # Build adjacency list using only edges with bridge count > 0
    adj: Dict[str, List[str]] = {isl["id"]: [] for isl in islands}
    for e in edges:
        if solution["bridge_counts"].get(e["id"], 0) > 0:
            adj[e["from"]].append(e["to"])
            adj[e["to"]].append(e["from"])

    # DFS to find components; visit islands in deterministic order (sorted by id)
    visited: Set[str] = set()
    components: List[List[str]] = []

    for isl in sorted(islands, key=lambda x: x["id"]):
        node_id = isl["id"]
        if node_id not in visited:
            # DFS from this island
            component: List[str] = []
            stack: List[str] = [node_id]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                component.append(current)
                for neighbor in adj[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            components.append(sorted(component))

    # Sort components by their first (smallest) element for deterministic output
    components.sort(key=lambda c: c[0])
    return components


def is_connected(
    islands: List[Island], edges: List[CandidateBridge], solution: Solution
) -> bool:
    """True when there is exactly one component."""
    return len(find_connected_components(islands, edges, solution)) == 1
