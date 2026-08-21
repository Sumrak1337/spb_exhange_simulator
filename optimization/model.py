import pyomo.environ as pyo
import inspect

from domain.data import OptimizationInput
from typing import List
from optimization.builder import Builder

import optimization.sets as sets
import optimization.parameters as parameters
import optimization.constraints as constraints
import optimization.variables as variables
import optimization.objective as objectives


class LogisticsModel(pyo.ConcreteModel):
    def __init__(self, data: OptimizationInput):
        super().__init__()
        self.data = data

        self.sets_builders: List[Builder] = self._add_set_builders()
        self.parameters_builders: List[Builder] = (
            self._add_parameter_builders()
        )
        self.variable_builders: List[Builder] = self._add_variable_builders()
        self.constraint_builders: List[Builder] = (
            self._add_constraint_builders()
        )
        self.objective_builders: List[Builder] = self._add_objective_builders()

    def build(self):
        for builder in self.sets_builders:
            builder.build()

        for builder in self.parameters_builders:
            builder.build()

        for builder in self.variable_builders:
            builder.build()

        for builder in self.constraint_builders:
            builder.build()

        for builder in self.objective_builders:
            builder.build()

    def _add_set_builders(self) -> List[Builder]:
        return [data_set(model=self) for _, data_set in inspect.getmembers(sets) if inspect.isclass(data_set)]

    def _add_parameter_builders(self) -> List[Builder]:
        return [parameter(model=self) for _, parameter in inspect.getmembers(parameters) if inspect.isclass(parameter)]

    def _add_variable_builders(self) -> List[Builder]:
        return [variable(model=self) for _, variable in inspect.getmembers(variables) if inspect.isclass(variable)]

    def _add_constraint_builders(self) -> List[Builder]:
        return [constraint(model=self) for _, constraint in inspect.getmembers(constraints) if inspect.isclass(constraint)]

    def _add_objective_builders(self) -> List[Builder]:
        return [objective(model=self) for _, objective in inspect.getmembers(objectives) if inspect.isclass(objective)]
