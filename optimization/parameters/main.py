import pyomo.environ as pyo

from optimization.builder import Builder


class MainParameters(Builder):
    def __init__(self, model: pyo.ConcreteModel):
        super().__init__(model=model)

    def build(self) -> None:
        self.model.supply_min = pyo.Param(self.model.supply_set, initialize=self.model.data.supply_min.set_index(["s", "n"]).value.to_dict())
        self.model.supply_max = pyo.Param(self.model.supply_set, initialize=self.model.data.supply_max.set_index(["s", "n"]).value.to_dict())
        self.model.supply_cost = pyo.Param(self.model.supply_set, initialize=self.model.data.supply_cost.set_index(["s", "n"]).value.to_dict())

        self.model.demand_min = pyo.Param(self.model.demand_set, initialize=self.model.data.demand_min.set_index(["s", "n"]).value.to_dict())
        self.model.demand_max = pyo.Param(self.model.demand_set, initialize=self.model.data.demand_max.set_index(["s", "n"]).value.to_dict())
        self.model.demand_price = pyo.Param(self.model.demand_set, initialize=self.model.data.demand_price.set_index(["s", "n"]).value.to_dict())

        self.model.transport_min = pyo.Param(self.model.transport_set, initialize=self.model.data.transport_min.set_index(["s", "n1", "n2"]).value.to_dict())
        self.model.transport_max = pyo.Param(self.model.transport_set, initialize=self.model.data.transport_max.set_index(["s", "n1", "n2"]).value.to_dict())
        self.model.transport_cost = pyo.Param(self.model.transport_set, initialize=self.model.data.transport_cost.set_index(["s", "n1", "n2"]).value.to_dict())

        self.model.transport_to = pyo.Param(self.model.transport_to_set, initialize=self.model.data.transport_min.groupby(["s", "n2"]).n1.apply(lambda x: x.values.tolist()).to_dict(), within=self.any)
        self.model.transport_from = pyo.Param(self.model.transport_from_set, initialize=self.model.data.transport_min.groupby(["s", "n1"]).n2.apply(lambda x: x.values.tolist()).to_dict(), within=self.any)

        self.model.distress_cost = pyo.Param(initialize=1e6)
