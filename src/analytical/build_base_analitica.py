import pandas as pd


def build_base_analitica(
    df: pd.DataFrame,
    dim_municipio: pd.DataFrame
) -> pd.DataFrame:

    # =========================================================
    # 1. Municípios que possuem meta definida para 2024
    # =========================================================

    municipios_com_meta = (
        df[
            (df["ano"] == 2024) &
            (df["ID_Rede"] == 3) &
            (df["meta"].notna())
        ]["id_municipio"]
        .unique()
    )

    # =========================================================
    # 2. Dados de 2023
    #    Somente informações que podem ser utilizadas como
    #    features do modelo
    # =========================================================

    df_2023 = df[
        (df["ano"] == 2023) &
        (df["ID_Rede"] == 3) &
        (df["id_municipio"].isin(municipios_com_meta))
    ].copy()

    features_2023 = [
        "id_municipio",
        "taxa_alfabetizacao",
        "taxa_presenca",
        "taxa_preenchimento",
        "alunos_avaliados",
        "alunos_alfabetizados",
        "alunos_presentes",
        "provas_preenchidas"
    ]

    df_2023 = df_2023[features_2023]

    df_2023 = df_2023.rename(
        columns={
            "taxa_alfabetizacao": "taxa_alfabetizacao_2023",
            "taxa_presenca": "taxa_presenca_2023",
            "taxa_preenchimento": "taxa_preenchimento_2023",
            "alunos_avaliados": "alunos_avaliados_2023",
            "alunos_alfabetizados": "alunos_alfabetizados_2023",
            "alunos_presentes": "alunos_presentes_2023",
            "provas_preenchidas": "provas_preenchidas_2023"
        }
    )

    # =========================================================
    # 3. Dados de 2024
    #    Usados somente para construir o target
    # =========================================================

    df_2024 = df[
        (df["ano"] == 2024) &
        (df["ID_Rede"] == 3) &
        (df["id_municipio"].isin(municipios_com_meta))
    ].copy()

    meta_2024 = (
        df_2024[
            [
                "id_municipio",
                "meta"
            ]
        ]
        .rename(
            columns={
                "meta": "meta_2024"
            }
        )
    )

    resultado_2024 = (
        df_2024[
            [
                "id_municipio",
                "taxa_alfabetizacao"
            ]
        ]
        .rename(
            columns={
                "taxa_alfabetizacao": "taxa_alfabetizacao_2024"
            }
        )
    )

    # =========================================================
    # 4. Construção da base
    # =========================================================

    base = df_2023.merge(
        meta_2024,
        on="id_municipio",
        how="inner"
    )

    base = base.merge(
        resultado_2024,
        on="id_municipio",
        how="inner"
    )

    # =========================================================
    # 5. Criar TARGET
    #
    # 1 = atingiu a meta em 2024
    # 0 = não atingiu a meta em 2024
    # =========================================================

    base["target_atingiu_meta_2024"] = (
        base["taxa_alfabetizacao_2024"]
        >= base["meta_2024"]
    ).astype(int)

    # =========================================================
    # 6. Enriquecimento com dimensão Município
    #
    # UF é uma informação territorial e pode ser utilizada
    # como feature.
    # =========================================================

    dim_municipio_reduzida = (
        dim_municipio[
            [
                "id_municipio",
                "UF"
            ]
        ]
        .drop_duplicates()
    )

    base = base.merge(
        dim_municipio_reduzida,
        on="id_municipio",
        how="left",
        validate="one_to_one"
    )

    # =========================================================
    # 7. Validações
    # =========================================================

    if base["id_municipio"].nunique() != len(base):
        raise ValueError(
            "Existem municípios duplicados na Base Analítica."
        )

    if base["meta_2024"].isna().any():
        raise ValueError(
            "Existem municípios sem meta de 2024."
        )

    if base["UF"].isna().any():
        raise ValueError(
            "Existem municípios sem UF na dimensão Município."
        )

    # =========================================================
    # 8. Remover informação de 2024 utilizada para criar
    #    o target, evitando data leakage
    # =========================================================

    base = base.drop(
        columns=[
            "taxa_alfabetizacao_2024"
        ]
    )

    return base