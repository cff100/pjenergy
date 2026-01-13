from pathlib import Path
from typing import Optional 
import cdsapi

from pjenergy.config.paths import BasicDirectories


def create_era5_client_doc(key: str , 
                           url: str="https://cds.climate.copernicus.eu/api",
                           path: Optional[Path] = None):
    
    path = path or BasicDirectories.default_cdsapirc_path()
    path.write_text(f"url: {url}\nkey: {key}\n")


def request_era5():

    client = cdsapi.Client()
    pass