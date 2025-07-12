# Módulos internos do projeto
from config.paths import PathsDados as pad
from geracoes.requisicao_dados_nc import requisicao_dados
from config.constants import ParametrosObtencaoDados as pod

def test_requisicao_dados(requisitar = True):
    """Teste para verificar a requisição de dados do Climate Data Store (CDS)"""

    # Escolhe apenas uma variável, um ano e um nível de pressão, para que o teste não demore um tempo impraticável.
    variavel = pod.VARIAVEIS[0]
    ano = pod.ANOS[0]
    pressao_nivel = pod.PRESSAO_NIVEIS[0]

    print(f"\n -> -> -> Variável escolhida: {variavel}")
    print(f" -> -> -> Ano escolhido: {ano}")
    print(f" -> -> -> Nível de pressão escolhido: {pressao_nivel}")

    # Localização do arquivo de saída
    dataset_caminho = pad.DadosTeste.DIRETORIO_DADOS_GERADOS_TESTES / f"teste-(var-{variavel})_(ano-{ano})_(pressao-{pressao_nivel}).nc"
   
    if not requisitar:
        print("\n -> -> -> ATENÇÃO: Requisição de dados não realizada. Mude o parâmetro 'requisitar' para True para realizar a requisição.")
    else:
        requisicao_dados(dataset_caminho, variavel, ano, pressao_nivel, substituir = True)
        