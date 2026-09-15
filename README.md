# 📊 Resultados e principais insights

A etapa de modelagem teve como objetivo prever a **taxa de alfabetização municipal de 2024** e utilizar essa previsão para identificar municípios com maior risco de não atingir a meta estabelecida.

O modelo final adotado foi uma **Regressão Linear**, integrada a um pipeline de pré-processamento e avaliada tanto por métricas de regressão quanto pela capacidade de identificar municípios em risco.

---

## 🎯 Desempenho do modelo

No conjunto de teste, composto por 20% dos municípios, o modelo apresentou:

| Métrica | Resultado |
| :--- | ---: |
| **MAE** | **8,48 p.p.** |
| **RMSE** | **11,19 p.p.** |
| **R²** | **0,65** |

O **MAE de 8,48 pontos percentuais** indica que, em média, a previsão do modelo ficou aproximadamente 8,5 p.p. distante da taxa observada.

O **R² de 0,65** indica que o modelo consegue explicar uma parcela relevante da variação observada na taxa de alfabetização de 2024.

> **Importante:** o modelo deve ser interpretado como uma ferramenta de estimativa e priorização, e não como uma previsão exata para cada município.

---

## 🔎 Principais fatores associados às previsões

A análise de **Permutation Feature Importance** identificou as principais variáveis utilizadas pelo modelo:

| Variável | Importância |
| :--- | ---: |
| **UF** | **4,95** |
| **Taxa de alfabetização 2023** | **4,56** |
| **Idade mediana 2022** | **0,56** |
| **Participação na avaliação 2023** | **0,50** |
| Domicílios 2022 | 0,04 |
| Taxa de alfabetização — Censo 2022 | 0,02 |
| Capital | -0,006 |
| Meta de alfabetização 2024 | -0,006 |

Dois fatores se destacam:

### 📈 Histórico recente

A **taxa de alfabetização de 2023** é uma das principais fontes de informação para prever o resultado de 2024.

Municípios que apresentam taxas mais elevadas em 2023 tendem a receber previsões mais elevadas para 2024.

### 🗺️ Dimensão territorial

A variável **UF** apresentou a maior importância individual na Permutation Importance.

Isso indica que existem diferenças relevantes no comportamento da alfabetização entre os estados brasileiros, tornando a dimensão territorial uma importante fonte de informação para a previsão.

> Os resultados representam associações preditivas identificadas pelo modelo e **não devem ser interpretados como relações causais**.

---

## 🧠 Interpretabilidade com SHAP

Além da importância global das variáveis, foi utilizada a técnica **SHAP (SHapley Additive exPlanations)** para compreender como as variáveis contribuem para as previsões individuais.

O **SHAP Summary Plot** mostrou que as principais contribuições estão concentradas em:

1. `taxa_alfabetizacao_2023`;
2. variáveis relacionadas à `UF`;
3. `idade_mediana_2022`;
4. `percentual_participacao_2023`.

A análise permite observar não apenas **quais variáveis são importantes**, mas também a direção de sua contribuição para a previsão.

### Interpretação

- Valores SHAP **positivos** contribuem para aumentar a previsão;
- Valores SHAP **negativos** contribuem para reduzir a previsão;
- Quanto maior a distância em relação a zero, maior o impacto daquela variável na previsão.

A análise SHAP reforça o resultado obtido pela Feature Importance, principalmente em relação à importância da taxa de alfabetização de 2023 e da dimensão territorial.

---

## 🎯 Previsão de atingimento da meta

A previsão da taxa de alfabetização foi transformada em uma classificação de risco por meio da comparação:

taxa_prevista_2024 >= meta_alfabetizacao_2024


## Conclusão
O modelo possui muito espaço para melhoria, pois não conseguirmos enriquecer o modelo com variáveis que permitam uma melhore predição, todavia hoje já temos um modelo sem data leakage e que se consegue se aproximar o % de alfabetização na cidade certa dos municípios. Para próximos passos é válido a tentativa de enriquecimento com outras informações socieconômicas.


