from pathlib import Path
from typing import Optional
import cdsapi


from pjenergy.config.paths import BasicDirectories


def create_era5_client_doc(key: str , 
                           url: str="https://cds.climate.copernicus.eu/api",
                           path: Optional[Path] = None):
    
    path = path or BasicDirectories.cdsapirc()
    path.write_text(f"url: {url}\nkey: {key}\n")


def create_era5_client() -> cdsapi.Client:
    return cdsapi.Client()