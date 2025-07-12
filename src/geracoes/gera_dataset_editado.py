from typing import Optional
import xarray as xr
from config.constants import Plataformas, Correspondencias as cr



def monta_dataset_ponto_especifico(plataforma: str | None = None, 
                                  latitude_longitude_alvo: tuple[float, float] | None = None, 
                                  caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> xr.Dataset:
    "Faz edições no dataset único para criar um dataset para um ponto específico"

    if not plataforma and not latitude_longitude_alvo:
        raise ValueError("É necessário informar a latitude e longitude alvo ou a plataforma.")
    
    elif plataforma:
            
        plataforma = gerencia_plataforma_nome(plataforma)

        plataforma_dados = Plataformas.PLATAFORMAS_DADOS[plataforma]["coords"]

        if not latitude_longitude_alvo: # Caso seja escolhida uma plataforma específica e as coordenadas não seja dadas, é obtido os valores das coordenadas dela.
            latitude_longitude_alvo = plataforma_dados #[plataforma]["coords"]
        elif latitude_longitude_alvo:
            # Confere se as coordenadas dadas correspondem à plataforma escolhida
            if latitude_longitude_alvo != oc.plataformas_dados[plataforma]["coords"]:
                latitude_longitude_alvo = oc.plataformas_dados[plataforma]["coords"]
                print(f"Sobreescrevendo as coordenadas fornecidas para as coordenadas reais da plataforma fornecida: {latitude_longitude_alvo}\n")
            else:
                pass
    # Lê dataset (verificando se o dataset existe)
    ds = ler_dataset_nc_relativo(caminho_relativo_dataset_unico)

    processos = [dataset_remocoes, dataset_interpola_lat_lon, interp_alturas_constantes, dataset_criacoes, dataset_renomeacoes]

    for funcao in processos:
        if funcao == dataset_interpola_lat_lon:
            ds = funcao(ds, latitude_longitude_alvo)
        else:
            ds = funcao(ds)

    salva_dataset_nc(ds, decide_caminho_absoluto_dataset_localizacao_especifica(plataforma))

    return ds



def gera_datasets_pontuais(usa_plataformas: bool = True, 
                                           latitude_longitude_alvo: Optional[tuple[float, float]] = None) -> None | xr.Dataset :
    """Gera um dataset editado em relação ao dataset unido.
    
    Parâmetros:
    - usa_plataformas: Se True, gera datasets para todas plataformas. Se False, gera um dataset para as coordenadas fornecidas."""
    
    if usa_plataformas:
        for plat in list(Plataformas.PLATAFORMAS_DADOS.keys()):
            if latitude_longitude_alvo != None:
                print("\nAs plataformas já possuem coordenadas registradas, não é necessário passar valores de latitude e longitude.\n")
            print(f"Plataforma: {plat}")
            ds = monta_dataset_ponto_especifico(plataforma = plat)  # Retorna o valor da última plataforma
    else:
        ds = monta_dataset_ponto_especifico(latitude_longitude_alvo = latitude_longitude_alvo)
    return ds 