from dataclasses import dataclass, asdict
from typing import Sequence
from math import prod

from pjenergy.io.ask import is_answer_yes, ask_value


@dataclass
class ERA5Parameters:
    dataset: str
    product_type: Sequence[str]
    variable: Sequence[str]
    year: Sequence[str]
    month: Sequence[str]
    day: Sequence[str]
    time: Sequence[str]
    area: Sequence[float]
    pressure_level: Sequence[str]
    data_format: Sequence[str]
    download_format: Sequence[str]

    def to_cds_dict(self) -> dict:
        data = asdict(self)
        data.pop("dataset")

        return data
    
    def count_parameter_combinations(self) -> int:
        data = asdict(self)
        data.pop("area") # The area is not relevant to the requisition load

        counts = [
            len(v) if isinstance(v, Sequence) and not isinstance(v, str) else 1
            for v in data.values()
        ]

        return prod(counts)
    
    def is_within_combinations_limit(self, limit: int) -> bool:
        return self.count_parameter_combinations() <= limit
    
    
    



    

