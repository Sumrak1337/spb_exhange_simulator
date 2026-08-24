import json

from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
from ui.layout import build_layout
from ui.callbacks.optimization import optimization_callback
from ui.callbacks.visualization import visualization_callbacks

def make_elements(result):
    elements = [
        {
            "data": {
                "id": "P1",
                "label": "P1\nProduction",
                "type": "production",
            },
            "position": {"x": 100, "y": 150},
        },
        {
            "data": {
                "id": "P2",
                "label": "P2\nProduction",
                "type": "production",
            },
            "position": {"x": 100, "y": 400},
        },
        {
            "data": {
                "id": "T1",
                "label": "T1\nTransfer",
                "type": "transfer",
            },
            "position": {"x": 400, "y": 150},
        },
        {
            "data": {
                "id": "T2",
                "label": "T2\nTransfer",
                "type": "transfer",
            },
            "position": {"x": 400, "y": 400},
        },
        {
            "data": {
                "id": "D1",
                "label": "D1\nDemand",
                "type": "demand",
            },
            "position": {"x": 700, "y": 150},
        },
        {
            "data": {
                "id": "D2",
                "label": "D2\nDemand",
                "type": "demand",
            },
            "position": {"x": 700, "y": 400},
        },
    ]

    for flow in result["flows"]:
        elements.append(
            {
                "data": {
                    "id": flow["id"],
                    "source": flow["source"],
                    "target": flow["target"],
                    "flow": round(flow["flow"]),
                    "capacity": flow["capacity"],
                    "label": (
                        f'{flow["flow"]:,.0f} t '
                        f'({flow["flow"] / flow["capacity"]:.0%})'
                    ),
                }
            }
        )

    return elements

def get_edge_color(flow, capacity):

    utilization = flow / capacity if capacity else 0

    if utilization >= 0.9:
        return "#dc2626"       # red
    elif utilization >= 0.7:
        return "#f59e0b"       # yellow
    else:
        return "#16a34a"       # green


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

        color = get_edge_color(
            flow["flow"],
            flow["capacity"],
        )

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

def solve_mock(demand_d1, demand_d2, production_p1, production_p2):
    total_demand = demand_d1 + demand_d2
    total_production = production_p1 + production_p2

    # Capacities of transfer nodes
    cap_t1 = 7000
    cap_t2 = 6000

    # Available production
    p1 = production_p1
    p2 = production_p2

    # --------------------------------------------------------
    # Простая имитация оптимального распределения
    # --------------------------------------------------------

    # Сначала пытаемся закрыть D1 через T1
    d1_from_p1 = min(p1, demand_d1 * 0.65)
    d1_from_p2 = min(p2, demand_d1 - d1_from_p1)

    # Остаток D1
    d1_served = d1_from_p1 + d1_from_p2
    # D2 получает оставшуюся продукцию
    remaining_p1 = max(0, p1 - d1_from_p1)
    remaining_p2 = max(0, p2 - d1_from_p2)

    d2_from_p1 = min(remaining_p1, demand_d2 * 0.55)
    d2_from_p2 = min(remaining_p2, demand_d2 - d2_from_p1)

    d2_served = d2_from_p1 + d2_from_p2

    # --------------------------------------------------------
    # Ограничиваем transfer capacities
    # --------------------------------------------------------

    t1_flow = min(d1_served, cap_t1)

    # Если T1 ограничил поток, часть D1 не обслужена
    d1_served = t1_flow

    t2_flow = min(d2_served, cap_t2)
    d2_served = t2_flow

    unmet = total_demand - d1_served - d2_served

    # --------------------------------------------------------
    # Потоки для визуализации
    # --------------------------------------------------------

    flows = [
        {
            "id": "p1-t1",
            "source": "P1",
            "target": "T1",
            "flow": d1_from_p1,
            "capacity": cap_t1,
        },
        {
            "id": "p2-t1",
            "source": "P2",
            "target": "T1",
            "flow": max(0, t1_flow - d1_from_p1),
            "capacity": cap_t1,
        },
        {
            "id": "t1-d1",
            "source": "T1",
            "target": "D1",
            "flow": d1_served,
            "capacity": cap_t1,
        },
        {
            "id": "p1-t2",
            "source": "P1",
            "target": "T2",
            "flow": d2_from_p1,
            "capacity": cap_t2,
        },
        {
            "id": "p2-t2",
            "source": "P2",
            "target": "T2",
            "flow": max(0, t2_flow - d2_from_p1),
            "capacity": cap_t2,
        },
        {
            "id": "t2-d2",
            "source": "T2",
            "target": "D2",
            "flow": d2_served,
            "capacity": cap_t2,
        },
    ]

    # Условная стоимость
    total_flow = d1_served + d2_served

    cost = (
        d1_from_p1 * 110
        + d1_from_p2 * 130
        + d2_from_p1 * 120
        + d2_from_p2 * 140
    )

    utilization = (
        total_flow / total_production
        if total_production > 0
        else 0
    )

    return {
        "flows": flows,
        "cost": cost,
        "unmet": max(0, unmet),
        "total_demand": total_demand,
        "total_flow": total_flow,
        "utilization": utilization,
    }


app = Dash(__name__, suppress_callback_exceptions=True)

with open("input_data/input_data.json", "r", encoding="utf-8") as file:
    main_data = json.load(file)

print("=" * 50)
app.layout = build_layout(main_data)

visualization_callbacks(app=app)
optimization_callback(app=app, main_data=main_data)

# @app.callback(
    # Output("network-container", "children"),
    # Output("kpi-bar", "children"),
    # Output("supply-bounds-value", "children"),
    # Output("supply-cost-value", "children"),
    # Output("production-p1-value", "children"),
    # Output("production-p2-value", "children"),
    # Input("supply-npz-bounds", "value"),
    # Input("supply-npz-cost", "value"),
    # Input("demand-sp-bounds", "value"),
    # Input("demand-sp-price", "value"),
    # Input("demand-spbe-bounds", "value"),
    # Input("demand-spbe-price", "value"),
    # Input("view-mode", "value")
# )
def update_dashboard(
    supply_npz_bounds,
    supply_npz_cost,
    demand_sp_bounds,
    demand_sp_price,
    demand_spbe_bounds,
    demand_spbe_price,
    view_mode,
):
    return
    result = solve_mock(
        supply_bounds,
        supply_cost,
        production_p1,
        production_p2,
    )

    # if view_mode == "network":
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

    # else:
        # network = dcc.Graph(
        #     figure=make_sankey(result),
        #     config={
        #         "displayModeBar": False,
        #     },
        # )

    return (
        network,
        # kpis,
        f"{supply_bounds:,.0f} t",
        f"{supply_cost:,.0f} t",
        f"{production_p1:,.0f} t",
        f"{production_p2:,.0f} t",
    )

if __name__ == "__main__":
    app.run(debug=True)
