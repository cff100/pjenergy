from dataclasses import dataclass
from typing import Sequence
from pjenergy.config.paths import TemplatesDirectories
from pjenergy.io.yaml import read_yaml
from pjenergy.utils.colab import is_in_colab, download_template


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


def download_parameters_from_github(force: bool = False) -> None:
    """    
    :param force: If the file already exists, force a replacement.
    :type force: bool
    """

    if is_in_colab():
        download_template(TemplatesDirectories.GITHUB_PARAMETERS_TEMPLATE_RAW_URL, 
                                      TemplatesDirectories.era5_parameters_master_file(), force)


def load_parameters_from_template() -> ERA5Parameters:

    data = read_yaml(TemplatesDirectories.era5_parameters_master_file())

    return ERA5Parameters(**data)


