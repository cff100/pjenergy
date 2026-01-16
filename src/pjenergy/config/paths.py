from pathlib import Path

from pjenergy.utils.colab import is_in_colab

class BasicDirectories:

    @staticmethod
    def cdsapirc() -> Path:
        return Path.home() / ".cdsapirc"
    
    @staticmethod
    def content_root() -> Path:
        if is_in_colab():
            return Path("/content")
        else:
            return Path(__file__).parents[3]

    @staticmethod
    def build_from_root(relative_path: str | Path) -> Path:
        path = BasicDirectories.content_root() / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def templates() -> Path:
        return BasicDirectories.build_from_root("templates")
    
    @staticmethod
    def data() -> Path:
        return BasicDirectories.build_from_root("data")
    

class TemplatesDirectories:

    @staticmethod
    def parameters() -> Path:
        return BasicDirectories.templates() / "era5_parameters.yaml"

    GITHUB_PARAMETERS_TEMPLATE_RAW_URL = "https://raw.githubusercontent.com/cff100/pjenergy/refs/heads/refactor/arquitetura/templates/era5_parameters.yaml"


class DataDirectories:

    @staticmethod
    def cds() -> Path:
        return BasicDirectories.data() / "cds"


if __name__ == "__main__":
    pass