from optimization.builder import Builder
import pyomo.environ as pyo


class MainVariables(Builder):
    def __init__(self, model: pyo.ConcreteModel):
        super().__init__(model=model)

    def build(self) -> None:
        self.model.supply = pyo.Var(self.model.supply_set, within=self.positive_variable)
        self.model.demand = pyo.Var(self.model.supply_set, within=self.positive_variable)
        self.model.transport = pyo.Var(self.model.supply_set, within=self.positive_variable)
        self.model.distress_purchase = pyo.Var(self.model.material_balance_set, within=self.positive_variable)
        self.model.distress_sale = pyo.Var(self.model.material_balance_set, within=self.positive_variable)
