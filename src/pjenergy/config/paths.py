from pathlib import Path

class BasicDirectories:

    @staticmethod
    def default_cdsapirc_path() -> Path:
        return Path.home() / ".cdsapirc"