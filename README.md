# Pjenergy

Pjenergy é um projeto que visa a obtenção e estudo do potencial energético do vento na região da Bacia de Campos, especificamente na área em que se localiza um conjunto de plataformas de pretóleo e gás em descomissionamento, com a ideia em mente de contribuir com informações relevantes para a possível contrução de aerogeradores offshore. 

Para o fim de maior aprofundamento, o projeto foca na localização de uma plataforma em específico.

Os dados utilizados foram obtidos do Climate Data Store (CDS), um agrupamento de dados climáticos do Programa da União Europeia. Os dados cobrem 250 combinações de 5 variáveis ("u_component_of_wind", "v_component_of_wind", "relative_humidity", "temperature", "geopotential"), 5 níveis de pressão (900hPa, 925hPa, 950hPa, 975hPa, 1000hPa) e 10 anos (2015-2024), em todas essas conbinações capturando o conjunto de todos os dias, meses e horários inteiros.


## Pré-requisitos

- Intalar [Anaconda](https://anaconda.org/anaconda/anaconda-navigator): O Anaconda vem com o Conda, um gerenciador de pacotes e ambientes que facilita a instalação de pacotes, criação de ambientes isolados (evitando assim conflitos de dependência) e, principalmente, permitindo um fluido compartilhamento de ambientes, o que é necessário em um trabalho em equipe.

- [Git](https://git-scm.com/downloads): Necessário para o uso e contribuição ao código.

- Ter uma conta registrada no [Climate Data Store](https://cds.climate.copernicus.eu/): É o local de retirada dos datasets utilizados.


## Primeiros Passos

### 1 - Clonar repositório

 - No diretório em que deseja clonar o projeto digite:

```bash
git clone https://github.com/cff100/pjenergy.git
```

### 2 - Intalar o projeto localmente

Isso permite o projeto utilizável como um pacote (essencial para importações) e instalar dependências, utilizando um ambiente virtual compartilhado.

Crie o ambiente virtual com:

```bash
conda env create -f environment.yml
```
E o ative:

```bash
conda activate pjenergy
```

Os pacotes instalados estão organizados no [arquivo de ambiente](environment.yml). Quando você ou outra pessoa trabalhando no projeto fizer alterações nesse arquivo é necessário uma atualização caso se queira estar em dia com as mudanças. Para isso, use:

```bash
conda env update -f environment.yml
```

### 3 - Salvar o token pessoal para obtenção dos dados

Esse passo serve para manter a generalidade do código, de forma que não ocorra que a conta de apenas uma pessoa seja usada para obtenção dos dados.

Tendo registrado uma conta no CDS, basta ir à página de [CDSAPI setup](https://cds.climate.copernicus.eu/how-to-api) e copiar o código com o url e a key.

Agora crie um arquivo no seu diretório de usuário e dê o nome de .cdsapi (por exemplo, com o comando abaixo) e copia o url e a key para lá.

```bash
notepad $env:USERPROFILE\.cdsapirc
```

OBS.: Conforme o funcionamento esperado, o arquivo .cdsapirc não subirá para o Github.


## Obtenção dos Dados

Como esse é um processo extremamente custoso em horas computacionais, os dados foram obtidos pela API do CDS e armazenados em na pasta de [dados NetCDF](data/nc_files/) do repositório. Ainda assim, estrutura para obtenção desses dados está no repositório para uso eventual. O processo leva dezenas de horas, porém a estrutura do código foi feita utilizando um padrão de nome para os arquivos baixados para permitir que a obtenção possa ser interrompida e recomeçada quantas vezes necessário sem que seja necessário retomar a obtenção desde o início. A função principal para isso está [aqui](src/main/obtem_arquivos_nc_padrao.py). 

Também há uma estrutura para obter dados com diferentes parâmetros. Nesse caso, pode-se inclusive ajustar para se obter uma quantidade bem menor de dados, como um teste, por exemplo. Função principal para essa funcionalidade [aqui](src/main/obtem_arquivos_nc_padrao.py).


## Geração do Dataset Único

Obtidos os 250 datasets na etapa anterior, essa é a parte que os une em um só dataset NetCDF com essa [função principal](src/main/gera_dataset_unico.py). A lógica do código faz uso do padrão dos nomes para unir de forma estruturada.

## Leitura de Arquivos NetCDF

Caso se queira ler o conteúdo de algum dos arquivos NetCDF (seja os baixados, seja o feito da união) pode-se usar esta [função](src/obtaining_and_manipulating_data/nc_files/ler_nc.py) para abrí-los.

