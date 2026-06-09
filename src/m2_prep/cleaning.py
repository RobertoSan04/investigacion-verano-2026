"""
cleaning.py - M2
Paso 2: parseo numerico

Objetivos:
- Mapear celdas no numericas (***, SD, C) -> NaN en columnas numericas
- Convertir columnas numericas de str -> float
- Dejar columnas de categoria o texto como str

Caracteres identificados:
- ***: Valor no medido -> NaN
- SD: Sin dato -> NaN
- C: Valor censurado -> NaN
- IgG Negativo -> 0.0
- IgG >250 -> 250


"""

import pandas as pd

# Caracteres
NAN_TOKENS = {"***", "SD", "C"}

# Columnas CMV
# Logica: Negativo -> 0.0, >250 -> 250 (Positivo)
COLUMNAS_CMV = {
    "CMV  IgM DONADOR",
    "CMV IgG DONADOR",
    "CMV  IgM RECEPTOR",
    "CMV IgG RECEPTOR",
}

# Columnas RH
COLUMNAS_RH = {
    " RH DONADOR",
    " RH RECEPTOR",
}

# Columnas de categorias o texto
COLUMNAS_NO_NUMERICAS = {
    "FECHA",
    "FOLIO",
    "DONADOR",
    "RECEPTOR",
    "DX",
    "CULTIVO M.",
    "PROCEDENCIA",
    "LUGAR DE INFUSIÓN",
    "OBSERVACIONES",
    "FECHA DE TRASPLANTE",
    "SITIO AFECTADO",
    "HCT-Cie",
    "MORBILIDADES PRETRASPLANTE",
    "COMPLICACIONES",
    "INFECCIONES ESPECÍFICAS",
    "MUERTE EN PRIMEROS 100 DÍAS",
    "MUERTE EN PRIMER AÑO",
    "MUERTE RELACIONADA AL TRASPLANTE",
    "TIPO",
    "SEXO DON",
    "ESTIMULACIÓN",
    "CEBADO",
    "DESECHABLE ",
    "MAQUINA ",
    "ACCESO",
    "EVENTOS ADV EN PROCESO",
    "GPO ABO DONADOR",
    "GPO ABO RECEPTOR",
}

def _parsear_cmv(serie: pd.Series) -> pd.Series:
    # Parear una columna de CMV a float

    s = serie.str.strip()
    s = s.replace(list(NAN_TOKENS), pd.NA)
    s = s.replace("NEGATIVO", "0.0")
    s = s.replace(">250", "250")

    return pd.to_numeric(s, errors = "coerce")

def _parsear_rh(serie: pd.Series) -> pd.Series:
    # Parsear una columna de RH
    s = serie.str.strip()
    s = s.replace("POSITIVO", "1.0")
    s = s.replace("NEGATIVO", "0.0")
    return pd.to_numeric(s, errors = "coerce")

def parsear_numericos(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Convierte columnas numericas de str -> float

    Parametros:
    - df: pd.DataFrame
        df_raw proviene de loader.cargar_hoja1 (todo en str)
    - verbose: bool
        Si True, imprime resumen de conversiones y NaN generados

    Returns:
    - pd.DataFrame:
        Igual que la entrada pero con columnas numericas ahora como float y
        columnas no numericas siguen como str
    """

    df = df.copy()

    cols_generales = []
    cols_nan_inesperados = {}

    for col in df.columns:

        if col in COLUMNAS_NO_NUMERICAS:
            continue

        if col in COLUMNAS_CMV:
            df[col] = _parsear_cmv(df[col])
            cols_generales.append(col)
            continue

        if col in COLUMNAS_RH:
            df[col] = _parsear_rh(df[col])
            cols_generales.append(col)
            continue

        serie = df[col].str.strip()
        serie = serie.replace(list(NAN_TOKENS), pd.NA)
        serie_num = pd.to_numeric(serie, errors = "coerce")

        nan_nuevos = serie_num.isna().sum() - serie.isna().sum
        if nan_nuevos > 0:
            mask = serie_num.isna() & serie.notna()
            cols_nan_inesperados[col] ={
                "nan_extra": int(nan_nuevos),
                "tokens": serie[mask].unique().tolist(),
            }

        df[col] = serie_num
        cols_generales.append(col)

    if verbose:
        n_no_num = len(COLUMNAS_NO_NUMERICAS)
        n_cmv = len(COLUMNAS_CMV)
        n_rh = len(COLUMNAS_RH)
        n_gen = len(cols_generales) - n_cmv - n_rh
        print(f"[cleaning] Columnas numéricas generales : {n_gen}")
        print(f"[cleaning] Columnas CMV (serológicas)   : {n_cmv}  → NEGATIVO=0, >250=250, número=float")
        print(f"[cleaning] Columnas RH  (binarias)      : {n_rh}  → POSITIVO=1, NEGATIVO=0")
        print(f"[cleaning] Columnas no-numéricas        : {n_no_num}")

        if cols_nan_inesperados:
            print("\n[cleaning] Tokens inesperados (revisar):")
            for col, info in cols_nan_inesperados.items():
                print(f"  {col!r}: {info['nan_extra']} NaN extra - tokens: {info['tokens']}")
        else:
            print("[cleaning] Sin tokens inesperados - parseo limpio")

        # NaN por columna numérica
        cols_num = [c for c in df.columns if c not in COLUMNAS_NO_NUMERICAS]
        nan_counts = df[cols_num].isna().sum()
        nan_counts = nan_counts[nan_counts > 0].sort_values(ascending=False)
        if not nan_counts.empty:
            print("\n[cleaning] NaN por columna numérica:")
            for col, n in nan_counts.items():
                pct = 100 * n / len(df)
                print(f"  {col!r:45s}: {n:>3} ({pct:.1f}%)")

    return df