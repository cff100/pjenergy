from dataclasses import dataclass
from typing import Sequence

@dataclass
class ERA5Request:
    dataset: str
    product_type: Sequence[str]
    variables: Sequence[str]
    years: Sequence[str]
    months: Sequence[str]
    days: Sequence[str]
    times: Sequence[str]
    area: Sequence[float]
    pressure_levels: Sequence[str]
    data_format: Sequence[str]
    download_format: Sequence[str]

    def to_cds_dict(self) -> dict:
        