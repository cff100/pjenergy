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
        """
        Assembles the dictionary required for the CDS API request.
        
        :return: Dictionary required for the CDS API request.
        :rtype: dict[Any, Any]
        """
        data = asdict(self)
        data.pop("dataset")

        return data
    
    @staticmethod
    def count_parameter_combinations(data: dict) -> int:
        """        
        Counts the numbers of parameters combinations from a parameters 
        dictionary.

        :param data: Parameters dictionary.
        :type data: dict
        :return: Number of parameters combinations. 
        :rtype: int
        """
        data = data.copy()
        data.pop("area") # The area is not relevant to the requisition load

        counts = [
            len(v) if isinstance(v, Sequence) and not isinstance(v, str) else 1
            for v in data.values()
        ]

        return prod(counts)
    
    @staticmethod
    def respects_request_limit(data: dict, limit: int) -> bool:
        """
        Checks if the number of parameters combinations in the request is below the limit.
        
        :param data: Parameters dictionary.
        :type data: dict
        :param limit: Maximum number of parameters combinations allowed.
        :type limit: int
        :return: `True` if the number of parameters combinations is below the limit, `False` otherwise.
        :rtype: bool
        """
        return ERA5Parameters.count_parameter_combinations(data) <= limit
    

    @staticmethod
    def _is_splitting_valid(data: dict, param: str) -> bool:
        return len(data[param]) <= 1 or isinstance(data[param], str)

    @staticmethod
    def _fix_parameter(data: dict, param: str, i: int) -> dict:
        if ERA5Parameters._is_splitting_valid(data, param):
            #print("!!")
            return data
        return {**data, param: data[param][i]}  # {**d, k: v} = clone d and replace k with v.

    @staticmethod
    def brake_depth(data: dict, limit: int):
 
        for depth, param in enumerate(RequestFlowConstants.PARAMETERS_PRIORITY_ORDER):

            if ERA5Parameters.respects_request_limit(data, limit):
                return depth

            data = ERA5Parameters._fix_parameter(data, param, 0)

        return len(RequestFlowConstants.PARAMETERS_PRIORITY_ORDER)
            
    @staticmethod
    def placeholder_01(data: dict, param: str):
        
        new_data_list = []
        for i in range(len(data[param])):
            new_data = ERA5Parameters._fix_parameter(data, param, i)
            new_data_list.append(new_data)

        return new_data_list
    
    @staticmethod
    def placeholder_02(initial_data: dict, depth: int):

        data_list = [initial_data]

        for param in RequestFlowConstants.PARAMETERS_PRIORITY_ORDER[:depth]:
            new_data_list = []
            for data in data_list:
                list = ERA5Parameters.placeholder_01(data, param)
                new_data_list.extend(list)
            data_list = new_data_list
        return data_list


    # def placeholder_1(self, limit: int):
    #     data = asdict(self)
    #     obj = self
    #     i = 0
    #     parameters_dicts_list_total = [data]
    #     first_dict = parameters_dicts_list_total[0]
    #     while not obj.respects_request_limit(limit):
    #         param = RequestFlowConstants.PARAMETERS_PRIORITY_ORDER[i]
    #         if len(first_dict[param]) == 1:
    #             pass
    #         else: 
    #             parameters_dicts_list_2 = []
    #             for d in parameters_dicts_list_total:
    #                 parameters_dicts_list = []
    #                 for elem in d[param]:
    #                     new_dict = deepcopy(d)
    #                     new_dict[param] = elem
    #                     parameters_dicts_list.append(new_dict)
    #                 parameters_dicts_list_2.extend(parameters_dicts_list) 
    #             parameters_dicts_list_total = parameters_dicts_list_2
    #             first_dict = parameters_dicts_list_total[0]
    #             obj = ERA5Parameters(**first_dict)
    #         i += 1
    #     return parameters_dicts_list_total



    