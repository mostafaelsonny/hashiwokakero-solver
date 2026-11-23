"""Core Graph Engine Context (S2 - M2).

Provides pre-computed incident edge mappings and geometric crossing adjacency
maps derived from the canonical, deterministic CandidateBridge[] list.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from core.crossing_detector import _build_island_map, _would_cross
from core.models import CandidateBridge, Island, Puzzle



@dataclass
class GraphContext:
    """Pre-computed graph lookups for search and optimization algorithms."""

    islands_by_id: Dict[str, Island]
    candidate_bridges: List[CandidateBridge]
    incident_edges_by_island: Dict[str, List[int]] = field(default_factory=dict)
    crossing_edges_by_index: Dict[int, List[int]] = field(default_factory=dict)

    def get_incident_edges(self, island_id: str) -> List[int]:
        """Return a copy of candidate bridge indices incident to `island_id`."""
        return list(self.incident_edges_by_island.get(island_id, []))

    def get_crossing_edges(self, edge_index: int) -> List[int]:
        """Return a copy of candidate bridge indices that geometrically cross `edge_index`."""
        return list(self.crossing_edges_by_index.get(edge_index, []))

    def would_edges_cross(self, edge_index_a: int, edge_index_b: int) -> bool:
        """Return True if candidate bridges at `edge_index_a` and `edge_index_b` cross."""
        return edge_index_b in self.crossing_edges_by_index.get(edge_index_a, [])

    def max_possible_degree(self, island_id: str) -> int:
        """Maximum degree reachable if every incident candidate bridge has count 2."""
        return 2 * len(self.get_incident_edges(island_id))



def build_graph_context(
    puzzle: Puzzle, candidate_bridges: List[CandidateBridge]
) -> GraphContext:
    """Build pre-computed graph context without mutating or reordering bridges."""
    islands: List[Island] = puzzle["islands"]
    islands_by_id = _build_island_map(islands)

    # 1. Initialize incident_edges_by_island for all islands
    incident_edges_by_island: Dict[str, List[int]] = {
        island["id"]: [] for island in islands
    }

    for idx, edge in enumerate(candidate_bridges):
        from_id = edge["from"]
        to_id = edge["to"]
        if from_id in incident_edges_by_island:
            incident_edges_by_island[from_id].append(idx)
        if to_id in incident_edges_by_island:
            incident_edges_by_island[to_id].append(idx)

    # 2. Initialize crossing_edges_by_index for all candidate bridges
    num_edges = len(candidate_bridges)
    crossing_edges_by_index: Dict[int, List[int]] = {i: [] for i in range(num_edges)}

    for i in range(num_edges):
        for j in range(i + 1, num_edges):
            if _would_cross(candidate_bridges[i], candidate_bridges[j], islands_by_id):
                crossing_edges_by_index[i].append(j)
                crossing_edges_by_index[j].append(i)

    return GraphContext(
        islands_by_id=islands_by_id,
        candidate_bridges=candidate_bridges,
        incident_edges_by_island=incident_edges_by_island,
        crossing_edges_by_index=crossing_edges_by_index,
    )