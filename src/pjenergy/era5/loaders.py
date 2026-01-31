from pathlib import Path

from pjenergy.config.paths import TemplatesDirectories
from pjenergy.io.yaml import read_yaml
from pjenergy.utils.colab import is_in_colab, download_template
from pjenergy.era5.parameters import ERA5Parameters
from pjenergy.io.ask import is_answer_yes, ask_value

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
    cds_dict = p.to_cds_dict()
    print(cds_dict)
    #print(p.count_parameter_combinations())