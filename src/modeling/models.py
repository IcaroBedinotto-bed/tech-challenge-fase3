from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


def create_linear_regression(preprocessor):
    """
    Cria o pipeline de Regressão Linear.
    """

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])

    return model


def create_random_forest(preprocessor):
    """
    Cria o pipeline de Random Forest.
    """

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ))
    ])

    return model