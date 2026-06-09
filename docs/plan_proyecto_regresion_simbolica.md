# Plan — Regresión simbólica para predecir WB (aféresis CD34+)

**Meta:** obtener una **fórmula explicable** que prediga WB (volumen de sangre a procesar). Herramienta: **PySR**. Fitness: **R²**.

**Entregable actual (reunión 2):** demo completo con PCA + regresión simbólica sobre los datos reales → M1 (validación) + M2 + M3 + M4.

---

## Reglas fijas (no olvidar)

- **Target (ŷ) = WB.** Nunca va en X.
- **Leakage:** fuera de X todo lo que contenga WB en su definición → `CE2%`, `COSECHA *`, `POST *`. Se quita **a mano y antes del PCA**.
- **Features redundantes legítimas** (PESO, TALLA, IMC, VOLEMIA...): NO se curan a mano → eso lo hace el PCA.
- **Orden:** M1 → M2 → M3 → M4.

---

## M1 · PoC con PySR (datos sintéticos) — sección de validación del demo

**Objetivo:** abrir el demo mostrando que PySR recupera una fórmula conocida. Da credibilidad antes de pasar a los datos reales.

1. Elegir una fórmula conocida, ej. `y = 2x² - 3x + 1`.
2. Generar datos: `X` aleatorio en un rango, `y = f(X)` (+ opcional ruido pequeño).
3. Instalar y configurar PySR (instala Julia en el primer uso).
4. Correr `PySRRegressor` con operadores básicos (`+, -, *, /`) y `model_selection="best"`.
5. Revisar que la fórmula encontrada ≈ la original.

**Salida:** notebook PySR funcionando.

---

## M2 · Preparación de datos

**Objetivo:** dejar un `df_clean` limpio, sin tocar la información real.

1. Cargar **`Hoja1`** (header en fila correcta). NO usar `R. TRIMESTRAL` (sus 74 folios ya están en Hoja1, 0 únicos → solo duplicaría filas).
2. Quitar filas vacías (sin `FOLIO`).
3. **Parsear numéricos** (no altera información):
   - Texto-que-es-número → número.
   - `***` y `SD` → `NaN` (significan "no medido"; marcar ausencia no es alterar).
   - Tokens censurados (`>250`, `NEGATIVO`, `C`) viven en columnas CMV/typo que no se usan → ignorar.
4. **Quitar columnas de leakage:** `CE2% *`, `COSECHA *`, `POST *`, y outcomes post-trasplante (EICH, muerte, recuperación).
5. Elegir la columna WB como `y` (probable: `Processed WB (liters)`) y sacarla de X.
6. Encoding de categóricas legítimas (TIPO, SEXO, ESTIMULACIÓN) → numérico.
7. NO podar features legítimas a mano (eso lo decide el PCA en M3).

**Salida:** `df_clean` (X = features pre-procedimiento + `y`) + diccionario de variables.

---

## M3 · PCA

**Objetivo:** entender redundancia/multicolinealidad y guiar qué variables conservar.

1. Estandarizar X (z-score). PCA es sensible a escala → obligatorio.
2. Manejar los pocos `NaN` que queden: borrar esas ~2-3 filas incompletas (no imputar → no inventar valores).
3. Correr PCA.
4. Graficar: scree plot + varianza explicada acumulada.
5. Revisar **loadings** (qué variables originales pesan en cada componente) y biplot.
6. Interpretar componentes y anotar qué features son redundantes.

**Salida:** decisión justificada de qué variables originales pasan a M4.
**Nota:** la SR corre sobre **variables originales**, no sobre PCs (los PCs rompen la interpretabilidad).

---

## M4 · SR sobre datos reales (PySR)

**Objetivo:** la fórmula final para WB.

1. Tomar X (guiada por M3) y `y = WB`.
2. Split train/test (n≈116 → cuidar overfitting).
3. Correr `PySRRegressor`: operadores `+, -, *, /` (la fórmula teórica usa división), opcional `sqrt, log`.
4. Revisar el **frente de Pareto** (complejidad vs error) y elegir fórmula simple + buen R².
5. Comparar contra baselines: regresión lineal y fórmula teórica (diapositiva 19).
6. Graficar: predicho vs real, residuales.

**Salida:** fórmula + R² + comparación.

---

## M5 · Producto final (a futuro)

Función validada → generar datos nuevos → borrador de artículo.

---

## Pendientes por confirmar (Anastacio / Cordero)

- ¿Cuál columna de WB es la etiqueta? (probable: `Processed WB (liters)`)
- ¿Existe columna de "dosis CD34+ deseada"? Sin ella el modelo es descriptivo, no de dosis.
- Significado de varias variables (el profe no está seguro).

---

## Stack

Python · PySR (SR) · pandas/numpy · scikit-learn (PCA, escalado) · matplotlib · Jupyter.
