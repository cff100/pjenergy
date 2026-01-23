import dask.dataframe as dd

def remove_linhas_nan_dataframes(df: dd.DataFrame) -> dd.DataFrame:
    """
    Remove linhas com valores NaN do dataframe.
    """

    df = df.dropna()
    return df