import pyomo.environ as pyo
import pandas as pd
from typing import Dict


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
        "selector": '[type = "supply"]',
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
    print(result)
    elements = []
    for entity, x_pos in zip(["supply", "demand"], [0, 200]):
        materials = []
        for i, entity_dct in enumerate(result[entity]):
            # materials.append(entity_dct["material_id"])
            elements.append({"data": {"id": entity_dct["node_id"], "material": entity_dct["material_id"], "label": entity_dct["node_id"], "type": entity, "value": entity_dct["value"]}, "position": {"x": x_pos, "y": 100 * i}})

    for transport in result["transport"]:
        elements.append(
            {
                "data": {
                    "id": f"{transport["from_node_id"]}|{transport["to_node_id"]}",
                    "source": f"{transport["from_node_id"]}",
                    "target": f"{transport["to_node_id"]}",
                }
            }
        )

    return elements

def extract_solution(model: pyo.ConcreteModel) -> Dict[str, pd.DataFrame]:
    supply = pd.DataFrame([{"material_id": s, "node_id": n, "value": pyo.value(value), "cost": pyo.value(model.supply_cost[s, n])} for (s, n), value in model.supply.items()])
    demand = pd.DataFrame([{"material_id": s, "node_id": n, "value": pyo.value(value), "price": pyo.value(model.demand_price[s, n])} for (s, n), value in model.demand.items()])
    transport = pd.DataFrame([{"material_id": s, "from_node_id": n1, "to_node_id": n2, "value": pyo.value(value), "cost": pyo.value(model.transport_cost[s, n1, n2])} for (s, n1, n2), value in model.transport.items()])
    distress_sale = pd.DataFrame([{"material_id": s, "node_id": n, "value": pyo.value(value), "cost": pyo.value(model.distress_cost)} for (s, n), value in model.distress_sale.items()])
    distress_purchase = pd.DataFrame([{"material_id": s, "node_id": n, "value": pyo.value(value), "cost": pyo.value(model.distress_cost)} for (s, n), value in model.distress_purchase.items()])

    return {"supply": supply, "demand": demand, "transport": transport, "distress_sale": distress_sale, "distress_purchase": distress_purchase}

def aggregate_for_visualization(result: Dict[str, pd.DataFrame]):
    all_nodes = result["distress_sale"].node_id.unique()

    nodes_data = [{"id": node, "supply": result["supply"][result["supply"].node_id == node].set_index("node_id").to_dict(orient="records"), "demand": result["demand"][result["demand"].node_id == node].set_index("node_id").to_dict(orient="records"), "distress_sale": result["distress_sale"][result["distress_sale"].node_id == node].set_index("node_id").to_dict(orient="records"), "distress_purchase": result["distress_purchase"][result["distress_purchase"].node_id == node].set_index("node_id").to_dict(orient="records")} for node in all_nodes]

    edges_data = []

    return {"nodes": nodes_data, "edges": edges_data}

