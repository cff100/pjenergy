
import cdsapi


from pjenergy.config.paths import BasicDirectories


def create_cdsapi_client_doc(key: str , 
                           url: str="https://cds.climate.copernicus.eu/api") -> None:
    """
    
    :param key: CDS API personal key.
    :type key: str
    :param url: CDS API url.
    :type url: str
    """
    
    path = BasicDirectories.cdsapirc()
    path.write_text(f"url: {url}\nkey: {key}\n")
    print("CDS API client document created.")


def create_cdsapi_client() -> cdsapi.Client:
    return cdsapi.Client()


if __name__ == "__main__":
    create_cdsapi_client_doc("")