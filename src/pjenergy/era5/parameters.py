from dataclasses import dataclass
from typing import Sequence
from pathlib import Path
from pjenergy.config.paths import TemplatesDirectories
from pjenergy.io.yaml import read_yaml
from pjenergy.utils.colab import is_in_colab, download_template_from_github


@dataclass
class ERA5Parameters:
    dataset: str
    product_type: Sequence[str]
    variable: Sequence[str]
    year: Sequence[str]
    month: Sequence[str]
    day: Sequence[str]
    time: Sequence[str]
    area: Sequence[float]
    pressure_level: Sequence[str]
    data_format: Sequence[str]
    download_format: Sequence[str]

    def to_cds_dict(self) -> dict:
        cds_dict = {}
        cds_dict["product_type"] = self.product_type
        cds_dict["variable"] = self.variable
        cds_dict["year"] = self.year
        cds_dict["month"] = self.month
        cds_dict["day"] = self.day
        cds_dict["time"] = self.time
        cds_dict["area"] = self.area
        cds_dict["pressure_level"] = self.pressure_level
        cds_dict["data_format"] = self.data_format
        cds_dict["download_format"] = self.download_format

        return cds_dict


def download_parameters_from_github():

    if is_in_colab():
        download_template_from_github(TemplatesDirectories.GITHUB_PARAMETERS_TEMPLATE_RAW_URL, 
                                      TemplatesDirectories.COLAB_PARAMETERS_TEMPLATE_PATH)

def load_parameters_from_template():

    if is_in_colab():
        data = read_yaml(TemplatesDirectories.COLAB_PARAMETERS_TEMPLATE_PATH)
    else:
        data = read_yaml(TemplatesDirectories.PARAMETERS_TEMPLATE_PATH)

    return ERA5Parameters(**data)


