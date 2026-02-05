from pjenergy.io.yaml import read_yaml, write_yaml


def test_read_write_yaml(tmp_path):
    path = tmp_path / "data.yaml"
    write_yaml("a: 1\n", path)
    assert path.read_text() == "a: 1\n"
    assert read_yaml(path) == {"a": 1}
