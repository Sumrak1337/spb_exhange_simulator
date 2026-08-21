from dataclasses import dataclass, field
import pandas as pd

@dataclass
class OptimizationInput:
    supply_min: pd.DataFrame = field(default_factory=pd.DataFrame)
    supply_max: pd.DataFrame = field(default_factory=pd.DataFrame)
    supply_cost: pd.DataFrame = field(default_factory=pd.DataFrame)

    demand_min: pd.DataFrame = field(default_factory=pd.DataFrame)
    demand_max: pd.DataFrame = field(default_factory=pd.DataFrame)
    demand_price: pd.DataFrame = field(default_factory=pd.DataFrame)

    transport_min: pd.DataFrame = field(default_factory=pd.DataFrame)
    transport_max: pd.DataFrame = field(default_factory=pd.DataFrame)
    transport_cost: pd.DataFrame = field(default_factory=pd.DataFrame)
