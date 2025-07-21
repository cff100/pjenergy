import xarray as xr
import numpy as np
from config.constants import OutrasConstantes as oc, ConstantesNumericas as cn



def dataset_interpola_lat_lon(dataset: xr.Dataset, latitude_longitude_alvo: tuple[float, float]) -> xr.Dataset:
    """Aplica a interpolação das dimensões de longitude e latitude do dataset e depois as remove.
    
    Args:
        dataset (xr.Dataset): Dataset a ser manipulado.
        latitude_longitude_alvo (tuple[float, float]): Par latitude-longitude em que se deseja aplicar a interpolação. 
            Mínimo: (-24.0,-42.0) - Máximo: (-21.0,-39.0)."""

    # Verifica se os pontos de latitude e longitude estão dentro do intervalo do dataset
    if not (dataset.latitude.min() <= latitude_longitude_alvo[0] <= dataset.latitude.max() and
            dataset.longitude.min() <= latitude_longitude_alvo[1] <= dataset.longitude.max()):
        raise ValueError(
            f"Os pontos de latitude {latitude_longitude_alvo[0]} e longitude {latitude_longitude_alvo[1]} estão fora do intervalo do dataset. \
            Mínimo: ({dataset.latitude.min().item()},{dataset.longitude.min().item()}) - \
            Máximo: ({dataset.latitude.max().item()},{dataset.longitude.max().item()})"
            )
    
    # Interpola as variáveis
    ds_interp = dataset.interp(latitude=latitude_longitude_alvo[0], longitude = latitude_longitude_alvo[1], method="linear")


    # Neste trecho, removemos as dimensões e variáveis 'latitude' e 'longitude' do dataset interpolado (ds_interp)
    # Isso é comum após uma interpolação para um ponto específico (ou poucos pontos),
    # em que essas dimensões acabam ficando com tamanho 1 e, portanto, se tornam desnecessárias.
    # Além disso, mantê-las pode atrapalhar operações posteriores (como cálculos ou concatenações),
    # pois o xarray ainda consideraria essas dimensões mesmo que não tenham mais variação.
    for dim in ["latitude", "longitude"]:
        # Se a dimensão ainda estiver presente nas dimensões do dataset (e.g. com tamanho 1), removemos com squeeze
        if dim in ds_interp.dims:
            # 'squeeze' remove dimensões com tamanho 1, transformando variáveis de [1, n] para [n], por exemplo
            ds_interp = ds_interp.squeeze(dim)

        # Se a dimensão também estiver presente como coordenada ou variável explícita, ela é removida
        if dim in ds_interp.coords or dim in ds_interp.variables:
            # 'drop_vars' remove completamente a variável ou coordenada do dataset
            ds_interp = ds_interp.drop_vars(dim)

    # Retorna o dataset limpo, sem as dimensões e variáveis redundantes de latitude/longitude
    return ds_interp


# -----------------------------------------------------------------------------------------------------------------------------------


def interp_por_altura(h: np.ndarray, var: np.ndarray, alturas_interp: np.ndarray = oc.ALTURAS_DESEJADAS) -> np.ndarray:
    """Interpolação linear de uma variável 'var' em função da altura 'h' para alturas especificadas em 'alturas_interp'.
    
    Args:
        h (np.ndarray): Array de alturas correspondentes aos valores da variável 'var'.
        var (np.ndarray): Array de valores da variável a ser interpolada.
        alturas_interp (np.ndarray, optional): Alturas alvo para interpolação. Default é oc.ALTURAS_DESEJADAS.

    Returns:
        np.ndarray: Valores interpolados da variável 'var' nas alturas especificadas em 'alturas_interp'.
    """

    # Ordena os arrays de altura e, de forma correspondente, a variável
    ordenado = np.argsort(h)
    h_ordenado = h[ordenado]
    var_ordenado = var[ordenado]

    # Realiza a interpolação linear
    return np.interp(alturas_interp, h_ordenado, var_ordenado)


def interpolar_variavel_em_altura(var_name: str, h: xr.DataArray, ds: xr.Dataset) -> xr.DataArray:
    """Interpolação de uma variável específica do dataset em função da altura.

    Args:
        var_name (str): Nome da variável a ser interpolada.
        h (xr.DataArray): Array de alturas correspondentes aos valores da variável.
        ds (xr.Dataset): Dataset original contendo a variável a ser interpolada.

    Returns:
        xr.DataArray: Array de dados interpolados da variável nas alturas especificadas.
    """

    alturas_desejadas = oc.ALTURAS_DESEJADAS

    return xr.apply_ufunc(
        interp_por_altura,
        h,     # Função a ser aplicada                                                 
        ds[var_name], # Dados da variável original
        kwargs={'alturas_interp': alturas_desejadas}, # Alturas alvo para interpolação
        input_core_dims=[['pressure_level'], ['pressure_level']], # Dimensões de entrada: pressão 
        output_core_dims=[['altura']], # Dimensão de saída: altura
        vectorize=True, # Aplica a função para cada tempo automaticamente
        dask='parallelized', # Permite execução paralela (útil para grandes volumes de dados)
        output_dtypes=[float], # Tipo de dado da saída (float, pois estamos interpolando valores contínuos)
    ).assign_coords(altura=alturas_desejadas) # Atribui as alturas desejadas como coordenada do resultado


def interpola_varias_variaveis_em_altura(dataset: xr.Dataset) -> xr.Dataset:
    """Aplica a interpolação de várias variáveis do dataset em função da altura.
    
    Args:
        dataset (xr.Dataset): Dataset contendo as variáveis a serem interpoladas.
    Returns:
        xr.Dataset: Dataset com as variáveis interpoladas nas alturas especificadas.
    """
    
    # Lista de variáveis que serão interpoladas
    variaveis = ["u", "v", "z", "r", "t"]

    # Cria um novo dataset para armazenar as variáveis interpoladas
    ds_interp = xr.Dataset()

    h = dataset["z"] / cn.G  # Altura em metros, obtida da variável de geopotencial do dataset

    # Interpola cada variável na lista
    for var in variaveis:
        ds_interp[var] = interpolar_variavel_em_altura(var, h, dataset)

    return ds_interp

