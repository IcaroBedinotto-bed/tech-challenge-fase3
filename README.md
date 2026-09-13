Predição da Taxa de Alfabetização Municipal

Sobre o projeto

Este projeto foi desenvolvido como parte do Tech Challenge e aplica
Engenharia de Dados, Análise Exploratória e Machine Learning para apoiar
a análise da alfabetização nos municípios brasileiros.

A proposta original considera a previsão de resultados de alfabetização
em nível de estudante. Como os dados disponíveis para este projeto são
predominantemente municipais, a abordagem foi adaptada para prever a
taxa de alfabetização municipal de 2024.

O objetivo de negócio é identificar municípios que apresentam maior
risco de não atingir a meta de alfabetização.

Objetivo analítico

Prever:

taxa_alfabetizacao_2024

utilizando informações disponíveis anteriormente ao período de previsão
e, posteriormente, comparar a previsão com:

meta_alfabetizacao_2024

A solução permite classificar municípios como previstos para atingir ou
não atingir a meta.

Perguntas de negócio

Quais características estão mais associadas à taxa de alfabetização?

Quais municípios apresentam maior risco de não atingir a meta?

Qual a capacidade do modelo de identificar municípios que não
atingem a meta?

Quais variáveis mais influenciam as previsões?

Como explicar uma previsão individual?

Dados

O projeto organiza os dados em camadas:

data/
├── silver/
├── gold/
├── dados_escolas/
├── analytical/
└── dados_populacao/

A camada Gold utiliza uma arquitetura dimensional com fatos e dimensões
de alfabetização.

Principais arquivos:

data/gold/facts/
├── fato_alfabetizacao_municipio.parquet
├── fato_alfabetizacao_uf.parquet
└── fato_alfabetizacao_brasil.parquet

data/gold/dimensions/
├── municipio.parquet
├── rede.parquet
├── tempo.parquet
└── uf.parquet

A base utilizada na modelagem é:

data/analytical/base_analitica_modelo.parquet

A base_analitica_modelo incorpora informações contextuais do Censo 2022.

Variáveis

Numéricas

taxa_alfabetizacao_2023

percentual_participacao_2023

meta_alfabetizacao_2024

domicilios_2022

taxa_alfabetizacao_censo_2022

indice_envelhecimento_2022

idade_mediana_2022

razao_sexo_2022

Categóricas

UF

Capital

Target

taxa_alfabetizacao_2024

Pré-processamento

O pré-processamento é integrado ao modelo por meio de Pipeline e
ColumnTransformer.

Para variáveis numéricas:

imputação de valores ausentes pela mediana;

padronização com StandardScaler.

Para variáveis categóricas:

imputação pela categoria mais frequente;

One-Hot Encoding;

handle_unknown="ignore".

O pré-processamento é ajustado dentro do fluxo de treinamento, evitando
o uso de informações do conjunto de teste no ajuste das transformações.

Separação dos dados

Os dados são divididos em:

80% para treinamento;

20% para teste;

random_state=42.

Modelo

O modelo principal utilizado foi a Regressão Linear, escolhida pela
combinação de desempenho, simplicidade e interpretabilidade. Além de ter tido a melhor performance em comparação ao Randon Forest.

O modelo é implementado em uma Pipeline que integra o pré-processamento
e o treinamento.

Resultados

No conjunto de teste:

Métrica          Resultado

MAE          8,48 p.p.
RMSE        11,19 p.p.
R²                0,65

O MAE indica um erro absoluto médio de aproximadamente 8,5 pontos
percentuais.

O R² de 0,65 indica capacidade relevante de explicar a variação
observada da taxa de alfabetização de 2024 no conjunto de teste.


Análise de erros

A análise de erros foi realizada a partir de:

data/analytical/evaluation/erros_linear.parquet

Foram analisados erros absolutos, maiores erros, subestimações,
superestimações, resíduos e a relação entre valores reais e previstos.

O gráfico de valores reais versus previstos mostra uma relação
consistente entre as duas medidas, mas também evidencia dificuldade nos
extremos.

Municípios com taxas reais muito baixas tendem a ter suas taxas
superestimadas, enquanto municípios com taxas muito altas tendem a ter
suas taxas subestimadas. Esse comportamento é consistente com regressão
à média.

Atingimento da meta

A previsão é convertida em uma decisão de negócio:

taxa_prevista_2024 >= meta_alfabetizacao_2024

Matriz observada no conjunto de teste:

Real  Previsto     Não atingiu   Atingiu

Não atingiu            293       182
Atingiu                    114   458

Considerando "não atingir a meta" como situação de risco:

293 de 475 municípios que realmente não atingiram foram
identificados;

recall de aproximadamente 61,7%;

entre os 407 municípios classificados como em risco, 293 realmente
não atingiram;

precisão de aproximadamente 72,0%.

Isso indica potencial para utilizar o modelo como ferramenta de
sinalização e priorização.

Feature Importance

Foi utilizada Permutation Importance.

Variável                            Importância

UF                                   4,95
taxa_alfabetizacao_2023              4,56
idade_mediana_2022                   0,56
percentual_participacao_2023         0,50
domicilios_2022                          0,04
taxa_alfabetizacao_censo_2022            0,02
Capital                                -0,006
meta_alfabetizacao_2024                -0,006

A UF e a taxa de alfabetização de 2023 são as principais fontes de
informação para a previsão.

A idade mediana e a participação apresentam contribuições adicionais
menores.

SHAP

O SHAP foi utilizado para interpretar o modelo global e localmente.

O SHAP Summary Plot mostrou maior contribuição de:

taxa_alfabetizacao_2023;

variáveis relacionadas à UF;

idade_mediana_2022;

percentual_participacao_2023.

O SHAP Waterfall Plot permite explicar uma previsão municipal
individual, mostrando quais atributos contribuíram para aumentar ou
reduzir a previsão.

As relações observadas por Feature Importance e SHAP são interpretadas
como associações preditivas, não como causalidade.

Principais insights

Histórico recente é o principal sinal

A taxa de alfabetização de 2023 é a principal fonte de informação para
prever a taxa de 2024.

Existe heterogeneidade territorial

A UF apresenta elevada importância preditiva, indicando diferenças
relevantes no comportamento da alfabetização entre estados.

Variáveis contextuais têm contribuições diferentes

Entre as variáveis do Censo 2022, a idade mediana apresentou
contribuição mais relevante. Outras variáveis tiveram impacto pequeno.

A meta é mais importante para a decisão do que para a previsão

A meta de 2024 apresentou importância praticamente nula para prever a
taxa, mas é fundamental para transformar a previsão em classificação de
risco.

O modelo tem dificuldade nos extremos

A regressão tende a aproximar previsões da média, superestimando valores
muito baixos e subestimando valores muito altos.

O modelo pode apoiar priorização

A identificação de aproximadamente 62% dos municípios que não atingiram
a meta, com precisão de aproximadamente 72% entre os municípios
sinalizados como risco, demonstra potencial para apoiar priorização de
análises.

Limitações

Nível de agregação

A formulação original do desafio é voltada ao nível de estudante,
enquanto os dados utilizados neste projeto são predominantemente
municipais. Portanto, a solução foi adaptada para previsão da taxa
municipal.

Dados futuros

A ausência de taxas observadas posteriores a 2024 limita a validação
temporal para anos futuros.

Causalidade

Feature Importance e SHAP mostram contribuição para o comportamento
preditivo do modelo e não evidenciam relações causais.

Estrutura

project/
├── data/
│   ├── silver/
│   ├── gold/
│   ├── analytical/
│   ├── dados_escolas/
│   └── dados_populacao/
├── notebooks/
├── src/
│   ├── preprocessing/
│   │   ├── build_base_analitica.py
│   │   ├── feature_engineering.py
│   │   └── preprocessing_pipeline.py
│   ├── modeling/
│   │   └── models.py
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── error_analysis.py
│   │   ├── cross_validation.py
│   │   ├── feature_importance.py
│   │   └── shap_analysis.py
│   └── visualization/
│       └── shap_plots.py
├── tests/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

Como executar

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

Tecnologias

Python

Pandas

NumPy

Scikit-learn

SHAP

Matplotlib

PyArrow / Parquet

Jupyter Notebook

Próximos passos

incorporar dados posteriores para validação temporal;

testar novos atributos educacionais e contextuais;

investigar estratégias de validação mais robustas para a
heterogeneidade territorial;

avaliar modelos adicionais;

calibrar o mecanismo de classificação de risco;

desenvolver um painel de acompanhamento municipal;

incorporar explicações SHAP à interface;

avaliar o modelo com dados futuros efetivamente observados.

Conclusão

O projeto integra dados, tratamento, engenharia de atributos, modelagem,
avaliação e interpretabilidade em uma solução voltada a um problema
educacional real.

O modelo não deve ser utilizado como substituto de análises educacionais
ou decisões de política pública. Seu principal potencial está em
funcionar como instrumento complementar de sinalização de risco e
priorização, indicando municípios que merecem investigação mais
aprofundada.