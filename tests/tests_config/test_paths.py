import os
import pytest
from config.paths import PathsDados
from config.constants import FormatosArquivo as fa

@pytest.mark.parametrize(
    "formato_arquivo, plataforma, esperado_parte",
    [
        (fa.NETCDF, "NAMORADO 2 (PNA-2)", "datasets/coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2).nc"),
        (fa.PARQUET, "p2", "dataframes/coordenadas_especificas/plataformas/p2-PETROBRAS_26_(P-26)"),
        (fa.NETCDF, None, "datasets/coordenadas_especificas/ponto_nao_plataforma/ponto_nao_plataforma.nc"),
        (fa.PARQUET, None, "dataframes/coordenadas_especificas/ponto_nao_plataforma/ponto_nao_plataforma"),
    ]
)
def test_obtem_path_coord_especifica(formato_arquivo, plataforma, esperado_parte):
    path = PathsDados.obtem_path_coord_especifica(formato_arquivo, plataforma)
    esperado_norm = os.path.normpath(esperado_parte)
    assert str(path).endswith(esperado_norm)

def test_obtem_path_coord_especifica_plataforma_invalida():
    with pytest.raises(ValueError):
        PathsDados.obtem_path_coord_especifica(fa.NETCDF, "PLATAFORMA_INVALIDA")