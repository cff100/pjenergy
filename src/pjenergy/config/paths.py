from pathlib import Path

class BasicDirectories:

    PJENERGY_PATH = Path(__file__).parents[1]

    COLAB_CONTENT_PATH = Path("/content")

    @staticmethod
    def default_cdsapirc_path() -> Path:
        return Path.home() / ".cdsapirc"
    
    TEMPLATES_PATH = PJENERGY_PATH / "templates"
    COLAB_TEMPLATES_PATH = COLAB_CONTENT_PATH / "templates"

class TemplatesDirectories:

    PARAMETERS_TEMPLATE_PATH = BasicDirectories.TEMPLATES_PATH / "era5_parameters.yaml"
    COLAB_PARAMETERS_TEMPLATE_PATH = BasicDirectories.COLAB_TEMPLATES_PATH / "era5_parameters.yaml"
    GITHUB_PARAMETERS_TEMPLATE_RAW_URL = "https://raw.githubusercontent.com/cff100/pjenergy/refs/heads/refactor/arquitetura/src/pjenergy/templates/era5_parameters.yaml"

if __name__ == "__main__":
    print(BasicDirectories.PJENERGY_PATH)