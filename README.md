

## 1) 
Depois de clonar o repositório, para instalar o projeto localmente, ou seja, torná-lo utilizável como um pacote no seu ambiente, e instalar dependências: 

No diretório mestre de todo o projeto, digite:

**pip install -r requirements.txt**

Ele serve para permitir a importação de funções, constantes, etc de outras pastas do projeto.

## 2)
Para adicionar a chave da API do CDS:

Abra ou crie o arquivo

**notepad $env:USERPROFILE\.cdsapirc**

E copie para lá o token pessoal fornecido na página https://cds.climate.copernicus.eu/how-to-api (Necessário ter uma conta)

