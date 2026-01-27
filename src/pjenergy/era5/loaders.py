from pathlib import Path

from pjenergy.config.paths import TemplatesDirectories
from pjenergy.io.yaml import read_yaml
from pjenergy.utils.colab import is_in_colab, download_template
from pjenergy.era5.parameters import ERA5Parameters

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


def prompt_for_combination_limit(self, allowed_combination_limit: int = 600, force: bool = False) -> None:

    while allowed_combination_limit >= 5400 and not force:
        if allowed_combination_limit >= 6000:
            print(f"{allowed_combination_limit} combinations is a very costly request. \
                The request will not be prioritized and even risks not being accepted by the CDS. \
                A lower value is better.")
        else:
            print(f"{allowed_combination_limit} combinations is a request of considerable size, \
                so it will not be prioritized by the CDS. 600 is better value")
            
        if is_answer_yes(f"Do you want to keep this value ({allowed_combination_limit} combinations)?"):
            break
        
        
        allowed_combination_limit = ask_value("What value do you want?")

    return 


def validate_parameter_combination_count(self, allowed_combination_limit: int = 600, force: bool = False) -> bool:
    
    is_valid = self.is_within_combinations_limit(allowed_combination_limit)
    self.prompt_for_combination_limit(allowed_combination_limit, force)

    return is_valid


if __name__ == "__main__":
    p = load_parameters_from_template()
    cds_dict = p.to_cds_dict()
    print(cds_dict)
    #print(p.count_parameter_combinations())