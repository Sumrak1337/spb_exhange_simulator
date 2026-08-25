from dash import html, Dash, Output, Input
import dash_cytoscape as cyto
from ui.utils import make_stylesheet, make_elements

def visualization_callbacks(app: Dash):
    @app.callback(
        Output("node-info", "children"),
        Input("cytoscape-network", "mouseoverNodeData")
    )
    def show_node_info(node_data):
        if not node_data:
            return ""
        return [
            html.B(node_data["label"]),
            html.Br(),
            # html.Div(f"Supply: {node_data["value"]}")
            html.Div(f"{node_data}")
        ]


    @app.callback(
        Output("network-container", "children"),
        Input("model-results-storage", "data"),
        Input("view-mode", "value")
    )
    def render_graph(result, view_mode):
        if result is None:
            return cyto.Cytoscape()

        elements = [{"label": node["id"], "type": "supply" if node["supply"] else "demand", **node} for node in result["nodes"]]

        if view_mode == "network":
            network = cyto.Cytoscape(
                id="cytoscape-network",
                elements=elements,
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

