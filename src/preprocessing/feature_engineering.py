import pandas as pd


def build_features(
    df: pd.DataFrame,
    df_censo: pd.DataFrame
) -> pd.DataFrame:


    df_features = df.copy()
    df_censo = df_censo.copy()

    # Seleciona as variáveis do Censo que serão utilizadas
    df_censo = df_censo[
        [
            "id_municipio",
            "domicilios",
            "taxa_alfabetizacao",
            "indice_envelhecimento",
            "idade_mediana",
            "razao_sexo"
        ]
    ].copy()

    # Padroniza o tipo do identificador do município
    df_features["id_municipio"] = (
        pd.to_numeric(
            df_features["id_municipio"],
            errors="coerce"
        )
        .astype("Int64")
        .astype(str)
    )


    df_censo["id_municipio"] = (
        pd.to_numeric(
            df_censo["id_municipio"],
            errors="coerce"
        )
        .astype("Int64")
        .astype(str)
    )

    # Renomeia as variáveis para deixar clara a origem
    df_censo = df_censo.rename(
        columns={
            "domicilios": "domicilios_2022",
            "taxa_alfabetizacao": "taxa_alfabetizacao_censo_2022",
            "indice_envelhecimento": "indice_envelhecimento_2022",
            "idade_mediana": "idade_mediana_2022",
            "razao_sexo": "razao_sexo_2022"
        }
    )

    # Converte a taxa do Censo de 0-1 para 0-100
    df_censo["taxa_alfabetizacao_censo_2022"] = (
        df_censo["taxa_alfabetizacao_censo_2022"] * 100
    )

    # Merge
    df_features = df_features.merge(
        df_censo,
        on="id_municipio",
        how="left",
        validate="one_to_one"
    )

    return df_features