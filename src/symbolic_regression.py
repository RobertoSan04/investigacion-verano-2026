"""
symbolic_regression.py - M4
Módulo de regresión simbólica sobre df_clean.

Convenciones:
- Funciones puras: no leen archivos, no muestran gráficas, sin side effects.
- Imports pesados (PySR, sklearn) son lazy (dentro de cada función).
- Todos los verbose= imprimen con prefijo [sr] para trazabilidad.
"""

import re
import unicodedata

import pandas as pd
import numpy as np

TARGET = "Processed WB (liters)"

# Utilidad interna

def _sanitize_names(columns) -> dict[str, str]:
    """
    Convierte nombres de columnas a identificadores válidos para PySR
    (solo ASCII alfanumérico + guión bajo).

    Pasos:
    1. Strip espacios externos.
    2. Cambiar Unicode -> ASCII
    3. Sustituir cualquier char no-[a-zA-Z0-9_] por _.
    4. Colapsar __ consecutivos; quitar _ extremos.
    5. Prefijo 'x' si el nombre empieza con dígito.
    6. Desambiguar colisiones añadiendo sufijo _1, _2, ...

    Returns:
    - dict  {nombre_original: nombre_sanitizado}
    """
    from collections import Counter

    def _clean(name: str) -> str:
        s = name.strip()
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        s = re.sub(r"[^a-zA-Z0-9_]", "_", s)
        s = re.sub(r"_+", "_", s).strip("_")
        if s and s[0].isdigit():
            s = "x" + s
        return s or "var"

    raw   = list(columns)
    clean = [_clean(c) for c in raw]

    counts = Counter(clean)
    seen: dict[str, int] = {}
    result = []
    for c in clean:
        if counts[c] > 1:
            seen[c] = seen.get(c, 0) + 1
            result.append(f"{c}_{seen[c]}")
        else:
            result.append(c)

    return dict(zip(raw, result))


# Columnas redundantes identificadas en M3 (heatmap + loadings)
FEATURES_REDUNDANTES = [
    "EDAD REC",          # r=0.964 con EDAD DON
    "IMC DON",           # = PESO/TALLA²; colineal con PC1
    "PESO REC.",         # r=0.792 con PESO DON
    "PRE MNC k/µL",      # = PRE WBC × PRE MNC%; drop el derivado
    "CMV  IgM RECEPTOR", # r=1.0 con CMV IgM DONADOR
    "CMV IgG RECEPTOR",  # r=0.926 con CMV IgG DONADOR
    "ACCESO_AMO",        # variables intra-procedimiento (dominan PC5)
    "ACCESO_CATÉTER",
    "ACCESO_PUNCIÓN",
]

# 1. Preparación de features
def dropear_redundantes(X: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Elimina las features redundantes identificadas en M3.

    Parámetros
    ----------
    - X: DataFrame
        Features tras preparar_para_pca() (shape ~110 × 44).
    - verbose: bool
        Si True, imprime resumen.

    Returns
    -------
    - X_red : DataFrame
        Features sin redundancias (~110 × 35).
    """

    presentes = [c for c in FEATURES_REDUNDANTES if c in X.columns]
    ausentes  = [c for c in FEATURES_REDUNDANTES if c not in X.columns]

    X_red = X.drop(columns=presentes)

    if verbose:
        print(f"[sr] Features antes del drop : {X.shape[1]}")
        print(f"[sr] Columnas dropeadas ({len(presentes)}): {presentes}")
        if ausentes:
            print(f"[sr] Columnas no encontradas (ignoradas): {ausentes}")
        print(f"[sr] Features tras drop: {X_red.shape[1]}")

    return X_red

# 2. Split
def split_datos(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
    verbose: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Train/test split estratificado por tamaño.

    Returns
    -------
    X_train, X_test, y_train, y_test
    """

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
    )

    if verbose:
        print(f"[sr] Split 80/20 (random_state={random_state})")
        print(f"[sr] Train: {X_train.shape[0]} filas")
        print(f"[sr] Test: {X_test.shape[0]} filas")
        print(f"[sr] y_train rango: [{y_train.min():.2f}, {y_train.max():.2f}] L")
        print(f"[sr] y_test  rango: [{y_test.min():.2f}, {y_test.max():.2f}] L")

    return X_train, X_test, y_train, y_test

# 3. Regresión simbólica
def correr_sr(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    niterations: int = 50,
    populations: int = 20,
    random_state: int = 42,
    verbose: bool = True,
) -> tuple["PySRRegressor", dict[str, str]]:
    """
    Ajusta PySRRegressor sobre (X_train, y_train).

    Configuración fija:
    - Operadores: +, -, *, /  (fórmula teórica usa división)
    - Sin operadores unarios   (priorizar interpretabilidad)
    - deterministic = True + procs = 0  (reproducibilidad real)
    - model_selection="best"

    Returns
    - model:
        PySRRegressor ajustado
    """
    from pysr import PySRRegressor

    # Sanitizar nombres de columnas
    name_map   = _sanitize_names(X_train.columns)
    var_names  = [name_map[c] for c in X_train.columns]

    if verbose:
        print(f"[sr] Iniciando PySR - {niterations} iteraciones, {populations} poblaciones")
        print(f"[sr] Operadores: +  -  *  /")
        print(f"[sr] X_train shape: {X_train.shape}")
        renamed = [(o, s) for o, s in name_map.items() if o != s]
        if renamed:
            print(f"[sr] Columnas renombradas para PySR ({len(renamed)}):")
            for orig, san in renamed:
                print(f"      {orig!r} -> {san!r}")

    model = PySRRegressor(
        binary_operators=["+", "-", "*", "/"],
        unary_operators=[],
        niterations=niterations,
        populations=populations,
        model_selection="best",
        random_state=random_state,
        deterministic=True,
        parallelism="serial",
        verbosity=1 if verbose else 0,
        progress=verbose,
    )

    model.fit(X_train.values, y_train.values, variable_names=var_names)

    if verbose:
        print(f"\n[sr] PySR completado.")
        print(f"[sr] Mejor ecuación: {model.sympy()}")

    return model, name_map

# 4. Análisis del frente de Pareto
def frente_pareto(model: "PySRRegressor") -> pd.DataFrame:
    """
    Extrae el frente de Pareto (complejidad vs loss) del modelo PySR.

    Returns
    - pareto_df:
        DataFrame con columnas:
            complexity, loss, score, equation
            Ordenado de menor a mayor complejidad.
    """
    equations = model.equations_

    pareto_df = equations[["complexity", "loss", "score", "equation"]].copy()
    pareto_df = pareto_df.sort_values("complexity").reset_index(drop=True)

    return pareto_df

# 5. Baseline lineal
def baseline_lineal(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    verbose: bool = True,
) -> dict:
    """
    Ajusta LinearRegression como baseline y evalúa en test.

    Returns
    - dict con claves:
        r2      : R² en test
        rmse    : RMSE en test
        y_pred  : array de predicciones en test
        modelo  : LinearRegression ajustado
    """

    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_squared_error

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)

    r2   = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    if verbose:
        print(f"[sr] Baseline lineal - test set")
        print(f"[sr] R^2: {r2:.4f}")
        print(f"[sr] RMSE: {rmse:.4f} L")

    return {"r2": r2, "rmse": rmse, "y_pred": y_pred, "modelo": lr}

# 6. Evaluación del modelo SR
def evaluar(
    model: "PySRRegressor",
    X_test: pd.DataFrame,
    y_test: pd.Series,
    verbose: bool = True,
) -> dict:
    """
    Evalúa el modelo PySR en el test set.

    Returns
    - dict con claves:
        r2      : R^2 en test
        rmse    : RMSE en test
        y_pred  : array de predicciones en test
    """

    from sklearn.metrics import r2_score, mean_squared_error

    y_pred = model.predict(X_test.values)

    r2   = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    if verbose:
        print(f"[sr] Modelo SR - test set")
        print(f"[sr] Ecuación: {model.sympy()}")
        print(f"[sr] R^2: {r2:.4f}")
        print(f"[sr] RMSE: {rmse:.4f} L")

    return {"r2": r2, "rmse": rmse, "y_pred": y_pred}
