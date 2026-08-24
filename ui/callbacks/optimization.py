import pandas as pd
from dash import Dash, Input, Output, ALL, State, dcc
import dash_cytoscape as cyto
import pyomo.environ as pyo
import numpy as np

from domain.data import OptimizationInput
from typing import Dict, Any
from optimization.model import LogisticsModel
from optimization.solver import SolverManager

def make_stylesheet(result):

    stylesheet = [{
        "selector": "node",
        "style": {
            "content": "data(label)",
            "width": 70,
            "height": 70,
            "text-wrap": "wrap",
            "font-size": "10px",
            "text-valign": "center",
            "text-halign": "center",
            "color": "black",
            "font-weight": "bold",
            "label-font": "sans-serif"
        },
    }, {
        "selector": '[type = "production"]',
        "style": {
            "background-color": "#2CA02C",
            "shape": "rectangle",
        },
    }, {
        "selector": '[type = "demand"]',
        "style": {
            "background-color": "#D62728",
            "shape": "ellipse",
        },
    }, {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "line-color": "#9467BD",
            "target-arrow-color": "#9467BD",
            "arrow-scale": 0.75,
            "label": "data(label)",
            "font-size": "11px",
            "text-background-color": "#ffffff",
            "text-background-opacity": 0.5,
            "text-background-padding": "3px",
        },
    }]

    return stylesheet

def make_elements(result):
    # TODO: make via nodes, not variables
    import random
    random.seed(42)

    elements = []
    for i, ((s, n), value) in enumerate(result["supply"].items()):
        elements.append({"data": {"id": f"{s}|{n}", "material": s, "label": n, "type": "production", "value": value}, "position": {"x": 0, "y": 100 * i}})
    for i, ((s, n), value) in enumerate(result["demand"].items()):
        elements.append({"data": {"id": f"{s}|{n}", "material": s, "label": n, "type": "demand", "value": value}, "position": {"x": 200, "y": 100 * i}})

    for (s, n1, n2), value in result["transport"].items():
        elements.append(
            {
                "data": {
                    "id": f"{s}{n1}-{n2}",
                    "source": f"{s}|{n1}",
                    "target": f"{s}|{n2}",
                    "label": f'{value:,.0f} тонн',
                }
            }
        )

    return elements

def optimization_callback(app: Dash, main_data: Dict[str, Any]):
    @app.callback(
        Output("network-container", "children"),
        Input({"type": "supply-range-slider", "s": ALL, "n": ALL}, "value"),
        Input({"type": "demand-range-slider", "s": ALL, "n": ALL}, "value"),
        Input({"type": "supply-number-input", "s": ALL, "n": ALL}, "value"),
        Input({"type": "demand-number-input", "s": ALL, "n": ALL}, "value"),
        State({"type": "supply-range-slider", "s": ALL, "n": ALL}, "id"),
        State({"type": "demand-range-slider", "s": ALL, "n": ALL}, "id"),
        State({"type": "supply-number-input", "s": ALL, "n": ALL}, "id"),
        State({"type": "demand-number-input", "s": ALL, "n": ALL}, "id"),
        Input("view-mode", "value")
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
        view_mode,
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
        result = {"supply": {k: pyo.value(v) for k, v in model.supply.items()},
                  "demand": {k: pyo.value(v) for k, v in model.demand.items()},
                  "transport": {k: pyo.value(v) for k, v in model.transport.items()},
                  "distress_sale": {k: pyo.value(v) for k, v in
                                    model.distress_sale.items()},
                  "distress_purchase": {k: pyo.value(v) for k, v in
                                        model.distress_purchase.items()}}

        if view_mode == "network":
            network = cyto.Cytoscape(
                id="cytoscape-network",
                elements=make_elements(result),
                stylesheet=make_stylesheet(result),
                layout={
                    "name": "preset",
                },
                style={
                    "width": "100%",
                    "height": "550px",
                    "backgroundColor": "#ffffff",
                },
            )
        else:
            # Future sankey realization
            network = cyto.Cytoscape()

        return network
