import subprocess
from pathlib import Path

from pjenergy.utils.path_existence import ask_replace_file

def is_in_colab() -> bool:

    try:
        import google.colab # type: ignore
        IN_COLAB = True
    except:
        IN_COLAB = False

    return IN_COLAB


def execute_curl_command(raw_url: str, destiny_path: Path):
    print(f"Downloading template to {destiny_path} ...")
    subprocess.run(["curl", "-sSL", "-o", str(destiny_path), raw_url], check=True)
    print("Download concluído.")


def download_template_from_github(raw_url: str, colab_path: Path) -> None:
        print(f"Downloading from github: {raw_url} ...")
        execute_curl_command(raw_url, colab_path)
        print("Now you can edit it freely in Colab.")


def download_template(raw_url: str, colab_path: Path, force: bool = False) -> None:

    if not colab_path.exists() or force:
        download_template_from_github(raw_url, colab_path)
    else: 
        if ask_replace_file():
            download_template_from_github(raw_url, colab_path)

        

