"""Path helpers for locating project directories and template files."""

from pathlib import Path
from typing import Optional

from pjenergy.utils.colab import is_in_colab

class BasicDirectories:
    """Base path helpers for local and Colab environments."""

    @staticmethod
    def cdsapirc() -> Path:
        """Return the default path for the CDS API credentials file."""
        return Path.home() / ".cdsapirc"
    
    @staticmethod
    def content_root() -> Path:
        """Return the root directory used by the project."""
        return Path("/content") if is_in_colab() else Path(__file__).parents[3]


    @staticmethod
    def build_from_root(relative_path: str | Path) -> Path:
        """
        Build an absolute path from a path relative to the project root.

        :param relative_path: Path in relation to the project's root.
        :type relative_path: str | Path
        :return: Absolute path.
        :rtype: Path
        """
        path = BasicDirectories.content_root() / relative_path
        return path
    
    @staticmethod
    def build_relative_paths(base_path: Path | str, relative_path: Optional[Path | str]) -> Path:
        """Combine a base path with an optional relative path segment."""
        base_path = Path(base_path)
        return base_path / relative_path if relative_path else base_path

    @staticmethod
    def templates(relative_path: Optional[Path | str] = None) -> Path:
        """Return the templates directory, optionally joined with a subpath."""
        path = BasicDirectories.build_relative_paths("templates", relative_path)
        return BasicDirectories.build_from_root(path)
    
    @staticmethod
    def data(relative_path: Optional[Path | str] = None) -> Path:
        """Return the data directory, optionally joined with a subpath."""
        path = BasicDirectories.build_relative_paths("data", relative_path)
        return BasicDirectories.build_from_root(path)
    

class TemplatesDirectories:
    """Helpers for template file locations."""

    @staticmethod
    def era5_parameters(relative_path: Optional[Path | str] = None) -> Path:
        """Return the ERA5 parameters template directory or a subpath."""
        path = BasicDirectories.build_relative_paths("era5_parameters", relative_path)
        return BasicDirectories.templates(path) 
    
    @staticmethod
    def era5_parameters_master_file() -> Path:
        """Return the main ERA5 parameters template path."""
        return TemplatesDirectories.era5_parameters("master.yaml")
    
    @staticmethod
    def era5_parameters_temp_file(file_name: str | Path) -> Path:
        """Return the temporary ERA5 parameters template path for a filename."""
        return TemplatesDirectories.era5_parameters(f"tmp/{file_name}")
    

    GITHUB_PARAMETERS_TEMPLATE_RAW_URL = "https://raw.githubusercontent.com/cff100/pjenergy/refs/heads/refactor/arquitetura/templates/era5_parameters/master.yaml"


class DataDirectories:
    """Helpers for data file locations."""

    @staticmethod
    def cds() -> Path:
        """Return the default ERA5 CDS output path."""
        return BasicDirectories.data("cds.nc")


if __name__ == "__main__":
    # path = TemplatesDirectories.era5_parameters_master_file()
    path = TemplatesDirectories.era5_parameters()
    print(path)
