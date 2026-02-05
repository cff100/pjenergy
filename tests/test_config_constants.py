from pjenergy.config.constants import RequestFlowConstants


def test_request_flow_constants_exist():
    assert RequestFlowConstants.DEFAULT_REQUEST_LIMIT > 0
    assert RequestFlowConstants.MEDIUM_REQUET_LIMIT > 0
    assert RequestFlowConstants.LARGE_REQUEST_LIMIT > 0
    assert isinstance(RequestFlowConstants.PARAMETERS_PRIORITY_ORDER, list)
    assert RequestFlowConstants.PARAMETERS_PRIORITY_ORDER
