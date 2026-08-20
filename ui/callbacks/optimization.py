from dash import Dash, Input

from domain.data import OptimizationInput


def optimization_callback(app: Dash):
    @app.callback(
        Input("supply-npz-bounds-value", "value"),
        # Input("supply-npz-cost", "value"),
        # Input("demand-sp-bounds", "value"),
        # Input("demand-sp-price", "value"),
        # Input("demand-spbe-bounds", "value"),
        # Input("demand-spbe-price", "value"),
    )
    def optimization(
        supply_npz_bounds,
        # supply_npz_cost,
        # demand_sp_bounds,
        # demand_sp_price,
        # demand_spbe_bounds,
        # demand_spbe_price,
    ):
        # Data creation
        pass

        # data = OptimizationInput(supply_min=supply_min,)

