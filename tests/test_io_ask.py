import builtins

import pjenergy.io.ask as ask


def test_is_answer_yes_or_no():
    assert ask.is_answer_yes_or_no("y") is True
    assert ask.is_answer_yes_or_no("N") is True
    assert ask.is_answer_yes_or_no("maybe") is False


def test_is_answer_yes(monkeypatch):
    inputs = iter(["maybe", "n"])
    monkeypatch.setattr(builtins, "input", lambda _q: next(inputs))
    assert ask.is_answer_yes("? ") is False


def test_ask_value(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _q: "123")
    assert ask.ask_value("? ") == 123


def test_ask_alternative_combination_limit(monkeypatch):
    calls = {"warnings": 0}

    def fake_warning(_limit):
        calls["warnings"] += 1

    inputs = iter(["N", "500", "Y"])
    monkeypatch.setattr(builtins, "input", lambda _q: next(inputs))
    monkeypatch.setattr(ask, "print_combination_limit_warning", fake_warning)

    assert ask.ask_alternative_combination_limit(600) == 500
    assert calls["warnings"] == 2
