from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class OptimizationInput:
    supply_min: Dict[Tuple[str], float]
    supply_max: Dict[Tuple[str], float]
    supply_cost: Dict[Tuple[str], float]

    demand_min: Dict[Tuple[str], float]
    demand_max: Dict[Tuple[str], float]
    demand_price: Dict[Tuple[str], float]

    transport_min: Dict[Tuple[str], float]
    transport_max: Dict[Tuple[str], float]
    transport_cost: Dict[Tuple[str], float]
