from optimization.builder import Builder
import pyomo.environ as pyo


class MainConstraints(Builder):
    def __init__(self, model: pyo.ConcreteModel):
        super().__init__(model=model)

    def build(self) -> None:
        @self.model.Constraint(self.model.material_balance_set)
        def material_balance_constraint(model, s, n):
            supply = model.supply[s, n] if (s, n) in model.supply else pyo.ZeroConstant
            demand = model.demand[s, n] if (s, n) in model.demand else pyo.ZeroConstant

            transport_to = pyo.ZeroConstant
            if (s, n) in model.transport_to:
                transport_to += sum(model.transport[s, n1, n] for n1 in model.transport_to[s, n])

            transport_from = pyo.ZeroConstant
            if (s, n) in model.transport_from:
                transport_from += sum(model.transport[s, n, n2] for n2 in model.transport_from[s, n])

            distress_purchase = model.distress_purchase[s, n]
            distress_sale = model.distress_sale[s, n]

            return supply + transport_to + distress_purchase == demand + transport_from + distress_sale
