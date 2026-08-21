from optimization.builder import Builder
import pyomo.environ as pyo


class MainConstraints(Builder):
    def __init__(self, model: pyo.ConcreteModel):
        super().__init__(model=model)

    def build(self) -> None:
        @self.model.Constraint(self.model.material_balance_set)
        def material_balance_constraint(model, s, n):
            supply = model.supply if (s, n) in model.supply else pyo.ZeroConstant
            demand = model.demand if (s, n) in model.demand else pyo.ZeroConstant



            return pyo.Constraint.Skip