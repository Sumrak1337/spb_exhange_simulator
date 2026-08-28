import datetime
from typing import Any, Dict

from dash import dcc, html

from ui.utils.config_data import NODE_COLORS, WEEKDAY_NAMES_RU, YEAR


def build_layout(data: Dict[str, Any]):
    return html.Div(
        [
            build_header(),
            # *build_kpi_bar(),
            build_main_content(data=data),
            *build_storage(),
        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": "#f1f5f9",
            "minHeight": "100vh",
        },
    )


def build_header():
    return html.Div(
        [
            html.H1(
                "Logistics Network Optimizer",
                style={
                    "margin": "0",
                    "fontSize": "28px",
                },
            ),
            html.Div(
                "Интерактивный симулятор биржевых обязательств",
                style={
                    "color": "#64748b",
                    "marginTop": "5px",
                },
            ),
        ],
        style={
            "padding": "20px 30px",
            "borderBottom": "1px solid #e2e8f0",
            "backgroundColor": "#f2f2f2",
        },
    )


def build_kpi_bar():
    return html.Div(
        id="kpi-bar",
        style={
            "display": "flex",
            "gap": "20px",
            "padding": "15px 30px",
            "backgroundColor": "#f8fafc",
        },
    )


def build_main_content(data: Dict[str, Any]):
    return html.Div(
        [
            build_parameters(data=data),
            build_network(),
        ],
        style={
            "display": "flex",
            "gap": "20px",
            "padding": "20px 30px",
            "backgroundColor": "#f1f5f9",
            "minHeight": "650px",
        },
    )


def build_network():
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "Network",
                        style={"margin": "0"},
                    ),
                    dcc.RadioItems(
                        id="view-mode",
                        options=[
                            {
                                "label": " Network",
                                "value": "network",
                            },
                            {
                                "label": " Sankey",
                                "value": "sankey",
                            },
                        ],
                        value="network",
                        inline=True,
                        style={"marginTop": "10px"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "flex-start",
                    "marginBottom": "10px",
                },
            ),
            html.Div(
                id="network-container",
            ),
            html.Div(
                id="node-info",
                style={
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "marginTop": "10px",
                    "backgroundColor": "white",
                },
            ),
        ],
        style={
            "flex": "1",
            "backgroundColor": "#f2f2f2",
            "padding": "20px",
            "borderRadius": "10px",
        },
    )


def build_parameters(data: Dict[str, Any]):
    return dcc.Tabs(
        id="parameters-tabs",
        children=[
            dcc.Tab(
                label="Параметры",
                children=html.Div(
                    [
                        build_supply_section(data=data, entity="supply"),
                        build_demand_section(data=data, entity="demand"),
                        html.Hr(),
                        build_legend(),
                    ],
                ),
            ),
            dcc.Tab(label="Биржа", children=build_spbe_layout(data=data)),
            dcc.Tab(
                label="Календарь", children=build_calendar_layout(year=YEAR)
            ),
        ],
        style={
            "width": "700px",
            "backgroundColor": "white",
            "padding": "25px",
            "borderRadius": "10px",
        },
    )


def build_supply_section(data: Dict[str, Any], entity: str):
    rows = []
    for item in data[entity]:
        rows.append(
            html.Div(
                [
                    html.Div(
                        f"{item['material_id']} | {item['node_id']}",
                        style={
                            "textAlign": "left",
                            # "color": "#f2f2f2",
                            "marginBottom": "15px",
                        },
                    ),
                    dcc.RangeSlider(
                        id={
                            "type": "supply-range-slider",
                            "s": item["material_id"],
                            "n": item["node_id"],
                        },
                        min=item["min"],
                        max=item["max"],
                        value=[item["min"], item["max"]],
                        # marks={
                        #     i: {"label": str(i), "style": {"color": "#f2f2f2"}}
                        #     for i in range(item["min"], item["max"] + 1, 1000)
                        # },
                        step=100,
                        tooltip={
                            "placement": "top",
                            "always_visible": False,
                            "template": "{value}",
                        },
                    ),
                    dcc.Input(
                        id={
                            "type": "supply-number-input",
                            "s": item["material_id"],
                            "n": item["node_id"],
                        },
                        type="number",
                        min=0,
                        max=1e4,
                        value=item["cost"],
                        placeholder="Cost",
                    ),
                ]
            ),
        )

    return html.Div(
        [
            html.H2(entity.capitalize()),#, style={"color": "#f2f2f2"}),
            *rows,
        ],
        # style={"backgroundColor": NODE_COLORS["supply"]},
    )


def build_demand_section(data: Dict[str, Any], entity: str):
    rows = []
    for item in data[entity]:
        rows.append(
            html.Div(
                [
                    html.Div(
                        f"{item['material_id']} | {item['node_id']}",
                        style={
                            "textAlign": "left",
                            "color": "#0c2a45",
                            "marginBottom": "15px",
                        },
                    ),
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
                            "placement": "top",
                            "always_visible": False,
                            "template": "{value}",
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
                        style={"marginBottom": "15px"},
                    ),
                ]
            ),
        )

    return html.Div(
        [
            html.H2(entity.capitalize(), style={"color": "#0c2a45"}),
            *rows,
        ],
        style={"backgroundColor": NODE_COLORS["demand"]},
    )


def build_legend():
    return html.Div(
        [
            html.Div(
                "Legend",
                style={
                    "fontWeight": "bold",
                    "marginBottom": "10px",
                },
            ),
            html.Div(
                "●  < 70% utilization",
                style={
                    "color": "#16a34a",
                    "marginBottom": "5px",
                },
            ),
            html.Div(
                "●  70–90% utilization",
                style={
                    "color": "#f59e0b",
                    "marginBottom": "5px",
                },
            ),
            html.Div(
                "●  > 90% utilization",
                style={
                    "color": "#dc2626",
                },
            ),
        ]
    )


def build_storage():
    return [
        dcc.Store(id="model-results-storage", storage_type="memory"),
        dcc.Store(id="colors", storage_type="memory"),
    ]


def build_calendar_layout(year: int = None, month: int = None) -> html.Div:
    today = datetime.date.today()
    year = year or today.year
    month = month or today.month

    return html.Div(
        [
            dcc.Store(id="calendar-state", storage_type="session"),
            dcc.Store(id="current-month", data={"year": year, "month": month}),
            html.Div(
                [
                    html.Button(
                        "◀", id="prev-month-btn", className="cal-nav-btn"
                    ),
                    html.H3(id="month-title", className="cal-month-title"),
                    html.Button(
                        "▶", id="next-month-btn", className="cal-nav-btn"
                    ),
                ],
                className="cal-nav",
            ),
            html.Div(
                [
                    html.Div(wd, className="cal-weekday-header")
                    for wd in WEEKDAY_NAMES_RU
                ],
                className="cal-weekdays-row",
            ),
            html.Div(id="calendar-grid", className="cal-grid"),
            dcc.Store(id="calendar-output", storage_type="session"),
        ],
        className="calendar-wrapper",
    )

def build_spbe_layout(data: Dict[str, Any]):
    return html.Div(
        [
            build_spbe_base(data=data),
            html.Hr(),
            build_spbe_sales(data=data),
        ],
    )


def build_spbe_base(data):
    # TODO: add selector
    rows = []
    for item in data["spbe_material_data"]:
        rows.append(html.Div(
            [
                html.Div(
                    [
                        html.Div(f"{item['spbe_material']}|{item['spbe_supplier']}"),
                        html.H4("Процент"),
                        dcc.Slider(
                            id={"type": "spbe-percent", "s": item["spbe_material"], "n": item["spbe_supplier"]},
                            min=0,
                            max=100,
                            step=0.1,
                        ),
                        html.H4("Множитель"),
                        dcc.Input(id={
                            "type": "spbe-factor",
                            "s": item["spbe_material"],
                            "n": item["spbe_supplier"],
                        },
                            type="number",
                            min=0,
                            max=10,
                            step=0.01,
                            value=1,
                        ),
                        html.H4("Размер лота"),
                        dcc.Input(id={
                            "type": "spbe-lot-size",
                            "s": item["spbe_material"],
                            "n": item["spbe_supplier"],
                        },
                            type="number",
                            min=0,
                            max=100,
                            value=60,
                        ),
                        html.H4("Статнагрузка"),

                    ]
                ),
            ],
            style={
                "display": "center",
                "gap": "100px",
                # "padding": "20px 30px",
                "minHeight": "1000px",
            }
        )
        )
    return html.Div([html.H3("База"), *rows])


def build_spbe_sales(data):
    rows = []
    return html.Div([html.H3("Продажи")])
