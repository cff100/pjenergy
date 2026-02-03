from pjenergy.io.ask import ask_alternative_combination_limit
from pjenergy.config.constants import RequestFlowConstants


def limit_selection_flow(limit: int = RequestFlowConstants.DEFAULT_REQUEST_LIMIT, 
                         force: bool = False):
    
    if limit >= RequestFlowConstants.MEDIUM_REQUET_LIMIT and not force:
        limit = ask_alternative_combination_limit(limit)

    return limit



if __name__ == "__main__":
    print(limit_selection_flow(5400))