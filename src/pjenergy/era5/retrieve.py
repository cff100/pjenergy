from pathlib import Path
import cdsapi

from .client import create_era5_client
from .template import load_request_from_template

def retrieve_era5():

    client = create_era5_client()

    req = load_request_from_template()

    dataset = req.dataset
    
    request = req

    client.retrieve(dataset, request, Path.home() / "test")