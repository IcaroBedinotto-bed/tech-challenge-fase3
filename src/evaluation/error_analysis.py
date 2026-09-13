import pandas as pd


def create_error_analysis(
    id_municipio,
    y_true,
    y_pred
):
    avaliacao = pd.DataFrame({
        "id_municipio": id_municipio,
        "real": y_true,
        "previsto": y_pred
    })

    avaliacao["erro"] = (
        avaliacao["real"] - avaliacao["previsto"]
    )

    avaliacao["erro_absoluto"] = (
        avaliacao["erro"].abs()
    )

    return avaliacao


def get_worst_errors(
    avaliacao,
    n=10
):
    return avaliacao.sort_values(
        "erro_absoluto",
        ascending=False
    ).head(n)


def get_underestimated(
    avaliacao,
    n=10
):
    return avaliacao.sort_values(
        "erro",
        ascending=False
    ).head(n)


def get_overestimated(
    avaliacao,
    n=10
):
    return avaliacao.sort_values(
        "erro",
        ascending=True
    ).head(n)