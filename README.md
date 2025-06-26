

## 1) 
Depois de clonar o repositório, para instalar o projeto localmente, ou seja, torná-lo utilizável como um pacote no seu ambiente, e instalar dependências: 

Usando o conda, no diretório mestre do projeto, digite:
(caso você não tenha o conda, é necessário instalá-lo)

**conda env create -f environment.yml** 

**conda activate pjenergy**

Isso também serve para permitir a criação do ambiente virtual, mais pacotes necessários para o projeto.

OBS.: Use **conda env update -f environment.yml** quando adicionar novos pacotes ao environment.yml

## 2)
Para adicionar a chave da API do CDS:

Abra ou crie o arquivo por meio de:

**notepad $env:USERPROFILE\.cdsapirc**

E copie para lá o token pessoal fornecido na página https://cds.climate.copernicus.eu/how-to-api (Basta clicar no ícone de copiar). OBS.:Necessário ter uma conta

Esse arquivo não está guardado remotamente, e deve ficar no seu diretório de usuário. Ex.: C:\Users\nome_do_usuario\.cdsapi

