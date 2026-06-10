# Regresión simbólica para predecir volumen de sangre en aféresis CD34+

Proyecto de investigación de verano 2026 — UANL FCFM

## Objetivo

Derivar una fórmula explícita e interpretable que prediga el **volumen de sangre total a procesar (WB, litros)** durante una aféresis de células CD34+, usando regresión simbólica (PySR) sobre datos clínicos reales.

## Resultado principal

PySR encontró la siguiente fórmula (complejidad 9, frente de Pareto):

$$WB = \text{Talla donador} \times \left[(\text{Peso donador} - \text{CD34}^+/\mu L\ \text{día 5}) \times 0.040 + 9.351\right]$$

| Modelo | R² (test) | RMSE (L) |
|---|---|---|
| Regresión lineal (baseline) | 0.567 | 4.43 |
| PySR — complejidad 9 | 0.526 | 4.63 |

El valor del modelo SR no es el R² absoluto sino la **interpretabilidad**: 3 variables clínicas con sentido biológico directo vs. 35 coeficientes opacos. Ver limitaciones en `notebooks/M4_symbolic_regression.ipynb`.

## Pipeline

```
M1 → M2 → M3 → M4
```

| Milestone | Notebook | Descripción |
|---|---|---|
| M1 | `notebooks/M1_poc_synthetic.ipynb` | PoC: PySR recupera `y = 2x² - 3x + 1` con datos sintéticos |
| M2 | `notebooks/M2_data_prep.ipynb` | Limpieza, parseo numérico, eliminación de leakage, encoding |
| M3 | `notebooks/M3_pca.ipynb` | PCA: heatmap de correlación, scree plot, decisión de features |
| M4 | `notebooks/M4_symbolic_regression.ipynb` | SR sobre datos reales, frente de Pareto, comparación de modelos, robustez |

## Estructura

```
.
├── notebooks/          # Un notebook por milestone (correr en orden)
├── src/
│   ├── m2_data_prep/   # loader, cleaning, leakage, encoding
│   ├── pca_analysis.py
│   └── symbolic_regression.py
├── docs/
│   ├── plan_proyecto_regresion_simbolica.md
│   └── diccionario_variables.md   # 45 features + target + columnas eliminadas
├── pyproject.toml
└── uv.lock
```

> `data/` y `outputs/` están en `.gitignore` - los datos clínicos no se versionan.

## Cómo correr

**Requisitos:** Python ≥ 3.14, [uv](https://docs.astral.sh/uv/), Julia (PySR la instala automáticamente en el primer uso).

```bash
git clone https://github.com/RobertoSan04/investigacion-verano-2026.git
cd investigacion-verano-2026
uv sync
```

Coloca el archivo de datos en `data/raw/2025_CPH_2_xlsx_final.xlsx`, luego corre los notebooks **en orden** desde Jupyter:

```bash
uv run jupyter notebook
```

## Dataset

116 procedimientos de aféresis CD34+ del Hospital Universitario (2025).  
Hoja: `Hoja1`. Target: `Processed WB (liters)`.  
Ver `docs/diccionario_variables.md` para descripción completa de las 91 columnas originales.

## Dependencias principales

- [PySR](https://github.com/MilesCranmer/PySR) — regresión simbólica
- pandas, scikit-learn, matplotlib