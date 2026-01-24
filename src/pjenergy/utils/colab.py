import subprocess
from pathlib import Path

from pjenergy.io.ask import is_answer_yes

def is_in_colab() -> bool:

    try:
        import google.colab # type: ignore
        IN_COLAB = True
    except:
        IN_COLAB = False

    return IN_COLAB


def execute_curl_donwload_command(raw_url: str, destiny_path: Path):
    subprocess.run(["curl", "-sSL", "-o", str(destiny_path), raw_url], check=True)
    


def download_template_from_github(raw_url: str, colab_path: Path) -> None:
        print(f"Downloading template from github: {raw_url} to {colab_path} ...")
        execute_curl_donwload_command(raw_url, colab_path)
        print("Download concluído.")
        print(f"Now you can edit it freely in Colab. Go to {colab_path}")


def download_template(raw_url: str, colab_path: Path, force: bool = False) -> None:

    if not colab_path.exists() or force:
        download_template_from_github(raw_url, colab_path)
    else: 
        if is_answer_yes("File already exists. Replace? (Y/N): "):
            download_template_from_github(raw_url, colab_path)

        

