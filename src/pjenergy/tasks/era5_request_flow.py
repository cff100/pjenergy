from pjenergy.era5.parameters import ERA5Parameters


def validate_parameters(param: ERA5Parameters, limit: int = 600, force: bool = False):

    combinations = param.count_parameter_combinations()

    