from typing import Any, Dict

from dash import ALL, Dash, Input, Output, State

from optimization.model import LogisticsModel
from optimization.solver import SolverManager
from ui.utils.utils import (
    aggregate_for_visualization,
    data_creation,
    extract_solution,
)


def optimization_callback(app: Dash, main_data: Dict[str, Any]):
    @app.callback(
        Output("model-results-storage", "data"),
        Output("colors", "data"),
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
        data = data_creation(
            supply_bounds=supply_bounds,
            demand_bounds=demand_bounds,
            supply_cost=supply_cost,
            demand_price=demand_price,
            supply_bounds_ids=supply_bounds_ids,
            demand_bounds_ids=demand_bounds_ids,
            supply_cost_ids=supply_cost_ids,
            demand_price_ids=demand_price_ids,
            main_data=main_data,
        )

        # Model building
        model = LogisticsModel(data=data)
        model.build()

        solver = SolverManager()
        solver.solve(model=model)

        # Result extracting
        result = extract_solution(model=model)

        return aggregate_for_visualization(result=result)
