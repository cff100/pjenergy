
Descrição dos objetivos e funcionamentos por trás dos códigos. Antes de tudo explicado aqui, é necessário seguir os Primeiros Passos do [README](../README.md)

# Obtenção dos dados originais

O primeiro objetivo que se visa atingir é obter os dados meteorológicos que servirão de base para todas as análises, criação de tabelas, gráficos, etc. O arquivo principal que gerencia esse objetivo é [este](../src/main/obtem_datasets_originais.py). Com ele há duas opções de obtenção de dados, uma em que se busca a obtenção de múltiplas combinações de parâmetros e outra em que se busca apenas uma combinação. 

Os parâmetros considerados nas combinações são 3: variáveis (velocidade do vento na direção u, velocidade do vento na direção v, temperatura, geopotencial, umidade relativa, etc), anos e níveis de pressão. No caso de se desejar buscar apenas um combinação de parâmetros, deve-se usar a [função principal](../src/main/obtem_datasets_originais.py#L5) com `usa_multiplos_dados = False` e passar os valores específicos de `variavel`, `ano` e `pressao_nivel`, além do `dataset_salvamento_caminho` (o local onde será salvo o arquivo obtido).



