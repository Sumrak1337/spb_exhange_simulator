import pandas as pd
from dash import Dash, Input, Output, ALL, State
import dash_cytoscape as cyto

from domain.data import OptimizationInput
from typing import Dict, Any
from optimization.model import LogisticsModel
from optimization.solver import SolverManager

def make_stylesheet(result):

    stylesheet = [
        # ----------------------------------------------------
        # Nodes
        # ----------------------------------------------------
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
                "width": 70,
                "height": 70,
                "font-size": "13px",
                "text-valign": "center",
                "text-halign": "center",
                "color": "white",
                "font-weight": "bold",
                "border-width": 2,
                "border-color": "#ffffff",
            },
        },

        {
            "selector": '[type = "production"]',
            "style": {
                "background-color": "#2563eb",
                "shape": "rectangle",
            },
        },

        {
            "selector": '[type = "transfer"]',
            "style": {
                "background-color": "#f59e0b",
                "shape": "diamond",
            },
        },

        {
            "selector": '[type = "demand"]',
            "style": {
                "background-color": "#16a34a",
                "shape": "ellipse",
            },
        },

        # ----------------------------------------------------
        # Edges
        # ----------------------------------------------------
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "arrow-scale": 1.2,
                "label": "data(label)",
                "font-size": "11px",
                "text-background-color": "#ffffff",
                "text-background-opacity": 0.9,
                "text-background-padding": "3px",
            },
        },
    ]

    # Individual edge styling
    for flow in result["flows"]:
        color = "tab:green"
        # color = get_edge_color(
        #     flow["flow"],
        #     flow["capacity"],
        # )

        # Minimum width so zero flows remain visible
        width = max(
            2,
            min(
                16,
                2 + 14 * flow["flow"] / flow["capacity"]
            ),
        )

        stylesheet.append(
            {
                "selector": f'#{flow["id"]}',
                "style": {
                    "line-color": color,
                    "target-arrow-color": color,
                    "width": width,
                },
            }
        )

    return stylesheet


def optimization_callback(app: Dash, main_data: Dict[str, Any]):
    @app.callback(
        # Output("network-container", "value"),
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

        model.pprint()

        # data_preprocessing(supply_bounds, supply_bounds_ids, demand_bounds, demand_bounds_ids, supply_cost, supply_cost_ids, demand_price, demand_price_ids, data)

        # network = cyto.Cytoscape(
        #     id="cytoscape-network",
        #     elements=make_elements(result),
        #     stylesheet=make_stylesheet(result),
        #     layout={
        #         "name": "preset",
        #     },
        #     style={
        #         "width": "100%",
        #         "height": "550px",
        #         "backgroundColor": "#ffffff",
        #     },
        # )

        # data = OptimizationInput(supply_min=supply_min,)

