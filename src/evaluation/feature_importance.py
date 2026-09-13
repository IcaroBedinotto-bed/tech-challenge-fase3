import pandas as pd
from sklearn.inspection import permutation_importance


def calculate_permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10
) -> pd.DataFrame:

    resultado = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="neg_mean_absolute_error",
        n_repeats=n_repeats,
        random_state=42
    )

    feature_importance = pd.DataFrame({
        "variavel": X_test.columns,
        "importancia": resultado.importances_mean,
        "desvio_padrao": resultado.importances_std
    })

    feature_importance = feature_importance.sort_values(
        "importancia",
        ascending=False
    ).reset_index(drop=True)

    return feature_importance