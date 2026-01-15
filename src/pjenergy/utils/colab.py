import subprocess
from pathlib import Path


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


def download_template_from_github(raw_url: str, colab_path: Path):
  
    if not colab_path.exists():
        colab_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading from github: {raw_url} ...")
        execute_curl_command(raw_url, colab_path)
        print("Now you can edit it freely in Colab.")
    else: 
        print(f"The {colab_path} already exists in Colab.")
        replace = None
        while replace not in ["Y", "N"]:
            replace = input("Do you want to replace it? (Y / N)")
        if replace == "Y":
            print(f"Downloading from github: {raw_url} ...")
            execute_curl_command(raw_url, colab_path)
            print("Now you can edit it freely in Colab.")
        else: 
            return