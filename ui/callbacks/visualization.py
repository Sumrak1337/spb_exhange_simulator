from dash import html, Dash, Output, Input

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
            html.Div(f"Supply: {node_data["value"]}")
        ]

