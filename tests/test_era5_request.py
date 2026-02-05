from pathlib import Path

import pjenergy.era5.request as request


class DummyParams:
    dataset = "ds"

    def to_cds_dict(self):
        return {"a": 1}


class DummyClient:
    def __init__(self, capture):
        self.capture = capture

    def retrieve(self, dataset, req, path):
        self.capture["args"] = (dataset, req, path)


def test_request_era5_calls_client(monkeypatch):
    captured = {}
    monkeypatch.setattr(request, "create_cdsapi_client", lambda: DummyClient(captured))
    monkeypatch.setattr(request, "load_parameters_from_template", lambda: DummyParams())
    monkeypatch.setattr(request.DataDirectories, "cds", lambda: Path("out.nc"))

    request.request_era5()

    assert captured["args"] == ("ds", {"a": 1}, Path("out.nc"))
