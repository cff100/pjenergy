from pathlib import Path

class BasicDirectories:

    PJENERGY_PATH = Path(__file__).parents[1]

    @staticmethod
    def default_cdsapirc_path() -> Path:
        return Path.home() / ".cdsapirc"
    

if __name__ == "__main__":
    print(BasicDirectories.PJENERGY_PATH)