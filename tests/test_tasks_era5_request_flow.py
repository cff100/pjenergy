import pjenergy.tasks.era5_request_flow as flow
from pjenergy.config.constants import RequestFlowConstants


def test_limit_selection_flow_prompts_when_needed(monkeypatch):
    monkeypatch.setattr(flow, "ask_alternative_combination_limit", lambda _limit: 123)
    result = flow.limit_selection_flow(RequestFlowConstants.MEDIUM_REQUET_LIMIT, force=False)
    assert result == 123


def test_limit_selection_flow_force_skips_prompt(monkeypatch):
    called = {"hit": False}

    def fake_ask(_limit):
        called["hit"] = True
        return 999

    monkeypatch.setattr(flow, "ask_alternative_combination_limit", fake_ask)
    result = flow.limit_selection_flow(RequestFlowConstants.MEDIUM_REQUET_LIMIT, force=True)
    assert result == RequestFlowConstants.MEDIUM_REQUET_LIMIT
    assert called["hit"] is False
