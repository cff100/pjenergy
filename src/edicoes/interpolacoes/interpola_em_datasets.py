import xarray as xr
import numpy as np
from config.constants import ConstantesNumericas as cn



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



def interp_alturas_constantes(ds: xr.Dataset) -> xr.Dataset:
    """
    Interpola as variáveis do dataset para alturas constantes (em metros),
    usando o geopotencial como base para calcular essas alturas.

    Retorna um novo Dataset, agora com as variáveis expressas em função da altura (e não mais da pressão),
    e com a pressão estimada como uma variável comum (não mais uma coordenada).
    """

    # -----------------------------
    # ETAPA 1: Definir alturas alvo
    # -----------------------------
    # Essas são as alturas fixas para as quais queremos obter os dados.
    # Estamos pedindo valores de 25 em 25 metros, de 100 até 350 metros.
    # Isso nos permite estudar os dados em alturas regulares e controladas.
    alturas_desejadas = np.arange(100, 350, 25)

    # -----------------------------
    # ETAPA 2: Calcular altura a partir do geopotencial
    # -----------------------------
    # O geopotencial é uma medida de energia potencial por unidade de massa (em m²/s²),
    # e está disponível no dataset com o nome "z".
    # Ao dividirmos pelo valor da gravidade (g), obtemos a altura geométrica real em metros.
    # Isso nos dá, para cada tempo e nível de pressão, a altura correspondente.
    h = ds["z"] / cn.G  # cn.G é a aceleração da gravidade

    # -----------------------------
    # ETAPA 3: Identificar variáveis a serem interpoladas
    # -----------------------------
    # Queremos interpolar apenas as variáveis que estão organizadas com as dimensões:
    # (tempo, nível de pressão). Por exemplo, temperatura[tempo, pressão].
    # Isso evita tentar interpolar variáveis com outras dimensões, o que causaria erro.
    variaveis = [
        var for var in ds.data_vars
        if set(ds[var].dims) == {"valid_time", "pressure_level"}
    ]

    # Criamos um novo Dataset vazio onde vamos guardar os resultados interpolados
    ds_interp = xr.Dataset()

    # -----------------------------
    # ETAPA 4: Função auxiliar de interpolação 1D
    # -----------------------------
    # Essa função realiza a interpolação propriamente dita para cada linha de dados.
    # h_valores: vetor com alturas originais
    # var_valores: valores da variável nesses pontos
    # alturas: alturas para as quais queremos estimar os novos valores
    def interp_1d(h_valores, var_valores, alturas):
        # Por segurança, garantimos que os valores estejam em ordem crescente de altura
        ordenado = np.argsort(h_valores)
        # np.interp faz interpolação linear entre os pontos fornecidos
        return np.interp(alturas, h_valores[ordenado], var_valores[ordenado])

    # -----------------------------
    # ETAPA 5: Aplicar interpolação nas variáveis
    # -----------------------------
    # Para cada variável identificada anteriormente:
    for var in variaveis:
        # Aplicamos a função de interpolação usando xarray.apply_ufunc,
        # que permite aplicar funções NumPy em objetos xarray de forma vetorizada.
        da_interp = xr.apply_ufunc(
            interp_1d,              # Função a ser aplicada
            h,                      # Altura em metros (calculada com z/g)
            ds[var],                # Dados da variável original
            input_core_dims=[["pressure_level"], ["pressure_level"]],
            output_core_dims=[["h"]],  # Indicamos que a saída terá uma nova dimensão chamada 'h'
            vectorize=True,         # Aplica a função para cada tempo automaticamente
            dask="parallelized",    # Permite execução paralela (útil para grandes volumes de dados)
            kwargs={"alturas": alturas_desejadas},  # Passamos as alturas alvo como argumento fixo
            output_dtypes=[ds[var].dtype]  # Mantemos o mesmo tipo de dado da variável original
        )
        # Adicionamos a variável interpolada ao novo dataset
        ds_interp[var] = da_interp

    # -----------------------------
    # ETAPA 6: Interpolar também a pressão
    # -----------------------------
    # A pressão original (pressure_level) é uma coordenada no dataset,
    # mas como agora trabalhamos com altura como base, queremos saber
    # "qual a pressão estimada em cada uma dessas novas alturas".
    # Por isso, aplicamos a mesma interpolação.
    pressao_valores = ds["pressure_level"]

    # Como a pressão depende só do nível e não do tempo,
    # usamos broadcast_like para replicá-la ao longo do tempo
    # e permitir que a função de interpolação funcione corretamente.
    da_pressao_interp = xr.apply_ufunc(
        interp_1d,
        h,                                 # Altura calculada a partir do geopotencial
        pressao_valores.broadcast_like(h),  # Pressão replicada para cada tempo
        input_core_dims=[["pressure_level"], ["pressure_level"]],
        output_core_dims=[["h"]],
        vectorize=True,
        dask="parallelized",
        kwargs={"alturas": alturas_desejadas},
        output_dtypes=[pressao_valores.dtype],
    )

    # Adicionamos a nova variável de pressão ao dataset interpolado
    ds_interp["pressure_level"] = da_pressao_interp

    # -----------------------------
    # ETAPA 7: Adicionar coordenada de altura
    # -----------------------------
    # Aqui indicamos que a nova dimensão 'h' representa altura em metros,
    # e associamos os valores exatos usados na interpolação
    ds_interp = ds_interp.assign_coords(altura=("h", alturas_desejadas))

    # -----------------------------
    # ETAPA 8: Reorganizar as dimensões
    # -----------------------------
    # Por fim, reorganizamos as dimensões do dataset para que fiquem
    # na ordem esperada: primeiro o tempo, depois a altura.
    ds_interp = ds_interp.transpose("valid_time", "h")


    import matplotlib.pyplot as plt

    # Pegue uma amostra de tempo
    h_exemplo = h.isel(valid_time=1000).values
    t_exemplo = ds["t"].isel(valid_time=1000).values
    alturas_exemplo = alturas_desejadas
    t_interp = interp_1d(h_exemplo, t_exemplo, alturas_exemplo)

    plt.plot(h_exemplo, t_exemplo, label="Original")
    #plt.plot(alturas_exemplo, t_interp, "o--", label="Interpolado")
    plt.xlabel("Altura (m)")
    plt.ylabel("Temperatura (K)")
    plt.legend()
    plt.title("Interpolação para altura constante (exemplo)")
    plt.grid(True)
    plt.show()

    return ds_interp
