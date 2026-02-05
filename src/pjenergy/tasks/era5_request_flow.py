"""High-level request flow helpers for ERA5 downloads."""

from pjenergy.io.ask import ask_alternative_combination_limit
from pjenergy.config.constants import RequestFlowConstants


def limit_selection_flow(limit: int = RequestFlowConstants.DEFAULT_REQUEST_LIMIT, 
                         force: bool = False):
    """
    Apply the limit selection flow for request size constraints.

    :param limit: Initial combination limit.
    :type limit: int
    :param force: If True, skip prompting and use the provided limit.
    :type force: bool
    :return: Final limit to use.
    :rtype: int
    """
    
    if limit >= RequestFlowConstants.MEDIUM_REQUET_LIMIT and not force:
        limit = ask_alternative_combination_limit(limit)

    return limit



if __name__ == "__main__":
    print(limit_selection_flow(5400))
