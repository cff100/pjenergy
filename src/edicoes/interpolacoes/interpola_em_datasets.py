import xarray as xr
import numpy as np
from config.constants import ConstantesNumericas as cn



def dataset_interpola_lat_lon(dataset: xr.Dataset, latitude_longitude_alvo: tuple[float, float]) -> xr.Dataset:
    """Faz a interpolação das variáveis na longitude e latitude
    
    Parâmetros:
    latitude_logitude_alvo: Mínimo: (-24.0,-42.0) - Máximo: (-21.0,-39.0)"""

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

    # Remove as dimensões de latitude e longitude
    for dim in ["latitude", "longitude"]:
        if dim in ds_interp.dims:
            ds_interp = ds_interp.squeeze(dim)
        if dim in ds_interp.coords or dim in ds_interp.variables:
            ds_interp = ds_interp.drop_vars(dim)
            
    return ds_interp



def interp_alturas_constantes(ds: xr.Dataset) -> xr.Dataset:
    """
    Interpola as variáveis do dataset para alturas constantes em metros,
    usando o geopotencial para calculá-las.

    Retorna um novo Dataset com variáveis em função de altura e tempo,
    e com a pressão estimada como variável interpolada.
    """

    # -----------------------------
    # ETAPA 1: Definir alturas alvo
    # -----------------------------
    # Essas são as alturas (em metros) para as quais queremos valores interpolados.
    alturas_desejadas = np.arange(25, 401, 25)

    # -----------------------------
    # ETAPA 2: Calcular altura a partir do geopotencial
    # -----------------------------
    # O geopotencial 'z' tem unidade m²/s². Ao dividir pela aceleração da gravidade,
    # obtemos a altura geométrica (em metros): h = z / g.
    # Isso resulta em um DataArray com dimensões (valid_time, pressure_level).
    h = ds["z"] / cn.G

    # -----------------------------
    # ETAPA 3: Identificar variáveis a serem interpoladas
    # -----------------------------
    # Seleciona apenas variáveis com as dimensões exatas (valid_time, pressure_level),
    # que são as variáveis que fazem sentido serem interpoladas verticalmente.
    variaveis = [
        var for var in ds.data_vars
        if set(ds[var].dims) == {"valid_time", "pressure_level"}
    ]

    # Inicializa um novo Dataset que irá armazenar os resultados interpolados
    ds_interp = xr.Dataset()

    # -----------------------------
    # ETAPA 4: Função auxiliar de interpolação 1D
    # -----------------------------
    # Essa função recebe vetores 1D de altura (h) e da variável (var),
    # e retorna os valores da variável interpolados para as alturas desejadas.
    def interp_1d(h_valores, var_valores, alturas):
        # Ordena os valores de altura (por segurança)
        ordenado = np.argsort(h_valores)
        # Interpola (linear por padrão)
        return np.interp(alturas, h_valores[ordenado], var_valores[ordenado])

    # -----------------------------
    # ETAPA 5: Aplicar interpolação nas variáveis
    # -----------------------------
    # Para cada variável relevante do Dataset:
    for var in variaveis:
        # Aplica a função de interpolação com xarray.apply_ufunc,
        # o que permite operação vetorizada.
        da_interp = xr.apply_ufunc(
            interp_1d,              # Função que será aplicada de forma vetorizada
            h,                      # Altura real calculada (como base para interpolação)
            ds[var],                # Dados da variável a interpolar
            input_core_dims=[["pressure_level"], ["pressure_level"]],
            output_core_dims=[["altura"]],
            vectorize=True,         # Aplica elemento a elemento nos outros eixos (no caso, no tempo)
            dask="parallelized",    # Permite processamento paralelo com Dask
            kwargs={"alturas": alturas_desejadas},  # Alturas alvo
            output_dtypes=[ds[var].dtype]         # Tipo de saída
        )
        # Armazena no novo dataset
        ds_interp[var] = da_interp

    # -----------------------------
    # ETAPA 6: Interpolar também a pressão
    # -----------------------------
    # A pressão é originalmente uma coordenada, mas aqui queremos que ela vire uma variável,
    # representando a pressão estimada correspondente às alturas desejadas.
    # Para isso, usamos a mesma técnica de interpolação.
    pressao_valores = ds["pressure_level"]

    # Como 'pressure_level' não depende do tempo, usamos broadcast_like(h)
    # para replicar os valores de pressão ao longo da dimensão 'valid_time'
    da_pressao_interp = xr.apply_ufunc(
        interp_1d,
        h,                                 # altura (h) calculada  / 1º argumento -> h_vals → ["pressure_level"]
        pressao_valores.broadcast_like(h),    # pressão replicada no tempo / 2º argumento -> var_vals → ["pressure_level"]
        input_core_dims=[["pressure_level"], ["pressure_level"]],
        output_core_dims=[["altura"]],
        vectorize=True,
        dask="parallelized",
        kwargs={"alturas": alturas_desejadas},
        output_dtypes=[pressao_valores.dtype],
    )

    # Adiciona a pressão como uma nova variável no dataset resultante
    ds_interp["pressure_level"] = da_pressao_interp

    # -----------------------------
    # ETAPA 7: Adicionar coordenada de altura
    # -----------------------------
    # Para fins de organização, adicionamos explicitamente a coordenada 'altura'
    ds_interp = ds_interp.assign_coords(altura=("altura", alturas_desejadas))

    # -----------------------------
    # ETAPA 8: Reorganizar as dimensões
    # -----------------------------
    # Garante que as dimensões fiquem na ordem desejada: (tempo, altura)
    ds_interp = ds_interp.transpose("valid_time", "altura")

    return ds_interp