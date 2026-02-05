from pathlib import Path

import pjenergy.era5.loaders as loaders


def test_download_parameters_from_github_colab(monkeypatch):
    called = {}

    def fake_download(url, path, force):
        called["args"] = (url, path, force)

    monkeypatch.setattr(loaders, "is_in_colab", lambda: True)
    monkeypatch.setattr(loaders, "download_template", fake_download)

    loaders.download_parameters_from_github(force=True)
    assert called["args"][0] == loaders.TemplatesDirectories.GITHUB_PARAMETERS_TEMPLATE_RAW_URL
    assert called["args"][1] == loaders.TemplatesDirectories.era5_parameters_master_file()
    assert called["args"][2] is True


def test_download_parameters_from_github_non_colab(monkeypatch):
    monkeypatch.setattr(loaders, "is_in_colab", lambda: False)
    called = {"hit": False}

    def fake_download(*_args, **_kwargs):
        called["hit"] = True

    monkeypatch.setattr(loaders, "download_template", fake_download)
    loaders.download_parameters_from_github(force=False)
    assert called["hit"] is False


def test_load_parameters_from_template(tmp_path):
    lines = [
        "dataset: reanalysis-era5-pressure-levels",
        "product_type: [reanalysis]",
        "variable: [temperature]",
        "year: [2020]",
        "month: [01]",
        "day: [01]",
        "time: [00:00]",
        "area: [0, 0, 0, 0]",
        "pressure_level: [1000]",
        "data_format: [netcdf]",
        "download_format: [unarchived]",
        "",
    ]
    content = "\n".join(lines)
    path = tmp_path / "params.yaml"
    path.write_text(content)

    params = loaders.load_parameters_from_template(path)
    assert params.dataset == "reanalysis-era5-pressure-levels"
    assert params.variable == ["temperature"]
