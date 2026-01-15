from dataclasses import dataclass
from typing import Sequence
from pathlib import Path
from pjenergy.config.paths import BasicDirectories
from pjenergy.io.read_yaml import read_yaml


@dataclass
class ERA5Parameters:
    dataset: str
    product_type: Sequence[str]
    variables: Sequence[str]
    years: Sequence[str]
    months: Sequence[str]
    days: Sequence[str]
    times: Sequence[str]
    area: Sequence[float]
    pressure_levels: Sequence[str]
    data_format: Sequence[str]
    download_format: Sequence[str]

    def to_cds_dict(self) -> dict:
        cds_dict = {}
        cds_dict["product_type"] = self.product_type
        cds_dict["variables"] = self.variables
        cds_dict["years"] = self.years
        cds_dict["months"] = self.months
        cds_dict["days"] = self.days
        cds_dict["times"] = self.times
        cds_dict["area"] = self.area
        cds_dict["pressure_levels"] = self.pressure_levels
        cds_dict["data_format"] = self.data_format
        cds_dict["download_format"] = self.download_format

        return cds_dict




def load_parameters_from_template(path: Path = BasicDirectories.PJENERGY_PATH / "templates" / "era5_parameters"):
    data = read_yaml(path)

    return ERA5Parameters(**data)


