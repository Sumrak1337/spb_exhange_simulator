from optimization.builder import Builder
import pyomo.environ as pyo

class MainSets(Builder):
    def __init__(self, model: pyo.ConcreteModel):
        super().__init__(model=model)

    def build(self) -> None:
        self.model.supply_set = pyo.Set(initialize=self.model.data.supply_min.set_index(["s", "n"]).index)
        self.model.demand_set = pyo.Set(initialize=self.model.data.demand_min.set_index(["s", "n"]).index)
        self.model.transport_set = pyo.Set(initialize=self.model.data.transport_min.set_index(["s", "n1", "n2"]).index)
        self.model.transport_to_set = pyo.Set(initialize=self.model.data.transport_min.set_index(["s", "n2"]).index)
        self.model.transport_from_set = pyo.Set(initialize=self.model.data.transport_min.set_index(["s", "n1"]).index)

        self.model.material_balance_set = pyo.Set(initialize=self.model.supply_set | self.model.demand_set | self.model.transport_to_set | self.model.transport_from_set)
