import pandas as pd


def build_base_analitica(df: pd.DataFrame) -> pd.DataFrame:

    df_2023 = df[df["ano"] == 2023].copy()
    df_2024 = df[df["ano"] == 2024].copy()

    base_2023 = df_2023[
        [
            "id_municipio",
            "Municipio",
            "UF",
            "Capital",
            "taxa_alfabetizacao",
            "percentual_participacao"
        ]
    ].copy()

    base_2023 = base_2023.rename(columns={
        "taxa_alfabetizacao": "taxa_alfabetizacao_2023",
        "percentual_participacao": "percentual_participacao_2023",
    })

    base_2024 = df_2024[
        [
            "id_municipio",
            "meta_alfabetizacao_2024",
            "taxa_alfabetizacao"
        ]
    ].copy()

    base_2024 = base_2024.rename(columns={
        "taxa_alfabetizacao": "taxa_alfabetizacao_2024"
    })



    base = base_2023.merge(
        base_2024,
        on="id_municipio",
        how="inner",
        validate="one_to_one"
    )

    base = base.dropna(
        subset=["meta_alfabetizacao_2024"]
    ).copy()

    UF_REGIAO = {
    "AC": "Norte",
    "AP": "Norte",
    "AM": "Norte",
    "PA": "Norte",
    "RO": "Norte",
    "RR": "Norte",
    "TO": "Norte",

    "AL": "Nordeste",
    "BA": "Nordeste",
    "CE": "Nordeste",
    "MA": "Nordeste",
    "PB": "Nordeste",
    "PE": "Nordeste",
    "PI": "Nordeste",
    "RN": "Nordeste",
    "SE": "Nordeste",

    "DF": "Centro-Oeste",
    "GO": "Centro-Oeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",

    "ES": "Sudeste",
    "MG": "Sudeste",
    "RJ": "Sudeste",
    "SP": "Sudeste",

    "PR": "Sul",
    "RS": "Sul",
    "SC": "Sul",
    }

    base["Regiao"] = base["UF"].map(UF_REGIAO)

    if base["Regiao"].isna().any():
        raise ValueError(
            "Existem UFs sem região mapeada."
        )

    base["gap_meta_2024"] = (
        base["meta_alfabetizacao_2024"]
        - base["taxa_alfabetizacao_2023"]
    )

    base["target_atingiu_meta_2024"] = (
        base["taxa_alfabetizacao_2024"]
        >= base["meta_alfabetizacao_2024"]
    ).astype(int)

    # validações...

    return base