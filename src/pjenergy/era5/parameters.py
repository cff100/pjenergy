from dataclasses import dataclass, asdict
from typing import Sequence
from math import prod

from pjenergy.era5.loaders import ask_alternative_combination_limit




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
        """        
        :return: Number of possible parameters combinations. 
        :rtype: int
        """
        data = asdict(self)
        data.pop("area") # The area is not relevant to the requisition load

        counts = [
            len(v) if isinstance(v, Sequence) and not isinstance(v, str) else 1
            for v in data.values()
        ]

        return prod(counts)
    
    def respects_request_limit(self, limit: int = 600, force: bool = False) -> bool:
        if limit > 5400 and not force:
            limit = ask_alternative_combination_limit(limit)
        return self.count_parameter_combinations() <= limit
    
    
    



    

