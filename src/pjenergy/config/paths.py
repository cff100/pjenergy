from pathlib import Path
from typing import Optional

from pjenergy.utils.colab import is_in_colab

class BasicDirectories:

    @staticmethod
    def cdsapirc() -> Path:
        return Path.home() / ".cdsapirc"
    
    @staticmethod
    def content_root() -> Path:
        return Path("/content") if is_in_colab() else Path(__file__).parents[3]


    @staticmethod
    def build_from_root(relative_path: str | Path) -> Path:
        """
        :param relative_path: Path in relation to the project's root.
        :type relative_path: str | Path
        :return: Absolute path.
        :rtype: Path
        """
        path = BasicDirectories.content_root() / relative_path
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def build_relative_paths(base_path: Path | str, relative_path: Optional[Path | str]) -> Path:
        base_path = Path(base_path)
        return base_path / relative_path if relative_path else base_path

    @staticmethod
    def templates(relative_path: Optional[Path | str] = None) -> Path:
        path = BasicDirectories.build_relative_paths("templates", relative_path)
        return BasicDirectories.build_from_root(path)
    
    @staticmethod
    def data(relative_path: Optional[Path | str] = None) -> Path:
        path = BasicDirectories.build_relative_paths("data", relative_path)
        return BasicDirectories.build_from_root(path)
    

class TemplatesDirectories:

    @staticmethod
    def era5_parameters(relative_path: Optional[Path | str] = None) -> Path:
        path = BasicDirectories.build_relative_paths("era5_parameters", relative_path)
        return BasicDirectories.templates(path) 
    
    @staticmethod
    def era5_parameters_master_file() -> Path:
        return TemplatesDirectories.era5_parameters("master.yaml")
    
    @staticmethod
    def era5_parameters_temp_file(file_name: str | Path) -> Path:
        return TemplatesDirectories.era5_parameters(f"tmp/{file_name}")
    

    GITHUB_PARAMETERS_TEMPLATE_RAW_URL = "https://raw.githubusercontent.com/cff100/pjenergy/refs/heads/refactor/arquitetura/templates/era5_parameters.yaml"


class DataDirectories:

    @staticmethod
    def cds() -> Path:
        return BasicDirectories.data("cds.nc")


if __name__ == "__main__":
    pass