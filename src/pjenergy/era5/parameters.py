"""ERA5 parameter models and request-splitting helpers."""

from dataclasses import dataclass, asdict
from typing import Sequence
from math import prod


from pjenergy.config.constants import RequestFlowConstants



@dataclass
class ERA5Parameters:
    """Container for ERA5 request parameters and helper utilities."""
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
        Build the payload dictionary required by the CDS API request.
        
        :return: Dictionary required for the CDS API request (without ``dataset``).
        :rtype: dict
        """
        data = asdict(self)
        data.pop("dataset")

        return data
    
    @staticmethod
    def count_parameter_combinations(data: dict) -> int:
        """        
        Count the number of parameter combinations represented by a mapping.

        The ``area`` entry does not affect the request load and is ignored.

        :param data: Parameters dictionary.
        :type data: dict
        :return: Number of parameter combinations.
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
        Check whether the number of parameter combinations is within a limit.
        
        :param data: Parameters dictionary.
        :type data: dict
        :param limit: Maximum number of parameters combinations allowed.
        :type limit: int
        :return: `True` if the number of parameters combinations is below the limit, `False` otherwise.
        :rtype: bool
        """
        return ERA5Parameters.count_parameter_combinations(data) <= limit
    

    @staticmethod
    def _is_splitting_invalid(data: dict, param: str) -> bool:
        """
        Determine whether splitting parameter values would be invalid.

        Splitting is considered invalid if ``data[param]`` is a string or a
        sequence with a single value.
        
        :param data: Dictionary of parameters
        :type data: dict
        :param param: Parameter whose values will be divided among the dictionaries.
        :type param: str
        :return: `True` if in the dictionary the parameter value is a string, or a list or tuple with a single value.
        :rtype: bool
        """
        return len(data[param]) <= 1 or isinstance(data[param], str)

    @staticmethod
    def _fix_parameter(data: dict, param: str, i: int) -> dict:
        """
        Return a shallow copy of ``data`` with ``param`` replaced by its i-th element.

        This method is typically used when expanding or iterating over parameters
        that are sequences. If splitting ``param`` is deemed invalid by
        ``_is_splitting_invalid``, the original dictionary is returned unchanged.

        :param data: Input mapping of parameters to values or sequences of values.
        :type data: dict
        :param param: Key whose value should be indexed and replaced.
        :type param: str
        :param i: Index of the element to extract from ``data[param]``.
        :type i: int
        :return: A new dictionary with ``param`` fixed to a single value, or the
                original dictionary if splitting is invalid.
        :rtype: dict
        """

        if ERA5Parameters._is_splitting_invalid(data, param):
            return data
        return {**data, param: data[param][i]}  # {**d, k: v} = clone d and replace k with v.

    @staticmethod
    def brake_depth(data: dict, limit: int):
        """
        Determine the split depth needed to respect a request size limit.

        The depth is calculated by progressively fixing parameters (following
        ``RequestFlowConstants.PARAMETERS_PRIORITY_ORDER``) until the number of
        parameter combinations is within ``limit``.

        :param data: Parameters dictionary.
        :type data: dict
        :param limit: Maximum number of parameter combinations allowed.
        :type limit: int
        :return: The depth at which the request is within the limit.
        :rtype: int
        """

        for depth, param in enumerate(RequestFlowConstants.PARAMETERS_PRIORITY_ORDER):

            if ERA5Parameters.respects_request_limit(data, limit):
                return depth

            data = ERA5Parameters._fix_parameter(data, param, 0)

        return len(RequestFlowConstants.PARAMETERS_PRIORITY_ORDER)
            
    @staticmethod
    def separates_one_parameter_values(data: dict, param: str) -> list[dict[str, Sequence]]:
        """
        Split a parameter's values into multiple dictionaries.
        
        :param data: Initial dictionary of parameters.
        :type data: dict
        :param param: Parameter whose values will be divided among the dictionaries.
        :type param: str
        :return: List of dictionaries with ``param`` fixed to each of its values.
        :rtype: list[dict[str, Sequence]]
        """
        
        new_data_list = []
        for i in range(len(data[param])):
            new_data = ERA5Parameters._fix_parameter(data, param, i)
            new_data_list.append(new_data)

        return new_data_list
    
    @staticmethod
    def separates_parameters_values(initial_data: dict, depth: int) -> list[dict[str, Sequence]]:
        """
        Split values for the first ``depth`` parameters in the priority list.
        
        :param initial_data: Master parameter dictionary containing all parameters.
        :type initial_data: dict
        :param depth: Depth of the priority list that determines which parameters
            will have their values split into separate dictionaries.
        :type depth: int
        :return: List of dictionaries with values split for the selected parameters.
        :rtype: list[dict[str, Sequence]]
        """

        data_list = [initial_data]

        for param in RequestFlowConstants.PARAMETERS_PRIORITY_ORDER[:depth]:
            new_data_list = []
            for data in data_list:
                list = ERA5Parameters.separates_one_parameter_values(data, param)
                new_data_list.extend(list)
            data_list = new_data_list
        return data_list


   
