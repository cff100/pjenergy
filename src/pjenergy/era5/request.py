
from pjenergy.era5.client import create_cdsapi_client
from pjenergy.era5.parameters import load_parameters_from_template
from pjenergy.config.paths import DataDirectories

def request_era5() -> None:

    client = create_cdsapi_client()

    parameters = load_parameters_from_template()
    dataset = parameters.dataset
    request = parameters.to_cds_dict()

    client.retrieve(dataset, request, DataDirectories.cds())


if __name__ == "__main__":
    request_era5()