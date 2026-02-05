import pjenergy.io.console as console
from pjenergy.config.constants import RequestFlowConstants


def test_print_combination_limit_warning_large(capsys):
    console.print_combination_limit_warning(RequestFlowConstants.LARGE_REQUEST_LIMIT)
    out = capsys.readouterr().out
    assert "very costly" in out


def test_print_combination_limit_warning_medium(capsys):
    console.print_combination_limit_warning(RequestFlowConstants.DEFAULT_REQUEST_LIMIT)
    out = capsys.readouterr().out
    assert "considerable size" in out
