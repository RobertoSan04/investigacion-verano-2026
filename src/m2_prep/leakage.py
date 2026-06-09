"""
leakage.py - M2
Paso 3: Eliminar leakage, ID's y outcomes

Categorias de columnas eliminadas:
- IDs:
    Identificadores, sin valor predictivo

- Leakage directo:
    Algunas columnas se calculan usando WB, entonces incluirlas en X causaria
    una fuga de informacion.
    - CE2% CD34+ = (CD34+ cosechados / CD34+ en sangre procesada) × 100
    - CE2% MNC = (COSECHA MNC / (PRE MNC * WB)) * 100
    - VOL. SANGUINEO PROCESADO mL = Processed WB * 1000
    - VOL. TOTAL PROCESADO mL, VOLEMIAS PROCESADAS, ACD TOT,
       VOL. PRODUCTO, VOLUMEN CALCULADO: todos derivados del volumen
       procesado o calculados junto con él durante el procedimiento.
    - % DE PÉRDIDA PLAQUETARIA

- Leakage temporal:
     Medidas durante o despues del procedimiento. No pueden usarse para predecir WB
     - TIEMPO MIN, VEL. INICIAL/MEDIANA/FINAL mL/MIN
     - COSECHA
     - POST

- Outcomes post-transplante
    Resultados clinicos del receptor despues

- Target
    Processed WB
"""

import pandas as pd

TARGET = "Processed WB (liters)"

# IDs
COLS_IDS = [
    "FECHA",
    "FOLIO",
    "DONADOR",
    "RECEPTOR",
    "DX",
    "NO. DE RECOLECCIÓN",
    "CULTIVO M.",
    "PROCEDENCIA",
    "FECHA DE TRASPLANTE",
    "LUGAR DE INFUSIÓN",
    "OBSERVACIONES",
    "SITIO AFECTADO",
    "HCT-Cie",
]

# Leakage directo
COLS_LEAKAGE_DIRECTO = [
    "VOL. SANGUÍNEO PROCESADO mL",    # = Processed WB (liters) × 1000 (corr=1.0)
    "VOL. TOTAL PROCESADO mL",        # = VOL. SANGUÍNEO + ACD; depende de WB
    "VOLEMIAS PROCESADAS",            # = WB / VOLEMIA; depende de WB
    "ACD TOT",                        # anticoagulante proporcional al vol. procesado
    "VOL. PRODUCTO",                  # volumen del producto recolectado (post-WB)
    "VOLUMEN CALCULADO",              # calculado junto con WB en el protocolo
    "CE2% CD34+",                     # = CD34+ cosechados / CD34+ procesados × 100
    "CE2% MNC",                       # análogo para MNC
    "% DE PÉRDIDA PLAQUETARIA",       # calculada sobre producto post-procedimiento
]

# Leakage temporal
COLS_LEAKAGE_TEMPORAL = [
    # intra-procedimiento
    "TIEMPO MIN.",
    "VEL. INICIAL mL/min",
    "VEL. MEDIANA mL/min",
    "VEL. FINAL mL/min",
    # producto cosechado (post-WB)
    "COSECHA WBC k/µL",
    "COSECHA  MNC%",
    "COSECHA MNC k/µL",
    " COSECHA CMN X10^9/ VOL TOTAL",
    "COSECHA HTO %",
    "COSECHA RBC x10⁶/µL",
    "COSECHA PLT k/µL ",
    "COSECHA    CD34+/µL",
    "COSECHA CD34+TOTAL",
    "COSECHA     CD34+ x10⁶/kg",
    "COSECHA CD45+/μL",
    "VIABILIDAD %",
    # post-procedimiento del donador
    "POST WBC k/µL",
    "POST MNC %",
    "POST MNC k/µL",
    "POST HTO %",
    "POST  PLT k/µL ",
    "POST CD34+/µL ",
]

# Outcomes
COLS_OUTCOMES = [
    "CD34+/kg TRASPLANTE",
    "CD34+/kg CRIO",
    "VIAB CRIO %",
    "REC MIELOIDE",
    "REC PLAQ",
    "EICH AGUDO",
    "EICH CRONICO",
    "MORBILIDADES PRETRASPLANTE",
    "COMPLICACIONES",
    "INFECCIONES ESPECÍFICAS",
    "MUERTE EN PRIMEROS 100 DÍAS",
    "MUERTE EN PRIMER AÑO",
    "MUERTE RELACIONADA AL TRASPLANTE",
]

# Lista completa de columnas a eliminar
COLS_ELIMINAR = (
    COLS_IDS
    + COLS_LEAKAGE_DIRECTO
    + COLS_LEAKAGE_TEMPORAL
    + COLS_OUTCOMES
)

def quitar_leakage(df: pd.DataFrame, verbose = True) -> tuple[pd.DataFrame, pd.Series]:
    """
    Elimina las columnas leakage, IDS y outcomes. Tambien separa el target y (WB).

    Parametros:
    - df: pd.DataFrame
        df_parsed proveniente de cleaning.parsear_numericos

    - verbose: True
        Si True, imprime resumen de columnas eliminadas y conservadas

    Returns:
    - X: pd.DataFrame
        Listas sin leakage

    - y: pd.Series
        Target: Processed WB

    En caso de error:
    - KeyError:
        Si el target no esta en el df

    - ValueError:
        Si alguna columna de X tiene correlacion >= 0.99 con y
    """

    if TARGET not in df.columns:
        raise KeyError(f"Target '{TARGET}' no encontrado en el DataFrame.")


    y = df[TARGET].copy()

    # Columnas a eliminar: leakage + ids + outcomes + target
    a_eliminar = set(COLS_ELIMINAR) | {TARGET}

    # Verificar que todas las columnas listadas existen (avisar si alguna no)
    no_encontradas = [c for c in COLS_ELIMINAR if c not in df.columns]
    if no_encontradas and verbose:
        print(f"[leakage] Columnas en lista pero no en df (ignoradas): {no_encontradas}")

    # Construir X
    cols_X = [c for c in df.columns if c not in a_eliminar]
    X = df[cols_X].copy()

    # Checamos la correlacion entre y
    filas_validas = y.notna()
    y_clean = y[filas_validas]
    leakage_detectado = []

    for col in X.select_dtypes("number").columns:
        x_col = X.loc[filas_validas, col]
        if x_col.notna().sum() < 10:
            continue  # no suficientes datos para calcular correlación
        corr = abs(x_col.corr(y_clean))
        if corr >= 0.99:
            leakage_detectado.append((col, round(corr, 4)))

    if leakage_detectado:
        raise ValueError(
            f"[leakage] Leakage detectado - correlación >= 0.99 con y:\n"
            + "\n".join(f"  {c}: corr={v}" for c, v in leakage_detectado)
        )

    if verbose:
        print(f"[leakage] Columnas eliminadas : {len(a_eliminar)}")
        print(f"  IDs / texto libre           : {len(COLS_IDS)}")
        print(f"  Leakage directo             : {len(COLS_LEAKAGE_DIRECTO)}")
        print(f"  Leakage temporal            : {len(COLS_LEAKAGE_TEMPORAL)}")
        print(f"  Outcomes post-trasplante    : {len(COLS_OUTCOMES)}")
        print(f"  Target (y)                  : 1")
        print(f"[leakage] Columnas en X       : {len(cols_X)}")
        print(f"[leakage] Test anti-leakage : sin correlaciones ≥ 0.99")
        print(f"\n[leakage] Features en X:")
        for c in X.columns:
            print(f"  {c!r}")
        print(f"\n[leakage] y = '{TARGET}'")
        print(f"  NaN en y: {y.isna().sum()} / {len(y)}")
        print(f"  Rango: [{y.min():.3f}, {y.max():.3f}] litros")

    return X, y