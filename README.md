# Pjenergy

Pjenergy é um projeto que visa a obtenção e estudo do potencial energético do vento na região da Bacia de Campos, especificamente na área em que se localiza um conjunto de plataformas de pretóleo e gás em descomissionamento, com a ideia em mente de contribuir com informações relevantes para a possível contrução de aerogeradores offshore. 

Para o fim de maior aprofundamento, o projeto foca na localização de uma plataforma em específico.

## Obtenção dos dados

Os dados utilizados foram obtidos do Climate Data Store, um agrupamento de dados climaticos do Programa da União Europeia.

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

