import builtins
import sys
import types

import pjenergy.utils.colab as colab


def test_is_in_colab_false(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("google.colab"):
            raise ImportError
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert colab.is_in_colab() is False


def test_is_in_colab_true(monkeypatch):
    google_mod = types.ModuleType("google")
    colab_mod = types.ModuleType("google.colab")
    monkeypatch.setitem(sys.modules, "google", google_mod)
    monkeypatch.setitem(sys.modules, "google.colab", colab_mod)
    assert colab.is_in_colab() is True


def test_execute_curl_download_command(monkeypatch, tmp_path):
    called = {}

    def fake_run(args, check):
        called["args"] = args
        called["check"] = check

    monkeypatch.setattr(colab.subprocess, "run", fake_run)
    colab.execute_curl_donwload_command("http://example", tmp_path / "f.txt")
    assert called["args"][:3] == ["curl", "-sSL", "-o"]
    assert called["check"] is True


def test_download_template_from_github(monkeypatch, capsys, tmp_path):
    called = {"args": None}

    def fake_exec(url, path):
        called["args"] = (url, path)

    monkeypatch.setattr(colab, "execute_curl_donwload_command", fake_exec)
    colab.download_template_from_github("http://example", tmp_path / "x.yaml")
    out = capsys.readouterr().out
    assert "Downloading template from github" in out
    assert called["args"] == ("http://example", tmp_path / "x.yaml")


def test_download_template_calls_when_missing(monkeypatch, tmp_path):
    called = {"hit": 0}

    def fake_download(_url, _path):
        called["hit"] += 1

    monkeypatch.setattr(colab, "download_template_from_github", fake_download)
    colab.download_template("http://example", tmp_path / "missing.yaml", force=False)
    assert called["hit"] == 1


def test_download_template_calls_when_force(monkeypatch, tmp_path):
    path = tmp_path / "exists.yaml"
    path.write_text("x")

    called = {"hit": 0}

    def fake_download(_url, _path):
        called["hit"] += 1

    monkeypatch.setattr(colab, "download_template_from_github", fake_download)
    colab.download_template("http://example", path, force=True)
    assert called["hit"] == 1
