from abc import ABC, abstractmethod
from typing import List

import pyomo.environ as pyo


class Builder(ABC):
    indices: List[str] = []

    def __init__(self, model: pyo.ConcreteModel):
        self.model = model

        self.positive_variable = pyo.NonNegativeReals
        self.binary = pyo.Binary
        self.reals = pyo.Reals
        self.integers = pyo.Integers
        self.any = pyo.Any

    @abstractmethod
    def build(self) -> None:
        raise NotImplementedError
