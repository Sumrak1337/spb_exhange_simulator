from dash import html, dcc
from typing import List

def main_parameter_row(
    parameter_id: str,
    label: str,
    min_value: float,
    max_value: float,
    step: float,
    values: List[float],
    min_value_cost: float
):
    return html.Div(
        [
            html.Label(
                label,
                className="parameter-row__label",
            ),

            dcc.RangeSlider(
                id={"type": "parameter-slider", "name": parameter_id},
                min=min_value,
                max=max_value,
                step=step,
                value=values,
            ),

            dcc.Input(
                id={"type": "parameter-input", "name": parameter_id},
                type="number",
                min=min_value_cost,
                max=max_value_cost,
                step=step_cost,
                value=value_cost,
                className="parameter-row__input",
            ),
        ],
        className="parameter-row",
    )
