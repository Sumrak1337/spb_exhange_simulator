from typing import AnyStr, Tuple, Union

import pyomo.environ as pyo

from optimization.builder import Builder

Numeric = Union[float, int]


class MainVariables(Builder):
    def __init__(self, model: pyo.ConcreteModel):
        super().__init__(model=model)

    def build(self) -> None:
        self.model.objective_var = pyo.Var(within=self.reals)

        self.model.supply = pyo.Var(
            self.model.supply_set,
            within=self.positive_variable,
            bounds=self._supply_bounds,
        )
        self.model.demand = pyo.Var(
            self.model.demand_set,
            within=self.positive_variable,
            bounds=self._demand_bounds,
        )
        self.model.transport = pyo.Var(
            self.model.transport_set,
            within=self.positive_variable,
            bounds=self._transport_bounds,
        )
        self.model.distress_purchase = pyo.Var(
            self.model.material_balance_set, within=self.positive_variable
        )
        self.model.distress_sale = pyo.Var(
            self.model.material_balance_set, within=self.positive_variable
        )

    @staticmethod
    def _supply_bounds(
        model, *indices: Tuple[AnyStr]
    ) -> Tuple[Numeric, Numeric]:
        return model.supply_min[indices], model.supply_max[indices]

    @staticmethod
    def _demand_bounds(
        model, *indices: Tuple[AnyStr]
    ) -> Tuple[Numeric, Numeric]:
        return model.demand_min[indices], model.demand_max[indices]

    @staticmethod
    def _transport_bounds(
        model, *indices: Tuple[AnyStr]
    ) -> Tuple[Numeric, Numeric]:
        return model.transport_min[indices], model.transport_max[indices]
