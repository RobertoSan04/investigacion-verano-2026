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

