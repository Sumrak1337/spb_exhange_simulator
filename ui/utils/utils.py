from typing import Any, Dict, List

import pandas as pd
import pyomo.environ as pyo

from domain.data import OptimizationInput
from ui.utils.config_data import NODE_COLORS, PRODUCT_COLORS


def data_creation(
    *,
    supply_bounds,
    demand_bounds,
    supply_cost,
    demand_price,
    supply_bounds_ids,
    demand_bounds_ids,
    supply_cost_ids,
    demand_price_ids,
    main_data,
) -> OptimizationInput:
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
        transport_min.append(
            {
                "s": item["material_id"],
                "n1": item["from_node_id"],
                "n2": item["to_node_id"],
                "value": item["min"],
            }
        )
        transport_max.append(
            {
                "s": item["material_id"],
                "n1": item["from_node_id"],
                "n2": item["to_node_id"],
                "value": item["max"],
            }
        )
        transport_cost_lst.append(
            {
                "s": item["material_id"],
                "n1": item["from_node_id"],
                "n2": item["to_node_id"],
                "value": item["cost"],
            }
        )

    data.supply_min = pd.DataFrame(supply_min)
    data.supply_max = pd.DataFrame(supply_max)
    data.demand_min = pd.DataFrame(demand_min)
    data.demand_max = pd.DataFrame(demand_max)
    data.supply_cost = pd.DataFrame(supply_cost_lst)
    data.demand_price = pd.DataFrame(demand_price_lst)
    data.transport_min = pd.DataFrame(transport_min)
    data.transport_max = pd.DataFrame(transport_max)
    data.transport_cost = pd.DataFrame(transport_cost_lst)

    return data


def make_stylesheet() -> List[Dict[str, Any]]:
    stylesheet = [
        {
            "selector": "node",
            "style": {
                "content": "data(label)",
                "width": 70,
                "height": 70,
                "text-wrap": "wrap",
                "font-size": "10px",
                "text-valign": "center",
                "text-halign": "center",
                "color": "#0c2a45",
                "font-weight": "bold",
                "label-font": "sans-serif",
            },
        },
        {
            "selector": '[type = "supply"]',
            "style": {
                "background-color": NODE_COLORS["supply"],
                "color": "white",
                "shape": "rectangle",
            },
        },
        {
            "selector": '[type = "demand"]',
            "style": {
                "background-color": NODE_COLORS["demand"],
                "shape": "ellipse",
            },
        },
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "line-color": "data(color)",
                "target-arrow-color": "data(color)",
                "arrow-scale": 0.75,
                "label": "data(label)",
                "font-size": "11px",
                "text-background-color": "#ffffff",
                "text-background-opacity": 0.5,
                "text-background-padding": "3px",
            },
        },
    ]

    return stylesheet


def extract_solution(model: pyo.ConcreteModel) -> Dict[str, pd.DataFrame]:
    supply = pd.DataFrame(
        [
            {
                "material_id": s,
                "node_id": n,
                "value": pyo.value(value),
                "cost": pyo.value(model.supply_cost[s, n]),
            }
            for (s, n), value in model.supply.items()
        ]
    )
    demand = pd.DataFrame(
        [
            {
                "material_id": s,
                "node_id": n,
                "value": pyo.value(value),
                "price": pyo.value(model.demand_price[s, n]),
            }
            for (s, n), value in model.demand.items()
        ]
    )
    transport = pd.DataFrame(
        [
            {
                "material_id": s,
                "from_node_id": n1,
                "to_node_id": n2,
                "value": pyo.value(value),
                "cost": pyo.value(model.transport_cost[s, n1, n2]),
            }
            for (s, n1, n2), value in model.transport.items()
        ]
    )
    distress_sale = pd.DataFrame(
        [
            {
                "material_id": s,
                "node_id": n,
                "value": pyo.value(value),
                "cost": pyo.value(model.distress_cost),
            }
            for (s, n), value in model.distress_sale.items()
        ]
    )
    distress_purchase = pd.DataFrame(
        [
            {
                "material_id": s,
                "node_id": n,
                "value": pyo.value(value),
                "cost": pyo.value(model.distress_cost),
            }
            for (s, n), value in model.distress_purchase.items()
        ]
    )

    return {
        "supply": supply,
        "demand": demand,
        "transport": transport,
        "distress_sale": distress_sale,
        "distress_purchase": distress_purchase,
    }


def aggregate_for_visualization(result: Dict[str, pd.DataFrame]):
    all_nodes = result["distress_sale"].node_id.unique()
    all_products = sorted(result["distress_sale"].material_id.unique())

    colors = {
        product: PRODUCT_COLORS[i % len(PRODUCT_COLORS)]
        for i, product in enumerate(all_products)
    }

    distress = result["distress_purchase"].merge(
        result["distress_sale"],
        on=["material_id", "node_id"],
        how="outer",
        suffixes=("_distress_purchase", "_distress_sale"),
    )
    supply = result["supply"].merge(distress, on=["material_id", "node_id"])
    demand = result["demand"].merge(distress, on=["material_id", "node_id"])
    nodes_data = [
        {
            "id": node,
            "supply": supply[supply.node_id == node]
            .set_index("node_id")
            .to_dict(orient="records"),
            "demand": demand[demand.node_id == node]
            .set_index("node_id")
            .to_dict(orient="records"),
        }
        for node in all_nodes
    ]

    edges_data = [
        {
            "id": f"{flow['material_id']}"
            f"|{flow['from_node_id']}"
            f"|{flow['to_node_id']}",
            "product": flow["material_id"],
            "source": flow["from_node_id"],
            "target": flow["to_node_id"],
            "label": f"{flow['value']}",
        }
        for flow in result["transport"].to_dict(orient="records")
    ]

    return {"nodes": nodes_data, "edges": edges_data}, colors
