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


def load_parameters_from_template():

    if is_in_colab():
        download_template_from_github(TemplatesDirectories.GITHUB_PARAMETERS_TEMPLATE_RAW_URL, 
                                      TemplatesDirectories.COLAB_PARAMETERS_TEMPLATE_PATH)
        data = read_yaml(TemplatesDirectories.COLAB_PARAMETERS_TEMPLATE_PATH)
    else:
        data = read_yaml(TemplatesDirectories.PARAMETERS_TEMPLATE_PATH)

    return ERA5Parameters(**data)


