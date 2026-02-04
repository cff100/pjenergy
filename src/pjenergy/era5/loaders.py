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



if __name__ == "__main__":
    data = {'dataset': ['reanalysis-era5-pressure-levels'], 'product_type': ['reanalysis'], 'variable': ['u_component_of_wind', 'v_component_of_wind', 'relative_humidity', 'temperature', 'geopotential'], 'year': ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'], 'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'], 'day': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], 'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'], 'area': [-21, -42, -24, -39], 'pressure_level': ['900', '925', '950', '975', '1000'], 'data_format': 'netcdf', 'download_format': 'unarchived'}
    #p = ERA5Parameters(**params)
    #print(p)
    # f = ERA5Parameters._fix_parameter(data, "variable")
    # print(f)
    # c = ERA5Parameters.count_parameter_combinations(data)
    # print(c)
    # l = ERA5Parameters.brake_depth(data, 2455200)
    # print(l)
    ll = ERA5Parameters.placeholder_02(data, 3)
    print(ll)
    # nd = ERA5Parameters.placeholder_01(data, "year")
    # print(nd)
    # cds_dict = p.to_cds_dict()
    #print(cds_dict)
    #print(p.count_parameter_combinations())