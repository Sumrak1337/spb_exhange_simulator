import pyomo.environ as pyo

from domain.data import OptimizationInput

class LogisticsModel(pyo.ConcreteModel):
    def __init__(self, data: OptimizationInput):
        super().__init__()
        self.data = data