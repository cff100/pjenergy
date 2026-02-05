from pathlib import Path

import pjenergy.era5.client as client


def test_create_cdsapi_client_doc_writes_file(tmp_path, monkeypatch):
    target = tmp_path / ".cdsapirc"
    monkeypatch.setattr(client.BasicDirectories, "cdsapirc", lambda: target)
    client.create_cdsapi_client_doc("mykey", "http://example.test/api")
    assert target.read_text() == "url: http://example.test/api\nkey: mykey\n"


def test_create_cdsapi_client_uses_cdsapi(monkeypatch):
    called = {"hit": False}

    def fake_client():
        called["hit"] = True
        return "client"

    monkeypatch.setattr(client.cdsapi, "Client", fake_client)
    assert client.create_cdsapi_client() == "client"
    assert called["hit"] is True
