from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence
import cdsapi

from pjenergy.config.paths import BasicDirectories


def create_era5_client_doc(key: str , 
                           url: str="https://cds.climate.copernicus.eu/api",
                           path: Optional[Path] = None):
    
    path = path or BasicDirectories.default_cdsapirc_path()
    path.write_text(f"url: {url}\nkey: {key}\n")



@dataclass
class ERA5Request:
    dataset: str
    variable: Sequence[str]
    year: str
    month: Sequence[str] | None = None
    day: Sequence[str] | None = None
    time: Sequence[str] | None = None
    product_type: str = "reanalysis"
    format: str = "netcdf"



def request_era5():

    client = cdsapi.Client()
    
    dataset = 'reanalysis-era5-pressure-levels'
    request = {
    'product_type': ['reanalysis'],
    'variable': variavel,
    'year': ano,
    'month': pod.MESES,
    'day': pod.DIAS,
    'time': pod.HORAS,
    'area': pod.AREA,  
    'pressure_level': pressao_nivel,  # Em hPa
    'data_format': pod.DATA_FORMAT,
    'download_format': pod.DOWNLOAD_FORMAT
    }

    c.retrieve(dataset, request, dataset_salvamento_caminho)