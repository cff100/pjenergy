import dask.dataframe as dd 


# from leituras.ler_datasets import ler_dataset_nc

def linhas_dataframes_com_nan(df: dd.DataFrame) -> tuple[dd.DataFrame, dd.DataFrame]:
    """
    Filtra para mostrar as linhas com algum valor NaN e também calcula quantos elementos NaN há em cada coluna.
    """

    df_nan = df[df.isna().any(axis=1)]
    n_valores = df.isna().sum()
    return df_nan, n_valores




if __name__ == "__main__":
    from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral  
    df = ler_dataframes_pontuais_plataformas_geral("p7")
    df_nan, n_valores = linhas_dataframes_com_nan(df)
    print(n_valores.compute())
    print(df_nan.compute().sample(15))
