from dash import Dash
from typing import Dict, Any

from ui.callbacks.optimization import optimization_callback
from ui.callbacks.visualization import visualization_callbacks

def register_callbacks(app: Dash, main_data: Dict[str, Any]):
    optimization_callback(app=app, main_data=main_data)
    visualization_callbacks(app=app)
