"""
build_df_clean.py - M2
Paso 5: Pipeline completo

Corre los 4 pasos anteriores en secuencia y guarda el resultado:
1. loader.cargar_hoja1
2. cleaning.parsear_numericos
3. leakage.quitar_leakage -> X, y
4. encoding.encodear_categoricas _. X_enc
5. Combinar X_enc + y -> df_clean.parquet
"""

import argparse
import sys
import pandas as pd
from pathlib import Path

from src.m2_preparacion.loader import cargar_hoja1
from src.m2_preparacion.cleaning import parsear_numericos
from src.m2_preparacion.leakage import quitar_leakage
from src.m2_preparacion.encoding import encodear_categoricas

# Añadir raíz del proyecto al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def build_df_clean(data_path: str, out_path: str) -> pd.DataFrame:
    print("=" * 50)
    print("M2 - Pipeline de preparación de datos")
    print("=" * 50)

    # Paso 1 — Carga
    print("\n[1/4] Cargando Hoja1...")
    df_raw = cargar_hoja1(data_path, verbose=True)

    # Paso 2 — Parseo numérico
    print("\n[2/4] Parseando numéricos...")
    df_parsed = parsear_numericos(df_raw, verbose=True)

    # Paso 3 — Quitar leakage y separar y
    print("\n[3/4] Eliminando leakage...")
    X, y = quitar_leakage(df_parsed, verbose=True)

    # Paso 4 — Encoding
    print("\n[4/4] Encoding de categóricas...")
    X_enc = encodear_categoricas(X, verbose=True)

    # Combinar X_enc + y en df_clean
    df_clean = X_enc.copy()
    df_clean["Processed WB (liters)"] = y.values

    # Guardar
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_parquet(out, index=False)

    print("\n" + "=" * 50)
    print(f"df_clean guardado en: {out}")
    print(f"Shape: {df_clean.shape}  ({df_clean.shape[1]-1} features + 1 target)")
    print(f"NaN en y: {df_clean['Processed WB (liters)'].isna().sum()}")
    print("=" * 50)

    return df_clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera df_clean.parquet desde el Excel de aféresis.")
    parser.add_argument("--data", required=True, help="Ruta al archivo .xlsx")
    parser.add_argument("--out", default="data/df_clean.parquet", help="Ruta de salida del parquet")
    args = parser.parse_args()

    build_df_clean(args.data, args.out)
