import pandas as pd
from dash import Dash, Input, Output, ALL, State
import pyomo.environ as pyo

from domain.data import OptimizationInput
from typing import Dict, Any
from optimization.model import LogisticsModel
from optimization.solver import SolverManager
from ui.utils import extract_solution, aggregate_for_visualization

def optimization_callback(app: Dash, main_data: Dict[str, Any]):
    @app.callback(
        Output("model-results-storage", "data"),
        Input({"type": "supply-range-slider", "s": ALL, "n": ALL}, "value"),
        Input({"type": "demand-range-slider", "s": ALL, "n": ALL}, "value"),
        Input({"type": "supply-number-input", "s": ALL, "n": ALL}, "value"),
        Input({"type": "demand-number-input", "s": ALL, "n": ALL}, "value"),
        State({"type": "supply-range-slider", "s": ALL, "n": ALL}, "id"),
        State({"type": "demand-range-slider", "s": ALL, "n": ALL}, "id"),
        State({"type": "supply-number-input", "s": ALL, "n": ALL}, "id"),
        State({"type": "demand-number-input", "s": ALL, "n": ALL}, "id"),
    )
    def optimization(
        supply_bounds,
        demand_bounds,
        supply_cost,
        demand_price,
        supply_bounds_ids,
        demand_bounds_ids,
        supply_cost_ids,
        demand_price_ids,
    ):
        # Data creation
        # TODO: to separate function
        data = OptimizationInput()

        demand_min = []
        supply_min = []
        transport_min = []
        supply_max = []
        demand_max = []
        transport_max = []
        supply_cost_lst = []
        demand_price_lst = []
        transport_cost_lst = []

        for ids, bounds in zip(supply_bounds_ids, supply_bounds):
            supply_min.append({"s": ids["s"], "n": ids["n"], "value": bounds[0]})
            supply_max.append({"s": ids["s"], "n": ids["n"], "value": bounds[1]})

        for ids, bounds in zip(demand_bounds_ids, demand_bounds):
            demand_min.append({"s": ids["s"], "n": ids["n"], "value": bounds[0]})
            demand_max.append({"s": ids["s"], "n": ids["n"], "value": bounds[1]})

        for ids, cost in zip(supply_cost_ids, supply_cost):
            cost = 0 if cost is None else cost
            supply_cost_lst.append({"s": ids["s"], "n": ids["n"], "value": cost})

        for ids, price in zip(demand_price_ids, demand_price):
            price = 0 if price is None else price
            demand_price_lst.append({"s": ids["s"], "n": ids["n"], "value": price})

        for item in main_data["transport"]:
            transport_min.append({"s": item["material_id"], "n1": item["from_node_id"], "n2": item["to_node_id"], "value": item["min"]})
            transport_max.append({"s": item["material_id"], "n1": item["from_node_id"], "n2": item["to_node_id"], "value": item["max"]})
            transport_cost_lst.append({"s": item["material_id"], "n1": item["from_node_id"], "n2": item["to_node_id"], "value": item["cost"]})

        data.supply_min = pd.DataFrame(supply_min)
        data.supply_max = pd.DataFrame(supply_max)
        data.demand_min = pd.DataFrame(demand_min)
        data.demand_max = pd.DataFrame(demand_max)
        data.supply_cost = pd.DataFrame(supply_cost_lst)
        data.demand_price = pd.DataFrame(demand_price_lst)
        data.transport_min = pd.DataFrame(transport_min)
        data.transport_max = pd.DataFrame(transport_max)
        data.transport_cost = pd.DataFrame(transport_cost_lst)

        # Model building
        model = LogisticsModel(data=data)
        model.build()

        solver = SolverManager()
        solver.solve(model=model)

        # Result extracting
        result = extract_solution(model=model)
        return aggregate_for_visualization(result=result)
        result = {
            "supply": [{"material_id": s, "node_id": n, "value": pyo.value(v)} for (s, n), v in model.supply.items()],
            "demand": [{"material_id": s, "node_id": n, "value": pyo.value(v)} for (s, n), v in model.demand.items()],
            "transport": [{"material_id": s, "from_node_id": n1, "to_node_id": n2, "value": pyo.value(v)} for (s, n1, n2), v in model.transport.items()],
            "distress_sale": [{"material_id": s, "node_id": n, "value": pyo.value(v)} for (s, n), v in model.distress_sale.items()],
            "distress_purchase": [{"material_id": s, "node_id": n, "value": pyo.value(v)} for (s, n), v in model.distress_purchase.items()],
        }
        return result
