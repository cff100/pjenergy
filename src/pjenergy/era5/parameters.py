from dataclasses import dataclass, asdict
from typing import Sequence
from pathlib import Path
from math import prod

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
        self.cds_dict = asdict(self)
        del self.cds_dict["dataset"]

        return self.cds_dict
    
    def count_parameter_combinations(self):
        self.dict = asdict(self)
        del self.dict["area"] # The area is not relevant to the requisition load
        self.parameters_count_dict = {
            k: (len(v) if not isinstance(v, str) else 1)
            for (k, v) in self.dict.items() 
        }
        self.parameters_combinations = prod(self.parameters_count_dict.values())

        return self.parameters_combinations
        

def download_parameters_from_github(force: bool = False) -> None:
    """    
    :param force: If the file already exists, force a replacement.
    :type force: bool
    """

    if is_in_colab():
        download_template(TemplatesDirectories.GITHUB_PARAMETERS_TEMPLATE_RAW_URL, 
                                      TemplatesDirectories.era5_parameters_master_file(), force)


def load_parameters_from_template(file_path: Path = TemplatesDirectories.era5_parameters_master_file()) -> ERA5Parameters:
    data = read_yaml(file_path)
    return ERA5Parameters(**data)


if __name__ == "__main__":
    p = load_parameters_from_template()
    # cds_dict = p.to_cds_dict()
    # print(cds_dict)
    print(p.count_parameter_combinations())
    

