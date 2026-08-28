import datetime

import dash_cytoscape as cyto
from dash import ALL, Dash, Input, Output, State, ctx, html, no_update

from ui.utils.calendar_utils import get_default_working_days, get_month_grid
from ui.utils.config_data import MONTH_NAMES_RU
from ui.utils.utils import make_stylesheet


def visualization_callbacks(app: Dash):
    # TODO: probably, need to divide into visualization and calendar sections
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

    @app.callback(
        Output("calendar-state", "data"),
        Output("calendar-output", "data"),
        Input("calendar-state", "data"),
        prevent_initial_call=False,
    )
    def init_calendar_state(current_state):
        """Первый запуск — заполняем год стандартными рабочими днями."""
        if current_state is not None:
            return current_state, current_state

        year = datetime.date.today().year
        default = get_default_working_days(year)
        return default, default

    @app.callback(
        Output("month-title", "children"),
        Input("current-month", "data"),
    )
    def update_month_title(current_month):
        year = current_month["year"]
        month = current_month["month"]
        return f"{MONTH_NAMES_RU[month - 1]} {year}"

    @app.callback(
        Output("current-month", "data"),
        Input("prev-month-btn", "n_clicks"),
        Input("next-month-btn", "n_clicks"),
        State("current-month", "data"),
        prevent_initial_call=True,
    )
    def navigate_month(_prev_clicks, _next_clicks, current):
        triggered = ctx.triggered_id
        if not triggered:
            return no_update

        year = current["year"]
        month = current["month"]

        if triggered == "prev-month-btn":
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        elif triggered == "next-month-btn":
            month += 1
            if month > 12:
                month = 1
                year += 1

        return {"year": year, "month": month}

    @app.callback(
        Output("calendar-grid", "children"),
        Input("current-month", "data"),
        Input("calendar-state", "data"),
    )
    def render_month_grid(current_month, state):
        if state is None or current_month is None:
            return []

        year = current_month["year"]
        month = current_month["month"]
        weeks = get_month_grid(year, month)
        today = datetime.date.today().isoformat()

        cells = []

        for week in weeks:
            for day in week:
                if day == 0:
                    cells.append(html.Div(className="cal-day empty"))
                    continue

                date_obj = datetime.date(year, month, day)
                date_str = date_obj.isoformat()
                is_working = state.get(date_str, True)

                classes = [
                    "cal-day",
                    "working" if is_working else "non-working",
                ]
                if date_str == today:
                    classes.append("today")

                cells.append(
                    html.Div(
                        str(day),
                        id={"type": "cal-day", "date": date_str},
                        className=" ".join(classes),
                        n_clicks=0,
                    )
                )

        return cells

    @app.callback(
        Output("calendar-state", "data", allow_duplicate=True),
        Output("calendar-output", "data", allow_duplicate=True),
        Output(
            {"type": "cal-day", "date": ALL}, "n_clicks", allow_duplicate=True
        ),
        Input({"type": "cal-day", "date": ALL}, "n_clicks"),
        State("calendar-state", "data"),
        State({"type": "cal-day", "date": ALL}, "id"),
        prevent_initial_call=True,
    )
    def toggle_day(n_clicks_list, state, day_ids):
        if state is None:
            return no_update, no_update, no_update

        clicked_indices = [
            i
            for i, clicks in enumerate(n_clicks_list)
            if clicks and clicks > 0
        ]

        if not clicked_indices:
            return no_update, no_update, [0] * len(n_clicks_list)

        clicked_idx = clicked_indices[-1]
        date_str = day_ids[clicked_idx]["date"]

        new_state = state.copy()
        new_state[date_str] = not new_state.get(date_str, True)

        new_n_clicks = [0] * len(n_clicks_list)

        return new_state, new_state, new_n_clicks
