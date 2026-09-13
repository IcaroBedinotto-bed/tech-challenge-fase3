import matplotlib.pyplot as plt
import shap


def plot_shap_summary(
    shap_values,
    X_transformed,
    feature_names
):
    shap.summary_plot(
        shap_values,
        X_transformed,
        feature_names=feature_names,
        show=False
    )

    plt.tight_layout()
    plt.show()


def plot_shap_waterfall(explanation):
    shap.plots.waterfall(
        explanation,
        max_display=10,
        show=False
    )

    plt.tight_layout()
    plt.show()