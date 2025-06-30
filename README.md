# Pjenergy

Pjenergy é um projeto que visa a obtenção e estudo do potencial energético do vento na região da Bacia de Campos, especificamente na área em que se localiza um conjunto de plataformas de pretóleo e gás em descomissionamento, com a ideia em mente de contribuir com informações relevantes para a possível contrução de aerogeradores offshore. 

Para o fim de maior aprofundamento, o projeto foca na localização de uma plataforma em específico.

Os dados utilizados foram obtidos do Climate Data Store (CDS), um agrupamento de dados climáticos do Programa da União Europeia. Os dados cobrem 250 combinações de 5 variáveis ("u_component_of_wind", "v_component_of_wind", "relative_humidity", "temperature", "geopotential"), 5 níveis de pressão (900hPa, 925hPa, 950hPa, 975hPa, 1000hPa) e 10 anos (2015-2024), em todas essas conbinações capturando o conjunto de todos os dias, meses e horários inteiros.

## Pré-requisitos

- Intalar [Anaconda](https://anaconda.org/anaconda/anaconda-navigator): O Anaconda vem com o Conda, um gerenciador de pacotes e ambientes que facilita a instalação de pacotes, criação de ambientes isolados (evitando assim conflitos de dependência) e, principalmente, permitindo um fluido compartilhamento de ambientes, o que é necessário em um trabalho em equipe.

- [Git](https://git-scm.com/downloads): Necessário para o uso e contribuição ao código.

## Primeiros Passos

### 1

Clonar repositório. No diretório em que deseja clonar o projeto digite 
´´´bash
git clone https://github.com/cff100/pjenergy.git
´´´

## Obtenção dos Dados

Como esse é um processo extremamente custoso em horas computacionais, os dados foram obtidos pela API do CDS e armazenados em na pasta de [dados .nc](data/nc_files/) do repositório. Ainda assim, estrutura para obtenção desses dados está no repositório para uso eventual. O processo leva dezenas de horas, porém a estrutura do código foi feita utilizando um padrão de nome para os arquivos baixados para permitir que a obtenção possa ser interrompida e recomeçada quantas vezes necessário sem que seja necessário retomar a obtenção desde o início. A função principal para isso está [aqui](src/main/obtem_arquivos_nc_padrao.py). 

Também há uma estrutura para obter dados com diferentes parâmetros. Nesse caso, pode-se inclusive ajustar para se obter uma quantidade bem menor de dados, como um teste, por exemplo. Função principal para essa funcionalidade [aqui](src/main/obtem_arquivos_nc_padrao.py).

## 1) 
Depois de clonar o repositório, para instalar o projeto localmente, ou seja, torná-lo utilizável como um pacote no seu ambiente, e instalar dependências: 

Usando o conda, no diretório mestre do projeto, digite no terminal:
(caso você não tenha o conda, é necessário instalá-lo)

**conda env create -f environment.yml** 

**conda activate pjenergy**

Isso também serve para permitir a criação do ambiente virtual, junto com os pacotes necessários para o projeto.

OBS.: Use **conda env update -f environment.yml** quando adicionar novos pacotes ao environment.yml


## 2)
Para adicionar a sua chave da API do CDS:

Abra ou crie o arquivo por meio do seguinte comando no terminal:

**notepad $env:USERPROFILE\.cdsapirc**

E copie para lá o token pessoal fornecido na página https://cds.climate.copernicus.eu/how-to-api (Basta clicar no ícone de copiar). OBS.: Necessário ter uma conta.

Esse arquivo não está guardado remotamente, e deve ficar no seu diretório de usuário. Ex.: C:/Users/nome_do_usuario/.cdsapi

