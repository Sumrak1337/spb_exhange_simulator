import pyomo.environ as pyo

from optimization.builder import Builder


class MainObjective(Builder):
    def __init__(self, model):
        super().__init__(model=model)

    def build(self) -> None:
        @self.model.Constraint()
        def objective_constraint(model):
            demand = sum(
                model.demand[s, n] * model.demand_price[s, n]
                for s, n in model.demand_set
            )
            supply = sum(
                model.supply[s, n] * model.supply_cost[s, n]
                for s, n in model.supply_set
            )
            transport = sum(
                model.transport[s, n1, n2] * model.transport_cost[s, n1, n2]
                for s, n1, n2 in model.transport_set
            )
            distresses = (
                sum(
                    model.distress_purchase[s, n] + model.distress_sale[s, n]
                    for s, n in model.material_balance_set
                )
                * model.distress_cost
            )
            return (
                model.objective_var == demand - supply - transport - distresses
            )

        self.model.objective = pyo.Objective(
            expr=self.model.objective_var, sense=pyo.maximize
        )
