
![alt text](/tutorials/images/Pasted%20image%2020250308162026.png)

# Pjenergy

Pjenergy é um projeto que visa a obtenção e estudo do potencial energético do vento na região da Bacia de Campos, especificamente na área em que se localiza um conjunto de plataformas de pretóleo e gás em descomissionamento, com a ideia em mente de contribuir com informações relevantes para a possível contrução de aerogeradores offshore. 

Os dados utilizados foram obtidos do Climate Data Store (CDS), um agrupamento de dados climáticos do Programa da União Europeia. O dataset específico é o [ERA5 hourly data on pressure levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=overview). Os dados obtidos cobrem 250 combinações de 5 variáveis ("u_component_of_wind", "v_component_of_wind", "relative_humidity", "temperature", "geopotential"), 5 níveis de pressão (900hPa, 925hPa, 950hPa, 975hPa, 1000hPa) e 10 anos (2015-2024), em todas essas combinações capturando o conjunto de todos os dias, meses e horários inteiros.


## Pré-requisitos

- Intalar [Anaconda](https://anaconda.org/anaconda/anaconda-navigator): O Anaconda vem com o Conda, um gerenciador de pacotes e ambientes que facilita a instalação de pacotes, criação de ambientes isolados (evitando assim conflitos de dependência) e, principalmente, permitindo um fluido compartilhamento de configuração de ambientes, o que é necessário em um trabalho em equipe.

- [Git](https://git-scm.com/downloads): Necessário para o uso e contribuição ao código.

- Ter uma conta registrada no [Climate Data Store](https://cds.climate.copernicus.eu/): É o local de retirada dos datasets utilizados. 
Essa etapa é opcional, já que os datasets necessários já estão no repositório.


## Primeiros Passos

### 1 - Clonar repositório

 - Estando no diretório em que deseja clonar o projeto, digite no terminal:

```bash
git clone https://github.com/cff100/pjenergy.git
```

### 2 - Intalar o projeto localmente

Isso torna o projeto utilizável como um pacote (essencial para importações) e instala dependências, criando um ambiente virtual com configurações compartilhadas.

Crie o ambiente virtual com:

```bash
conda env create -f environment.yml
```
E o ative:

```bash
conda activate pjenergy
```

Os pacotes instalados estão organizados no [arquivo de ambiente](environment.yml). 

**Quando necessário:** Quando você ou outra pessoa trabalhando no projeto fizer alterações nesse arquivo é necessário uma atualização caso se queira estar em dia com as mudanças. Para isso, use:

```bash
conda env update -f environment.yml
```

### 3 - Salvar o token pessoal para obtenção dos dados (opcional, para se obter os datasets da API do Climate Data Store)

Esse passo serve para manter a generalidade do código, de forma que não ocorra que a conta de apenas uma pessoa seja usada para obtenção dos datasets.

Tendo registrado uma conta no CDS, basta ir à página de [CDSAPI setup](https://cds.climate.copernicus.eu/how-to-api) e copiar o código com *url* e *key*.

Agora crie um arquivo no seu **diretório de usuário** e dê o nome de .cdsapi (por exemplo, com o comando abaixo) e copia url e key para lá.

```bash
notepad $env:USERPROFILE\.cdsapirc
```

**OBS.:** Conforme o funcionamento esperado, o arquivo .cdsapirc não subirá para o Github.


## Obtenção dos Dados

Como esse é um processo extremamente custoso em horas computacionais, os datasets foram obtidos pela API do CDS e armazenados na pasta de [dados NetCDF](data/datasets/originais) do repositório. Ainda assim, a estrutura para obtenção desses dados está no repositório para uso eventual. Esses datasets foram obtidos utilizando o conjunto de parâmetros representados na classe de [Parâmetros de obtenção de dados](src/config/constants.py). 

O processo leva dezenas de horas, porém a estrutura do código foi feita utilizando um padrão de nome para os arquivos baixados para permitir que a obtenção possa ser interrompida e recomeçada quantas vezes necessário sem que se tenha que retomar a obtenção desde o início. A função principal para a obtenção está [aqui](src/main/obtem_datasets_originais.py). 

Utilizando a mesma função, também pode se obter apenas um dataset com uma combinação de variável, ano e nível de pressão à escolha do usuário.
Pode-se testar esse tipo de uso com este [arquivo de teste](tests/tests_geracoes/test_requisicao_dados_nc.py). Basta usar:

```bash
pytest -s .\tests\tests_geracoes\test_requisicao_dados_nc.py
```

## Montagem dos dados (EM MANUTENÇÃO...)

Essa etapas envolve um conjunto de subetapas, desde a edição de datasets para unir os obtidos e processá-los para representar as localizações das plataformas até a geração de dataframes a partir dos datasets.

A função principal para esta etapa está [aqui](src/main/montagem_dados.py).

### Pastas de dados utilizadas nesse processo

**OBS.:** Essas pastas dsó são criadas após a execução do código.

- [Dataset unido](data/datasets/unido): Onde fica o dataset formado pela união dos datasets obtidos do CDS.
- [Datasets de coordenadas específicas](data/datasets/coordenadas_especificas)
    - [Datasets de plataformas](data/datasets/coordenadas_especificas/plataformas): Onde ficam os datasets específicos para as coordenadas de cada plataforma estudada.
    - [Datasets de ponto não plataforma](data/datasets/coordenadas_especificas/ponto_nao_plataforma): Onde fica o dataset para alguma coordenada diferente que tenha se desejado criar.

- [Dataframes de coordenadas específicas](data/dataframes/coordenadas_especificas)
    - [Dataframes de plataformas](data/dataframes/coordenadas_especificas/plataformas/): Onde ficam os dask dataframes específicos para as coordenadas de cada plataforma estudada.
    - [Dataframes de ponto não plataforma](data/dataframes/coordenadas_especificas/ponto_nao_plataforma/): Onde fica o dask dataframe para alguma coordenada diferente que tenha se desejado criar.






### Geração do Dataframe

A partir do dataset unificado, esta [função](src/main/gera_dataframe.py) cria um dask dataframe. Utilizar um dask dataframe é importante nesse caso pois ele permite o particionamente de um único dataframe em vários arquivos distintos, o que é essencial para trabalhar com dados nessa escala de tamanho, já que as memórias RAM comuns não possuem espaço suficiente para processar todo o dataframe ao mesmo tempo.

De forma complementar, foi escolhido [Parquet](https://parquet.apache.org/) como formato de armazenamento das partições do dataframe, devido a sua alta compressão e eficiência de armazenamento, eficiência de leitura (por ser orientado à colunas) e o armazenamento dos metadados da estrutura (o que preserva informações sobre os dados e assim melhora muito a eficiência de processos). 

Esse formato tem a desvantagem de não ser legível por humanos, porém isso pode ser contornado através da conversão parcial do dataframe para o formato CSV.

Esse dataframe com suas partições são guardados nesta [pasta](data/dataframes/dataframe_primario) (Essa pasta só será gerada localmente).


## Geração de um Dataframe com Colunas Temporais Adicionais (EM ANDAMENTO...)

O dataframe criado no passo anterior já possui a coluna **valid_time** do tipo datetime, mas para facilitar a manipulação e representação posterior (em gráficos, por exemplo), busca-se separar ano, mês, dia e hora como colunas à parte.