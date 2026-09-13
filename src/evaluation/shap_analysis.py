import shap


def calculate_shap_values(
    model,
    X_test
):
    preprocessor = model.named_steps["preprocessor"]
    regressor = model.named_steps["regressor"]

    X_test_transformed = preprocessor.transform(X_test)

    if hasattr(X_test_transformed, "toarray"):
        X_test_transformed = X_test_transformed.toarray()

    feature_names = preprocessor.get_feature_names_out()

    explainer = shap.LinearExplainer(
        regressor,
        X_test_transformed
    )

    shap_values = explainer(
        X_test_transformed
    )

    return (
        shap_values,
        X_test_transformed,
        feature_names
    )


def create_shap_explanation(
    shap_values,
    X_test_transformed,
    feature_names,
    index
):
    explanation = shap.Explanation(
        values=shap_values[index].values,
        base_values=shap_values[index].base_values,
        data=X_test_transformed[index],
        feature_names=feature_names
    )

    return explanation