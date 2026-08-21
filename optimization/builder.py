from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Any, Dict, List, Tuple

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

    # def _get_dict(self, parameter_name: str) -> Dict[Tuple[str], Union[float, int]]:
    #     return (
    #         self.model.data.parameters[parameter_name]
    #         .set_index(self.indices)
    #         .value.to_dict()
    #     )

    # def _get_mapping(
    #     self, dataframe: DataFrame, indices: List[str]
    # ) -> Dict[Hashable, Any]:
    #     if dataframe.empty:
    #         return {idx: [] for idx in self.model.periods}
    #
    #     grouped = (
    #         dataframe.rename(columns={"tgt": "t"})
    #         .drop_duplicates()
    #         .groupby("t")[indices]
    #     )
    #     return {idx: group[indices].values.tolist() for idx, group in grouped}
