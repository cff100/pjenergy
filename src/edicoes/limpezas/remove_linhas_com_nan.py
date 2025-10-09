import dask.dataframe as dd

def remove_linhas_nan_dataframes(df: dd.DataFrame) -> dd.DataFrame:

    df = df.dropna()
    return df