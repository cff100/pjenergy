from pathlib import Path

import pjenergy.config.paths as paths


def test_cdsapirc_path():
    assert paths.BasicDirectories.cdsapirc() == Path.home() / ".cdsapirc"


def test_content_root_local(monkeypatch):
    monkeypatch.setattr(paths, "is_in_colab", lambda: False)
    expected = Path(paths.__file__).resolve().parents[3]
    assert paths.BasicDirectories.content_root() == expected


def test_content_root_colab(monkeypatch):
    monkeypatch.setattr(paths, "is_in_colab", lambda: True)
    assert paths.BasicDirectories.content_root() == Path("/content")


def test_build_from_root(monkeypatch, tmp_path):
    monkeypatch.setattr(paths.BasicDirectories, "content_root", lambda: tmp_path)
    assert paths.BasicDirectories.build_from_root("a/b") == tmp_path / "a" / "b"


def test_build_relative_paths():
    base = Path("/base")
    assert paths.BasicDirectories.build_relative_paths(base, None) == base
    assert paths.BasicDirectories.build_relative_paths(base, "x") == base / "x"


def test_templates_and_data(monkeypatch, tmp_path):
    monkeypatch.setattr(paths.BasicDirectories, "build_from_root", lambda rel: tmp_path / rel)
    assert paths.BasicDirectories.templates("x") == tmp_path / "templates" / "x"
    assert paths.BasicDirectories.data("y") == tmp_path / "data" / "y"


def test_templates_directories(monkeypatch, tmp_path):
    def fake_templates(rel=None):
        return tmp_path / rel if rel else tmp_path
    monkeypatch.setattr(paths.BasicDirectories, "templates", fake_templates)
    assert paths.TemplatesDirectories.era5_parameters("foo") == tmp_path / "era5_parameters" / "foo"
    assert paths.TemplatesDirectories.era5_parameters_master_file() == tmp_path / "era5_parameters" / "master.yaml"
    assert paths.TemplatesDirectories.era5_parameters_temp_file("t.yaml") == tmp_path / "era5_parameters" / "tmp" / "t.yaml"


def test_data_directories(monkeypatch, tmp_path):
    monkeypatch.setattr(paths.BasicDirectories, "data", lambda rel=None: tmp_path / rel)
    assert paths.DataDirectories.cds() == tmp_path / "cds.nc"
