from pjenergy.io.ask import ask_request_limit, ask_alternative_combination_limit
from pjenergy.config.constants import RequestFlowConstants


def limit_selection_flow(limit: int = RequestFlowConstants.DEFAULT_REQUEST_LIMIT, 
                         force: bool = False):
    
    #limit = ask_request_limit(limit)

    if limit >= RequestFlowConstants.MEDIUM_REQUET_LIMIT and not force:
        limit = ask_alternative_combination_limit(limit)

    return limit



    