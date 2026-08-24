from dash import html, dcc
from typing import Dict, Any

def build_layout(data: Dict[str, Any]):
    return html.Div(
        [
            build_header(),
            # *build_kpi_bar(),
            build_main_content(data=data)
        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": "#f1f5f9",
            "minHeight": "100vh",
        }
    )
    app.layout = html.Div(
        [

            # ====================================================
            # HEADER
            # ====================================================
            html.Div([html.H1("Logistics Network Optimizer",
                              style={"margin": "0", "fontSize": "28px", }, ),
                      html.Div("Интерактивный симулятор биржевых обязательств",
                               style={"color": "#64748b",
                                      "marginTop": "5px", }, ), ],
                     style={"padding": "20px 30px",
                            "borderBottom": "1px solid #e2e8f0",
                            "backgroundColor": "white", }, ),

            # ====================================================
            # KPI BAR
            # ====================================================

            html.Div(id="kpi-bar",style={"display": "flex","gap": "20px","padding": "15px 30px","backgroundColor": "#f8fafc",},),

            # ====================================================
            # MAIN CONTENT
            # ====================================================

            html.Div(
                [

                    # ------------------------------------------------
                    # LEFT: NETWORK
                    # ------------------------------------------------

                    html.Div([
                        html.Div([
                            html.H3("Network", style={"margin": "0"}, ),
                            dcc.RadioItems(id="view-mode", options=[
                                {"label": " Network", "value": "network", },
                                {"label": " Sankey", "value": "sankey", }, ],
                                           value="network", inline=True,
                                           style={"marginTop": "10px"}, ), ],
                            style={"display": "flex",
                                   "justifyContent": "space-between",
                                   "alignItems": "flex-start",
                                   "marginBottom": "10px", }, ),
                        html.Div(id="network-container", ), ],style={"flex": "1", "backgroundColor": "white","padding": "20px", "borderRadius": "10px", }, ),

                    # ------------------------------------------------
                    # RIGHT: PARAMETERS
                    # ------------------------------------------------

                    html.Div([main_parameter_row(parameter_id="НПЗ",label="kavo",min_value=0,max_value=1000,step=100,values=[400, 600]),

                    html.Hr(),

                    html.Div(
                        [
                            html.Div("Legend",style={"fontWeight": "bold","marginBottom": "10px",},),

                            html.Div("●  < 70% utilization",style={"color": "#16a34a","marginBottom": "5px",},),

                            html.Div("●  70–90% utilization",style={"color": "#f59e0b","marginBottom": "5px",},),

                            html.Div("●  > 90% utilization",style={"color": "#dc2626",},),
                        ]
                    ),

                ],
                style={
                    "width": "300px",
                    "backgroundColor": "white",
                    "padding": "25px",
                    "borderRadius": "10px",
                },
            ),

                ],
                style={
                    "display": "flex",
                    "gap": "20px",
                    "padding": "20px 30px",
                    "backgroundColor": "#f1f5f9",
                    "minHeight": "650px",
                },
            ),

        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": "#f1f5f9",
            "minHeight": "100vh",
        },
    )

    # html.Div([
    #     html.H4("НПЗ", style={"width": "30%"}),
    #     dcc.RangeSlider(
    #     id="supply-bounds",
    #     min=0,
    #     max=10000,
    #     step=100,
    #     value=[4000, 6000],
    #     marks={value: f"{value // 1000}k" for value in range(0, 10001, 1000)},
    # ), html.Div(
    #     id="supply-bounds-value",
    #     style={
    #         "textAlign": "right",
    #         "color": "#475569",
    #         "marginBottom": "25px",
    #         "width": "30%"
    #     },
    # ),], ),
    # dcc.RangeSlider(
    #     id="supply-bounds",
    #     min=0,
    #     max=10000,
    #     step=100,
    #     value=[4000, 6000],
    #     marks={value: f"{value // 1000}k" for value in range(0, 10001, 1000)},
    # ),

    # # Main Supply Cost
    # html.Label("Стоимость производства НПЗ", style={"fontWeight": "bold"}, ),
    # dcc.Slider(
    #     id="supply-npz-cost",
    #     min=0,
    #     max=10000,
    #     step=100,
    #     value=5000,
    #     marks={
    #         0: "0",
    #         5000: "5k",
    #         10000: "10k",
    #     },
    # ),
    # html.Div(
    #     id="supply-npz-cost-value",
    #     style={
    #         "textAlign": "right",
    #         "color": "#475569",
    #         "marginBottom": "25px",
    #     },
    # ),
    #
    # # Main Demand
    # html.Label(
    #     "Потребность по СП",
    #     style={"fontWeight": "bold"},
    # ),
    # dcc.RangeSlider(
    #     id="demand-sp-bounds",
    #     min=0,
    #     max=12000,
    #     step=100,
    #     value=[3000, 4000],
    #     marks={
    #         0: "0",
    #         6000: "6k",
    #         12000: "12k",
    #     },
    # ),
    # html.Div(
    #     id="demand-sp-value",
    #     style={
    #         "textAlign": "right",
    #         "color": "#475569",
    #         "marginBottom": "25px",
    #     },
    # ),
    #
    # # Main Demand Price
    # html.Label(
    #     "Стоимость потребности по СП",
    #     style={"fontWeight": "bold"},
    # ),
    # dcc.Slider(
    #     id="demand-sp-price",
    #     min=0,
    #     max=12000,
    #     step=100,
    #     value=7000,
    #     marks={
    #         0: "0",
    #         6000: "6k",
    #         12000: "12k",
    #     },
    # ),
    # html.Div(
    #     id="demand-sp-price-value",
    #     style={
    #         "textAlign": "right",
    #         "color": "#475569",
    #         "marginBottom": "30px",
    #     },
    # ),
    #
    # # Demand Spbe
    # html.Label(
    #     "Потребность на Бирже",
    #     style={"fontWeight": "bold"},
    # ),
    # dcc.RangeSlider(
    #     id="demand-spbe-bounds",
    #     min=0,
    #     max=12000,
    #     step=100,
    #     value=[3000, 4000],
    #     marks={
    #         0: "0",
    #         6000: "6k",
    #         12000: "12k",
    #     },
    # ),
    # html.Div(
    #     id="demand-spbe-value",
    #     style={
    #         "textAlign": "right",
    #         "color": "#475569",
    #         "marginBottom": "25px",
    #     },
    # ),
    #
    # # Spbe Demand Price
    # html.Label(
    #     "Стоимость потребности на Бирже",
    #     style={"fontWeight": "bold"},
    # ),
    # dcc.Slider(
    #     id="demand-spbe-price",
    #     min=0,
    #     max=12000,
    #     step=100,
    #     value=7000,
    #     marks={
    #         0: "0",
    #         6000: "6k",
    #         12000: "12k",
    #     },
    # ),
    # html.Div(
    #     id="demand-spbe-price-value",
    #     style={
    #         "textAlign": "right",
    #         "color": "#475569",
    #         "marginBottom": "30px",
    #     },
    # ),

def build_header():
    return html.Div(
        [
            html.H1("Logistics Network Optimizer", style={"margin": "0", "fontSize": "28px", }, ),html.Div("Интерактивный симулятор биржевых обязательств",style={"color": "#64748b", "marginTop": "5px", }, ),
        ],
        style={"padding": "20px 30px", "borderBottom": "1px solid #e2e8f0", "backgroundColor": "white", }, )

def build_kpi_bar():
    return html.Div(
        id="kpi-bar",
        style={"display": "flex", "gap": "20px", "padding": "15px 30px", "backgroundColor": "#f8fafc", },
    )

def build_main_content(data: Dict[str, Any]):
    return html.Div(
        [
            build_network(),
            build_parameters(data=data),
        ],
        style={
            "display": "flex",
            "gap": "20px",
            "padding": "20px 30px",
            "backgroundColor": "#f1f5f9",
            "minHeight": "650px",
        }
    )

def build_network():
    return html.Div([
        html.Div([
            html.H3("Network", style={"margin": "0"}, ),
            dcc.RadioItems(id="view-mode", options=[
                {"label": " Network", "value": "network", },
                {"label": " Sankey", "value": "sankey", }, ],
                           value="network", inline=True,
                           style={"marginTop": "10px"}, ), ],
            style={"display": "flex",
                   "justifyContent": "space-between",
                   "alignItems": "flex-start",
                   "marginBottom": "10px", }, ),
        html.Div(id="network-container", ),
        html.Div(
            id="node-info",
            style={
                "padding": "10px",
                "border": "1px solid #ccc",
                "marginTop": "10px"
            }
        )],
        style={"flex": "1", "backgroundColor": "white", "padding": "20px",
               "borderRadius": "10px", })

def build_parameters(data: Dict[str, Any]):
    return html.Div(
        [
            build_supply_section(data=data, entity="supply"),
            build_demand_section(data=data, entity="demand"),
            html.Hr(),
            build_legend(),
        ],
        style={
            "width": "300px",
            "backgroundColor": "white",
            "padding": "25px",
            "borderRadius": "10px",
        }
    )

def build_supply_section(data: Dict[str, Any], entity: str):
    rows = []
    for item in data[entity]:
        rows.append(
            html.Div([
                html.Div(f"{item['material_id']} | {item['node_id']}", style={
                                "textAlign": "left",
                                "color": "#475569",
                                "marginBottom": "15px",
                            }),
                dcc.RangeSlider(
                    id={
                        "type": "supply-range-slider",
                        "s": item['material_id'],
                        "n": item['node_id'],
                    },
                    min=item["min"],
                    max=item["max"],
                    value=[item["min"], item["max"]],
                    step=100,
                    tooltip={
                        'placement': 'top',
                        'always_visible': False,
                        'template': '{value}'
                    },
                ),
                dcc.Input(
                    id={
                        "type": "supply-number-input",
                        "s": item['material_id'],
                        "n": item['node_id'],
                    },
                    type="number",
                    min=0,
                    max=1e4,
                    value=item["cost"],
                    placeholder="Cost"
                )
            ]),
        )

    return html.Div(
        [
            html.H2(entity.capitalize()),
            *rows,
        ]
    )

def build_demand_section(data: Dict[str, Any], entity: str):
    rows = []
    for item in data[entity]:
        rows.append(
            html.Div([
                html.Div(f"{item['material_id']} | {item['node_id']}",
                         style={
                                "textAlign": "left",
                                "color": "#475569",
                                "marginBottom": "15px",
                            }),
                dcc.RangeSlider(
                    id={
                        "type": "demand-range-slider",
                        "s": item["material_id"],
                        "n": item["node_id"],
                    },
                    min=item["min"],
                    max=item["max"],
                    value=[item["min"], item["max"]],
                    step=100,
                    tooltip={
                        'placement': 'top',
                        'always_visible': False,
                        'template': '{value}'
                    },
                ),
                dcc.Input(
                    id={
                        "type": "demand-number-input",
                        "s": item["material_id"],
                        "n": item["node_id"],
                    },
                    type="number",
                    min=0,
                    max=1e4,
                    value=item["price"],
                    placeholder="Price",
                    style={"marginBottom": "15px"}
                ),
            ]),
        )

    return html.Div(
        [
            html.H2(entity.capitalize()),
            *rows,
        ]
    )

def build_legend():
    return html.Div(
        [
            html.Div("Legend",
                     style={"fontWeight": "bold", "marginBottom": "10px", }, ),

            html.Div("●  < 70% utilization",
                     style={"color": "#16a34a", "marginBottom": "5px", }, ),

            html.Div("●  70–90% utilization",
                     style={"color": "#f59e0b", "marginBottom": "5px", }, ),

            html.Div("●  > 90% utilization", style={"color": "#dc2626", }, ),
        ]
    )
