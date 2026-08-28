import dash_cytoscape as cyto
from dash import Dash, Input, Output, html

from ui.utils.utils import make_stylesheet


def visualization_callbacks(app: Dash):
    @app.callback(
        Output("node-info", "children"),
        Input("cytoscape-network", "mouseoverNodeData"),
    )
    def show_node_info(node_data):
        if not node_data:
            return ""

        return [
            html.H3(node_data["label"]),
            *[
                html.Div(
                    [
                        html.B(f"{node['material_id']} "),
                        html.Span(
                            f"{node['value']}", style={"color": "green"}
                        ),
                        " || ",
                        "Penalty purchase: ",
                        html.Span(
                            f"{node['value_distress_purchase']}",
                            style={"color": "red"},
                        ),
                        " || ",
                        "Penalty sale: ",
                        html.Span(
                            f"{node['value_distress_sale']}",
                            style={"color": "red"},
                        ),
                    ]
                )
                for node in node_data["activity"]
            ],
        ]

    @app.callback(
        Output("network-container", "children"),
        Input("model-results-storage", "data"),
        Input("colors", "data"),
        Input("view-mode", "value"),
    )
    def render_graph(result, colors, view_mode):
        if result is None:
            return cyto.Cytoscape()

        elements = []
        for node in result["nodes"]:
            if node["supply"]:
                activity = node["supply"]
                node_type = "supply"
            else:
                activity = node["demand"]
                node_type = "demand"
            elements.append(
                {
                    "data": {
                        "id": node["id"],
                        "label": node["id"],
                        "type": node_type,
                        "activity": activity,
                    }
                }
            )
        elements.extend(
            {"data": {"color": colors[edge["product"]], **edge}}
            for edge in result["edges"]
        )

        if view_mode == "network":
            network = cyto.Cytoscape(
                id="cytoscape-network",
                elements=elements,
                stylesheet=make_stylesheet(),
                layout={
                    "name": "breadthfirst",
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
