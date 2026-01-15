from pathlib import Path

from .client import create_era5_client
from .parameters import load_parameters_from_template

def request_era5():

    client = create_era5_client()

    parameters = load_parameters_from_template()
    dataset = parameters.dataset
    request = parameters.to_cds_dict()

    client.retrieve(dataset, request, Path.home() / "test")