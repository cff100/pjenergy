
Descrição extensiva dos objetivos e funcionamentos por trás dos códigos. Antes de tudo explicado aqui, é necessário seguir os **Primeiros Passos** do [README](../README.md)

OBS.: A posição de certas linhas referenciadas no texto a seguir podem estar desatualizadas, mas ao arquivo ao qual pertencem estão corretos.

# Obtenção dos dados originais

O primeiro objetivo que se visa atingir é obter os dados meteorológicos do dataset [ERA5 hourly data on pressure levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=overview) através da API do Climate Data Store (CDS),
que servirão de base para todas as análises, criação de tabelas, gráficos, etc. O arquivo principal que gerencia esse objetivo é [este](../src/main/obtem_datasets_originais.py). Com ele há duas opções de obtenção de dados, uma em que se busca a obtenção de múltiplas combinações de parâmetros e outra em que se busca apenas uma combinação. 

Os parâmetros de dataset considerados nas combinações são 3: variáveis (por exemplo: componente u da direção do vento, componente v da direção do vento, temperatura, geopotencial, umidade relativa, etc), anos e níveis de pressão. No caso de se desejar buscar apenas uma combinação do trio de parâmetros, deve-se usar a [função principal](../src/main/obtem_datasets_originais.py#L5) com `usa_multiplas_combinacoes = False` e passar os valores específicos de `variavel`, `ano` e `pressao_nivel`, além do `dataset_salvamento_caminho` (o local onde será salvo o arquivo obtido).

No caso da obtenção de múltiplas combinações do trio de parâmetros, com `usa_multiplas_combinacoes = True` (default), o código executará a obtenção de combinações do trio de parâmetros com valores padrão do projeto, cada uma salva em um arquivo NetCDF distinto. Os padrão do projeto estão determinados no [arquivo de constantes](../src/config/constants.py), mais especificamente sob a classe [ParametrosObtencaoDados](../src/config/constants.py#L6).

Sob esta mesma classe estão definidos outros parâmetros de dataset de obtenção de dados importantes que são fixos ao longo de todo o projeto, não importando se é buscado várias combinações ou apenas uma de `variavel`, `ano` e `pressao_nivel`. Esses parâmentros fixos são:
- Parâmetros temporais
    - Meses: todos os 12 meses dos anos.
    - Dias: Todos os dias dos meses (31 dias, para abarcar os maiores meses).
    - Horas: Todas horas cheias dos dias (00:00, 01:00, 02:00, ..., 23:00).
- Área: região epecífica trabalhada, dentro da Bacia de Campos.
- Formato dos dados: NetCDF (Network Common Data Format) - Formato de armazenamento de dados científicos orientados a matrizes.
- Formato de download: Não compactados.

Não importando, quais os valores do trio de parâmetros passados para a função principal, ela chama [outra função](../src/geracoes/requisicao_dados_nc.py#L187) que gerencia um conjunto de processos para obtenção e salvamento de dados do dataset do CDS. Essa função separa os processamentos entre os casos do uso de apenas uma combinação e o do uso de múltiplas combinações do trio de parâmetros.

## Apenas uma combinação

No caso de apenas uma combinação, a função de 

