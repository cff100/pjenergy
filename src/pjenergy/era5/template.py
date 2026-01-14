from pathlib import Path
from pjenergy.config.paths import BasicDirectories
from pjenergy.io.read_yaml import read_yaml
from .request import ERA5Request

def load_request_from_template(path: Path = BasicDirectories.PJENERGY_PATH / "templates" / "era5_parameters"):
    data = read_yaml(path)

    return ERA5Request(**data)