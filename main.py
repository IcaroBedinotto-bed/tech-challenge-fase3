import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.preprocessing.build_base_analitica import build_base_analitica
from src.preprocessing.feature_engineering import build_features
from src.preprocessing.preprocessing_pipeline import create_preprocessor
from src.modeling.models import create_linear_regression, create_random_forest
from src.evaluation.metrics import calculate_regression_metrics
from src.evaluation.error_analysis import create_error_analysis, get_worst_errors, get_underestimated, get_overestimated
from src.evaluation.feature_importance import calculate_permutation_importance
from src.evaluation.shap_analysis import calculate_shap_values, create_shap_explanation
from src.visualization.shap_plots import plot_shap_summary, plot_shap_waterfall



#Criação da base análtica - Coração da modelagem
df = pd.read_parquet(
    "data/silver/meta_alfabetizacao_municipio/meta_alfabetizacao_municipio.parquet"
)


df_analitica = build_base_analitica(df)


Path("data/analytical").mkdir(
    parents=True,
    exist_ok=True
)

df_analitica.to_parquet(
    "data/analytical/base_analitica_v1.parquet",
    index=False
)

print("Base analitica inicial criada com sucesso")


#Enriquecimento das tabela - Apenas com o CENSO 2022
df_censo = pd.read_csv(
    "data/dados_populacao/censo_2022.csv"
)

df_modelo = build_features(df_analitica, df_censo)

df_modelo.to_parquet(
    "data/analytical/base_analitica_modelo.parquet",
    index=False
)

print("Base analitica para o modelo final criada com sucesso")


#Separação das features para modelagem
numeric_features = [
    "taxa_alfabetizacao_2023",
    "percentual_participacao_2023",
    "meta_alfabetizacao_2024",
    "domicilios_2022",
    "taxa_alfabetizacao_censo_2022",
    "idade_mediana_2022"
]

categorical_features = [
    "UF",
    "Capital"
]

X = df_modelo[
    numeric_features + categorical_features
]

y = df_modelo["taxa_alfabetizacao_2024"]

id_municipio = df_modelo["id_municipio"]

X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
    X,
    y,
    id_municipio,
    test_size=0.2,
    random_state=42
)

preprocessor = create_preprocessor(
    numeric_features=numeric_features,
    categorical_features=categorical_features
)



#Modelo de regressão linear
model_linear = create_linear_regression(
    preprocessor
)



model_linear.fit(
    X_train,
    y_train
)

y_pred_linear = model_linear.predict(
    X_test
)

feature_importance_linear = calculate_permutation_importance(
    model_linear,
    X_test,
    y_test
)

shap_values, X_test_transformed, shap_feature_names = calculate_shap_values(
    model_linear,
    X_test
)

print("\nSHAP:")
print("Quantidade de features:", len(shap_feature_names))
print("Quantidade de observações:", shap_values.shape[0])
print("Quantidade de features SHAP:", shap_values.shape[1])


# Identifica municípios previstos abaixo da meta
risco = X_test.copy()

risco["taxa_prevista_2024"] = y_pred_linear

risco["gap_previsto"] = (
    risco["meta_alfabetizacao_2024"]
    - risco["taxa_prevista_2024"]
)

risco = risco[
    risco["taxa_prevista_2024"]
    < risco["meta_alfabetizacao_2024"]
].copy()


# Seleciona o município com maior risco
gap_mediano = risco["gap_previsto"].median()

indice_risco = (
    (risco["gap_previsto"] - gap_mediano)
    .abs()
    .idxmin()
)

municipio_risco = risco.loc[indice_risco]


# Recupera a posição correspondente no SHAP
indice_risco = X_test.index.get_loc(
    municipio_risco.name
)


print("\nMunicípio selecionado para SHAP:")
print(
    f"Taxa prevista: "
    f"{municipio_risco['taxa_prevista_2024']:.2f}%"
)
print(
    f"Meta 2024: "
    f"{municipio_risco['meta_alfabetizacao_2024']:.2f}%"
)
print(
    f"Gap previsto: "
    f"{municipio_risco['gap_previsto']:.2f} p.p."
)


# SHAP local
explanation_risco = create_shap_explanation(
    shap_values,
    X_test_transformed,
    shap_feature_names,
    indice_risco
)

plot_shap_waterfall(
    explanation_risco
)




avaliacao_linear = create_error_analysis(
    id_municipio=id_test,
    y_true=y_test,
    y_pred=y_pred_linear
)

#Geração de arquivos para avaliação dos erros
piores_erros = get_worst_errors(
    avaliacao_linear
)

subestimou = get_underestimated(
    avaliacao_linear
)

superestimou = get_overestimated(
    avaliacao_linear
)



avaliacao_linear = create_error_analysis(
    id_municipio=id_test,
    y_true=y_test,
    y_pred=y_pred_linear
)

avaliacao_linear = avaliacao_linear.merge(
    df_modelo[
        [
            "id_municipio",
            "Municipio",
            "UF",
            "meta_alfabetizacao_2024"
        ]
    ],
    on="id_municipio",
    how="left",
    validate="one_to_one"
)

avaliacao_linear.to_parquet(
    "data/analytical/evaluation/erros_linear.parquet",
    index=False
)




metrics_linear = calculate_regression_metrics(
    y_test,
    y_pred_linear
)


print("Resultados - Regressão Linear")

print(
    f"MAE:  {metrics_linear['MAE']:.2f}"
)

print(
    f"RMSE: {metrics_linear['RMSE']:.2f}"
)

print(
    f"R²:   {metrics_linear['R2']:.2f}"
)





#Modelo Randon Forest
model_rf = create_random_forest(
    preprocessor
)

model_rf.fit(
    X_train,
    y_train
)

y_pred_rf = model_rf.predict(
    X_test
)