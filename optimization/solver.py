from pyomo.environ import SolverFactory, ConcreteModel


class SolverManager:
    def __init__(self):
        self.solver = self._set_solver()

    def solve(self, model: ConcreteModel):
        results = self.solver.solve(model, tee=True)
        return results

    @staticmethod
    def _set_solver():
        # TODO: fill
        solver = SolverFactory("highs")
        return solver


