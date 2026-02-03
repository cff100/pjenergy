from dataclasses import dataclass, asdict
from typing import Sequence
from math import prod
from copy import deepcopy

from pjenergy.config.constants import RequestFlowConstants



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
    
    def respects_request_limit(self, limit) -> bool:
        """
        Checks if the number of parameters combinations in the request is below the limit.
        
        :param limit: 
        :type limit: int
        :return:
        :rtype: bool
        """
        return self.count_parameter_combinations() <= limit
    
    
    def placeholder_1(self, limit: int, param_dict: dict):
        obj = self
        while not obj.respects_request_limit(limit):
            obj = self.placeholder_2(param_dict)
        return parameters_dicts_list
        
                
    def placeholder_2(self, param_dict: dict):
        for param in RequestFlowConstants.PARAMETERS_PRIORITY_ORDER:
            if len(param_dict[param]) == 1:
                continue
            else: 
                parameters_dicios_list = self.placeholder_3(param_dict, param)
        return parameters_dicios_list

    def placeholder_3(self, param_dict: dict, param: str):
        parameters_dicios_list = []
        for elem in param_dict[param]:
            new_dict = deepcopy(param_dict)
            new_dict[param] = elem
            parameters_dicios_list.append(new_dict)
        return parameters_dicios_list
            
    def placeholder_4(self, parameters_dicios_list: list[dict]):
        first_dict = parameters_dicios_list[0]
        p = ERA5Parameters(**first_dict)
        return p
    
    



    

