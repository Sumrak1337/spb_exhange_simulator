import json

from dash import Dash

from ui.callbacks import register_callbacks
from ui.layout import build_layout

app = Dash(__name__, suppress_callback_exceptions=True)

with open("input_data/input_data.json", "r", encoding="utf-8") as file:
    main_data = json.load(file)

app.layout = build_layout(data=main_data)
register_callbacks(app=app, main_data=main_data)

if __name__ == "__main__":
    app.run(debug=True)
