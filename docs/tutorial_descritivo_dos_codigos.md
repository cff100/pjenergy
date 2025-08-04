
Descrição extensiva dos objetivos e funcionamentos por trás dos códigos. Antes de tudo explicado aqui, é necessário seguir os Primeiros Passos do [README](../README.md)

# Obtenção dos dados originais

O primeiro objetivo que se visa atingir é obter os dados meteorológicos que servirão de base para todas as análises, criação de tabelas, gráficos, etc. O arquivo principal que gerencia esse objetivo é [este](../src/main/obtem_datasets_originais.py). Com ele há duas opções de obtenção de dados, uma em que se busca a obtenção de múltiplas combinações de parâmetros e outra em que se busca apenas uma combinação. 

Os parâmetros considerados nas combinações são 3: variáveis (por exemplo: componente u da direção do vento, componente v da direção do vento, temperatura, geopotencial, umidade relativa, etc), anos e níveis de pressão. No caso de se desejar buscar apenas uma combinação de parâmetros, deve-se usar a [função principal](../src/main/obtem_datasets_originais.py#L5) com `usa_multiplos_dados = False` e passar os valores específicos de `variavel`, `ano` e `pressao_nivel`, além do `dataset_salvamento_caminho` (o local onde será salvo o arquivo obtido).

No caso da obtenção de múltiplas combinações de parâmetros, com `usa_multiplos_dados = True` (default), o código executará a obtenção de combinações de parâmetros com valores padrão do projeto. Esses valores estão determinados no [arquivo de constantes](../src/config/constants.py), mais especificamente sob a classe [ParametrosObtencaoDados](../src/config/constants.py#L6).

Sob esta mesma classe estão definidos outros parâmetros de obtenção de dados importantes que são fixos ao longo de todo o projeto, não importando se é buscado várias combinações ou apenas uma de `variavel`, `ano` e `pressao_nivel`. Esses parâmentros fixos são:
- Parâmetros temporais
    - Meses: todos os 12 meses dos anos .
    - Dias: Todos os dias dos meses (31 dias, para abranger os maiores meses).
    - Horas: Todas horas cheias dos dias (00:00, 01:00, 02:00, ..., 23:00).
- Área: região epecífica trabalhada, dentro da Bacia de Campos.
- Formato dos dados: NetCDF (Network Common Data Format) - Formato de armazenamento de dados científicos orientados a matrizes.
- Formato de download: Não compactados.



