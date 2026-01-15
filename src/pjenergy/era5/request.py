from pathlib import Path

from .client import create_era5_client
from .parameters import load_parameters_from_template, write_parameters_template_in_colab

def request_era5():

    client = create_era5_client()

    write_parameters_template_in_colab()
    parameters = load_parameters_from_template()
    dataset = parameters.dataset
    request = parameters.to_cds_dict()

    client.retrieve(dataset, request, Path.home() / "test")