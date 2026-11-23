from dataclasses import dataclass, field
from typing import Any, Dict, List, Union


@dataclass
class GraphContext:
    incident_edges_by_island: Dict[str, List[Union[int, str]]] = field(default_factory=dict)
    crossings: Any = field(default_factory=dict)
