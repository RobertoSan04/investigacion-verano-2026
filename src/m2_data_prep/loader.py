"""
loader.py - M2
Paso 1: Cargar y validacion inicial de Hoja 1

Objetivos:
- Leer unicamente Hoja1 del excel
- Dropear filas sin FOLIO
- Validar que el numero de filas resultantes sea el esperado
- No modificar valores, no dropear columnas

"""

import pandas as pd
from numpy.ma.core import masked_less

SHEET_NAME = "Hoja1"
FOLIO_COL = "FOLIO"
EXPECTED_ROWS = 116

def cargar_hoja1(path: str, verbose: bool = True) -> pd.DataFrame:
    """
    Cargar Hoja1 del Excel y elimina filas sin FOLIO

    Parametros:
    - path: str
        Ruta del archivo (/Users/robertosanchezsantoyo/Library/Mobile Documents/com~apple~CloudDocs/00_Main/03_Academic/Research/Investigacion_verano_2026/data/raw/2025 CPH.xlsx)
    - verbose: bool
        Si True, imprime resumen de carga y validacion

    Returns:
    - pd.DataFrame
        DataFrame crudo
        Header = nombres originales del Excel

    En caso de error:
    - FileNotFoundError
        Si el archivo no existe
    - ValueError
        Si el numero de filas validas no coincide con EXPECTED_ROWS
    - KeyError
        Si la columna FOLIO no esta en el header
    """

    df = pd.read_excel(
        path,
        sheet_name = SHEET_NAME,
        header = 0,
        dtype = str,
        engine = "openpyxl"
    )

    if verbose:
        print(f"[loader] Hoja1 cargada: {df.shape[0]} filas x {df.shape[1]} cols")

    # Validar columna FOLIO
    if FOLIO_COL not in df.columns:
        raise KeyError(
            f"No se encontro la columna"
            f"Columnas disponibles: {df.columnas.tolist()}"
        )

    # Drop de filas sin FOLIO
    mask_valido = df[FOLIO_COL].notna() & (df[FOLIO_COL].str.strip() != "")
    df = df[mask_valido].copy()
    df.reset_index(drop = True, inplace = True)

    if verbose:
        print(f"[loader] Filas con FOLIO válido: {df.shape[0]}")

    # --- validación ---
    if df.shape[0] != EXPECTED_ROWS:
        raise ValueError(
            f"Se esperaban {EXPECTED_ROWS} filas con FOLIO, "
            f"se obtuvieron {df.shape[0]}. Revisar el archivo."
        )

    if verbose:
        print(f"[loader] Validación OK: {EXPECTED_ROWS} filas, {df.shape[1]} columnas")
        print(f"[loader] Columnas: {df.columns.tolist()}")

    return df

