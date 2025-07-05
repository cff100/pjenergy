from pathlib import Path
from datasets_operations.ler_nc import ler_dataset_nc
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO
from config.constants import NomeColunasDataframe as ndc
from config.constants import ConstantesNumericas as cn

def dataset_remocoes(dataset):
    "Remove coordenadas e variáveis indesejadas"

    lista_remover = ['number', 'expver']
    ds = dataset.drop(lista_remover)

    return ds

def dataset_criacoes(dataset):
    "Criar variáveis no dataset"

    # Variável de altura
    dataset["h"] = dataset["z"] / cn.g

    return dataset
    
    

def dataset_renomeacoes(dataset):
    "Renomeia coordenadas/variáveis"

    dicionario_renomear = ndc.novos_nomes
    ds = dataset.rename(dicionario_renomear)

    return ds


def edita_dataset_unico(caminho_relativo: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO):

    # Lê dataset
    ds = ler_dataset_nc(caminho_relativo)

    processos = [dataset_remocoes, dataset_criacoes]

    for funcao in processos:
        ds = funcao(ds)

    return ds


if __name__ == "__main__":
    ds = edita_dataset_unico()
    print(ds)




