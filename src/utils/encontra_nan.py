
# import xarray as xr
import dask.dataframe as dd 
# from pathlib import Path

# from leituras.ler_datasets import ler_dataset_nc

def linhas_dataframes_com_nan(df: dd.DataFrame) -> tuple[dd.DataFrame, dd.DataFrame]:
    """Filtra para mostrar as linhas com algum valor NaN"""

    df_nan = df[df.isna().any(axis=1)]
    n_valores = df.isna().sum()
    return df_nan, n_valores

# def elementos_dataset_com_nan(caminho: Path) -> xr.Dataset:

#     ds = ler_dataset_nc(caminho)
#     print(ds)
#     mask = ds.to_array().isnull().any(dim=('variable', 'latitude', 'longitude'))
#     ds_com_faltantes = ds.sel(valid_time=mask)

#     return ds_com_faltantes


if __name__ == "__main__":
    from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
    
    df = ler_dataframes_pontuais_plataformas_geral("p2")
    df_nan, n_valores = linhas_dataframes_com_nan(df)
    print(n_valores.compute())
    print(df_nan.compute().sample(15))


    # from config.paths import DiretoriosBasicos as db

    # ds_nan = elementos_dataset_com_nan(db.DIRETORIO_DADOS / "datasets/originais/(var-geopotential)_(ano-2015)_(pressao-900).nc")
    # print(ds_nan)