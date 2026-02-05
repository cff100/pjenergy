"""Console output helpers for the request flow."""

from pjenergy.config.constants import RequestFlowConstants

def print_combination_limit_warning(limit: int) -> None:
    """Print a warning about the size of a parameter combination request."""
    if limit >= RequestFlowConstants.LARGE_REQUEST_LIMIT:
        print(f"{limit} combinations is a very costly request. "
            "The request will not be prioritized and even risks not being accepted by the CDS. "
            "A lower value is better.")
    else:
        print(f"{limit} combinations is a request of considerable size, "
              "so it will not be prioritized by the CDS. 600 is a better value")
