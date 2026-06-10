"""
encoding.py - M2
Paso 4: encoding de columnas categoricas

Estrategia por columna:
- SEXO DON: binaria: M=1, F=0
- TIPO: 3 categorías (IDÉNTICO agrupado en ALOGÉNICO)
- ESTIMULACIÓN: binaria FILGRASTIM PEGILADO=1, resto=0
- CEBADO: binaria SI=1, NO=0
- DESECHABLE: binaria IDL=1, ***=0
- MAQUINA: 3 categorías (***→NaN)
- ACCESO: 3 categorías
- EVENTOS ADV EN PROCESO: binaria: NINGUNO=0, cualquier evento=1
- GPO ABO DONADOR: 4 categorías
- GPO ABO RECEPTOR: 4 categorías (A/O -> NaN, es caso ambiguo único)

"""

import pandas as pd

def encodear_categorias(X: pd.DataFrame, verbose:bool = True) -> pd.DataFrame:
    """
    Aplicar el encoding a todas las columnas categoricas de X.

    Parametros:
    - X: pd.DataFrame
        Features post-leakage

    - verbose: Bool
        Si True, imprime resumen de transformaciones aplicadas.

    Returns:
    - pd.DataFrame
        X con columnas categoricas reemplazadas por su representacion numérica.
        Las columnas originales no se modifican
    """

    X = X.copy()
    log = []

    # SEXO DON -> M = 1, F = 0
    X["SEXO DON"] = X["SEXO DON"].map({"M": 1, "F": 0})
    log.append("SEXO DON: binaria: M=1, F=0")

    # TIPO -> 3 Categorias
    # IDÉNTICO (1 caso) se agrupa en ALOGÉNICO
    X["TIPO"] = X["TIPO"].replace("IDÉNTICO", "ALOGÉNICO")
    tipo_dummies = pd.get_dummies(X["TIPO"], prefix="TIPO", dtype=float)
    X = pd.concat([X.drop(columns=["TIPO"]), tipo_dummies], axis=1)
    log.append("TIPO: 3 cols (AUTÓLOGO, HAPLOIDÉNTICO, ALOGÉNICO)")

    # ESTIMULACION -> binaria pegilado/estandar
    X["ESTIMULACION_PEGILADO"] = (
            X["ESTIMULACIÓN"].str.strip() == "FILGRASTIM PEGILADO"
    ).astype(float)
    X = X.drop(columns=["ESTIMULACIÓN"])
    log.append("ESTIMULACIÓN: binaria (PEGILADO=1, resto=0)")

    # CEBADO -> SI = 1, NO = 0
    X["CEBADO"] = X["CEBADO"].map({"SI": 1, "NO": 0})
    log.append("- CEBADO: binaria (SI=1, NO=0) — 2 NaN conservados")

    # DESECHABLE -> IDL = 1 *** = 0
    col_des = "DESECHABLE "
    X[col_des] = X[col_des].map({"IDL": 1, "***": 0})
    X = X.rename(columns={col_des: "DESECHABLE"})
    log.append("DESECHABLE: binaria (IDL=1, ***=0)")

    # MAQUINA (*** -> NaN)
    col_maq = "MAQUINA "
    X[col_maq] = X[col_maq].replace("***", None)
    maq_dummies = pd.get_dummies(X[col_maq], prefix="MAQUINA", dtype=float)
    # NaN en original -> fila de ceros en dummies; restaurar como NaN
    nan_mask = X[col_maq].isna()
    maq_dummies[nan_mask] = float("nan")
    X = pd.concat([X.drop(columns=[col_maq]), maq_dummies], axis=1)
    log.append("MAQUINA: 3 cols (EMT-25, EMT-50, EMT-68) — 2 NaN")

    # ACCESO -> 3 categorias (CATETER, PUNCION, AMO)
    acceso_dummies = pd.get_dummies(X["ACCESO"], prefix="ACCESO", dtype=float)
    X = pd.concat([X.drop(columns=["ACCESO"]), acceso_dummies], axis=1)
    log.append("ACCESO: 3 cols (CATÉTER, PUNCIÓN, AMO)")

    # EVENTOS ADV EN PROCESO -> binaria (tuvo evento / no tuvo)
    X["EVENTO_ADV"] = (
            X["EVENTOS ADV EN PROCESO"].str.strip() != "NINGUNO"
    ).astype(float)
    X = X.drop(columns=["EVENTOS ADV EN PROCESO"])
    log.append("EVENTOS ADV EN PROCESO -> binaria (NINGUNO=0, cualquier evento=1)")

    # GPO ABO DONADOR -> one-hot 4 categorías
    abo_don = pd.get_dummies(X["GPO ABO DONADOR"], prefix="ABO_DON", dtype=float)
    X = pd.concat([X.drop(columns=["GPO ABO DONADOR"]), abo_don], axis=1)
    log.append("GPO ABO DONADOR -> one-hot 4 cols (A, AB, B, O)")

    # GPO ABO RECEPTOR -> one-hot 4 categorías (A/O → NaN)
    X["GPO ABO RECEPTOR"] = X["GPO ABO RECEPTOR"].replace("A/O", None)
    abo_rec = pd.get_dummies(X["GPO ABO RECEPTOR"], prefix="ABO_REC", dtype=float)
    nan_mask_rec = X["GPO ABO RECEPTOR"].isna()
    abo_rec[nan_mask_rec] = float("nan")
    X = pd.concat([X.drop(columns=["GPO ABO RECEPTOR"]), abo_rec], axis=1)
    log.append("GPO ABO RECEPTOR -> one-hot 4 cols (A, AB, B, O) — A/O→NaN")

    if verbose:
        print("[encoding] Transformaciones aplicadas:")
        for line in log:
            print(f"  {line}")
        print(f"\n[encoding] Shape final de X: {X.shape}")
        # Verificar que no queden columnas object
        obj_restantes = X.select_dtypes("object").columns.tolist()
        if obj_restantes:
            print(f"[encoding] Columnas object restantes: {obj_restantes}")
        else:
            print("[encoding] Sin columnas categóricas - X lista para PCA/SR")

    return X
