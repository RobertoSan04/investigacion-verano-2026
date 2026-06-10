"""
pca_analysis.py - M3
Modulo de PCA sobre df_clean
"""

import pandas as pd
import numpy as np
from sympy.simplify.hyperexpand import Hyper_Function

TARGET = "Processed WB (liters)"
COL_DIA4 = "CD34+ /µL DÍA 4"

def preparar_para_pca(df_clean: pd.DataFrame, verbose: bool = True) -> tuple[pd.DataFrame, pd.Series, pd.Index]:
    """
    Preparar df_clean para PCA

    Parametros:
    - df_clean:
        DataFrame con features + target
    - verbose:
         Si True, imprime resumen de cada paso.

    Returns:
    - X:
        DataFrame listo para escalar y correr PCA
    - y:
        Series del target
    - idx:
        Index de filas conservadas
    """

    df = df_clean.copy()

    # Separar y
    if TARGET not in df.columns:
        raise KeyError(f"Target '{TARGET}' no encontrado en df_clean")

    y_full = df[TARGET]
    df = df.drop(columns = [TARGET])

    if verbose:
        print(f"[prep] Filas iniciales   : {len(df)}")
        print(f"[prep] Features iniciales: {df.shape[1]}")

    # Drop CD34+ DIA 4
    if COL_DIA4 not in df.columns:
        raise KeyError(f"Columna '{COL_DIA4}' no encontrada.")

    df = df.drop(columns=[COL_DIA4])

    if verbose:
        print(f"\n[prep] Dropped '{COL_DIA4}' (35% NaN, timing de medición)")
        print(f"[prep] Features tras drop: {df.shape[1]}")

    # Dropear filas con NaN restante
    cols_con_nan = df.columns[df.isna().any()].tolist()
    filas_con_nan = df.isna().any(axis=1).sum()

    df = df.join(y_full)
    df = df.dropna().reset_index(drop=True)

    y = df[TARGET]
    df = df.drop(columns=[TARGET])

    if verbose:
        print(f"\n[prep] Columnas con NaN  : {cols_con_nan}")
        print(f"[prep] Filas eliminadas  : {filas_con_nan}")
        print(f"\n[prep] Shape final → X: {df.shape} | y: {len(y)} filas")
        print(f"[prep] NaN en X: {df.isna().sum().sum()} (debe ser 0)")
        print(f"[prep] NaN en y: {y.isna().sum()} (debe ser 0)")

    return df, y, df.index


def escalar(X: pd.DataFrame) -> tuple[pd.DataFrame, "StandardScaler"]:
    """
    Aplica z-score (StandardScaler) a X.

    Returns:
    - X_scaled:
        DataFrame escalado (mismas columnas).
    - scaler:
        scaler ajustado (guardar para invertir en M4 si hace falta).
    """

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    arr = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(arr, columns=X.columns)
    return X_scaled, scaler


def correr_pca(X_scaled: pd.DataFrame) -> tuple["PCA", np.ndarray]:
    """
    Corre PCA sobre X_scaled (ya estandarizado).

    Returns:
    - pca:
        objeto PCA ajustado.
    - scores:
        proyección de las observaciones (n x n_components).
    """

    from sklearn.decomposition import PCA

    pca = PCA()
    scores = pca.fit_transform(X_scaled.values)
    return pca, scores


def tabla_loadings(pca, columnas: list, n_pcs: int = 6) -> pd.DataFrame:
    """
    Devuelve un DataFrame de loadings (variables × PCs).

    Parámetros:
    - pca:
        objeto PCA ya ajustado.
    - columnas:
        nombres de las features originales.
    - n_pcs:
        cuántos PCs incluir.

    Returns:
        DataFrame con shape (n_features, n_pcs).
    """

    return pd.DataFrame(
        pca.components_[:n_pcs].T,
        index=columnas,
        columns=[f"PC{i+1}" for i in range(n_pcs)],
    )
