
![alt text](/tutorials/images/Pasted%20image%2020250308162026.png)

# Pjenergy

**Pjenergy** é um projeto que visa estimar e estudar o potencial energético do vento na região da Bacia de Campos, com foco em uma área onde se localizam plataformas de petróleo e gás em processo de descomissionamento. A ideia central é contribuir com informações relevantes para uma possível instalação de aerogeradores offshore.

Os dados utilizados são provenientes do [Climate Data Store (CDS)](https://cds.climate.copernicus.eu/), um repositório europeu de dados climáticos. O dataset específico é o:

> [ERA5 hourly data on pressure levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=overview)

Foram consideradas as 250 combinações de:
- **5 variáveis:** `u_component_of_wind`, `v_component_of_wind`, `relative_humidity`, `temperature`, `geopotential`
- **5 níveis de pressão:** 900 hPa, 925 hPa, 950 hPa, 975 hPa, 1000 hPa
- **10 anos:** 2015 a 2024  
Todas as combinações cobrem todos os dias do ano, com dados para cada hora cheia.


---


## Pré-requisitos

- [Anaconda](https://anaconda.org/anaconda/anaconda-navigator): Inclui o Conda, um gerenciador de pacotes e ambientes que facilita a instalação de pacotes, criação de ambientes isolados (evitando assim conflitos de dependência) e, principalmente, permitindo um fluido compartilhamento de configuração de ambiente entre os membros da equipe.

- [Git](https://git-scm.com/downloads): Para o uso e contribuição ao código.

- Conta no [Climate Data Store](https://cds.climate.copernicus.eu/): Local de retirada dos datasets utilizados. Esse passo é opcional, já que os datasets necessários já estão no repositório.


---


## Primeiros Passos

### 1 - Clonar repositório

 - Estando no diretório em que deseja clonar o projeto, digite no terminal:

```bash
git clone https://github.com/cff100/pjenergy.git
```

### 2 - Instalar o projeto localmente

Isso torna o projeto utilizável como um pacote (essencial para importações) e garante a instalação de dependências em um ambiente virtual com configurações padronizadas.

Crie o ambiente virtual com:

```bash
conda env create -f environment.yml
```
E o ative:

```bash
conda activate pjenergy
```

Os pacotes instalados estão organizados no [arquivo de ambiente](environment.yml). 

**Quando necessário:** Quando você ou outra pessoa trabalhando no projeto fizer alterações neste arquivo, é necessário uma atualização caso se queira estar em dia com as mudanças. Para isso, use:

```bash
conda env update -f environment.yml
```

### 3 - (Opcional) Salvar o token pessoal para obtenção dos dados da API do Climate Data Store

Esse passo serve para manter a generalidade do código, de forma que não ocorra que a conta de apenas uma pessoa seja usada para obtenção dos datasets.

Tendo registrado uma conta no CDS, basta ir à página de [CDSAPI setup](https://cds.climate.copernicus.eu/how-to-api) e copiar o código com *url* e *key*.

Agora crie um arquivo no seu **diretório de usuário** e dê o nome de .cdsapi (por exemplo, com o comando abaixo) e copie url e key para lá.

```bash
notepad $env:USERPROFILE\.cdsapirc
```

**OBS.:** Conforme o funcionamento esperado, o arquivo .cdsapirc não subirá para o Github.


---


## Obtenção dos Dados

Como esse é um processo extremamente custoso em horas computacionais, os datasets foram obtidos pela API do CDS e armazenados na pasta de [dados NetCDF](data/datasets/originais) do repositório. Ainda assim, a estrutura para obtenção desses dados está no repositório para uso eventual. Os parâmetros utilizados estão definidos na classe `ParametrosObtencaoDados`([neste arquivo](src/config/constants.py)), que centraliza e organiza as combinações necessárias para a obtenção dos dados.



O processo leva dezenas de horas, porém a estrutura do código foi feita utilizando um padrão de nome para os arquivos baixados para permitir que a obtenção possa ser interrompida e recomeçada quantas vezes necessário sem que se tenha que retomar a obtenção desde o início. A função principal para a obtenção está [aqui](src/main/obtem_datasets_originais.py). 

Utilizando a mesma função, também pode se obter apenas um dataset com uma combinação de variável, ano e nível de pressão à escolha do usuário.
Pode-se testar esse tipo de uso com [este arquivo de teste](tests/tests_geracoes/test_requisicao_dados_nc.py). Basta usar:

```bash
pytest -s .\tests\tests_geracoes\test_requisicao_dados_nc.py
```


---


## Montagem dos dados (EM DESENVOLVIMENTO...)

Essa etapa envolve várias subetapas, incluindo a união dos datasets obtidos, edição e mapeamento para as coordenadas das plataformas e a geração de dataframes correspondentes.

A função principal para esta etapa está [aqui](src/main/montagem_dados.py).

### Estrutura Esperada de Pastas (geradas dinamicamente)


- [Dataset unido](data/datasets/unido): Onde fica o dataset formado pela união dos datasets obtidos do CDS.
- [Datasets de coordenadas específicas](data/datasets/coordenadas_especificas)
    - [Datasets de plataformas](data/datasets/coordenadas_especificas/plataformas): Onde ficam os datasets específicos para as coordenadas de cada plataforma estudada.
    - [Datasets de ponto não plataforma](data/datasets/coordenadas_especificas/ponto_nao_plataforma): Onde fica o dataset para alguma coordenada diferente que tenha se desejado criar.

- [Dataframes de coordenadas específicas](data/dataframes/coordenadas_especificas)
    - [Dataframes de plataformas](data/dataframes/coordenadas_especificas/plataformas/): Onde ficam os dask dataframes específicos para as coordenadas de cada plataforma estudada.
    - [Dataframes de ponto não plataforma](data/dataframes/coordenadas_especificas/ponto_nao_plataforma/): Onde fica o dask dataframe para alguma coordenada diferente que tenha se desejado criar.


---

## Decisões de Projeto

Algumas decisões técnicas foram tomadas visando equilíbrio entre desempenho, legibilidade e escalabilidade. Aqui estão algumas das principais escolhas:

### Por que Dask?
O volume de dados envolvido no projeto (dados horários, 10 anos, 250 combinações de variáveis) é grande o suficiente para tornar o uso de `pandas` ineficiente ou até inviável em máquinas comuns. O `Dask` permite a **manipulação de dados maiores que a memória RAM disponível**, por dividi-los em múltiplas partes.

### Por que Parquet?
O formato `Parquet` foi escolhido por:
- Ser um formato **colunar e comprimido**, eficiente para leitura seletiva.
- Ser altamente compatível com `Dask`, otimizando tempo de leitura/escrita.
- Reduzir significativamente o uso de armazenamento em comparação com CSV, apesar da desvantagem de não ser diretamente legível por humanos.
    - No entanto, essa limitação pode ser facilmente contornada, seja utilizando ferramentas de visualização de arquivos Parquet, seja convertendo os dados, parcial ou totalmente, para outros formatos como CSV, sempre que necessário.

