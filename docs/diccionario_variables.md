# Diccionario de Variables — M2 Preparación de Datos

Dataset: `2025_CPH_2_xlsx_final.xlsx` · Hoja: `Hoja1` · Filas válidas: 116 · Columnas originales: 91

**Leyenda de estado:**
- `X` — feature en el modelo
- `y` — variable target
- `drop` — eliminada (motivo indicado)

---

## Features en X (45 columnas post-encoding)

### Datos del donador

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `SEXO DON` | `SEXO DON` | binaria | 0–1 | 0 | Sexo del donador. M=1, F=0 |
| `EDAD DON ` | `EDAD DON ` | float | 1–73 | 0 | Edad del donador en años |
| `PESO DON` | `PESO DON` | float | 9.6–140.0 | 0 | Peso del donador en kg |
| `TALLA DON` | `TALLA DON` | float | 0.82–1.96 | 0 | Talla del donador en metros |
| `IMC DON` | `IMC DON` | float | 13.4–45.3 | 0 | Índice de masa corporal del donador |
| `GPO ABO DONADOR` | `ABO_DON_A/AB/B/O` | one-hot | 0–1 | 0 | Grupo sanguíneo ABO del donador |
| ` RH DONADOR` | ` RH DONADOR` | binaria | 0–1 | 0 | Factor Rh del donador. POSITIVO=1, NEGATIVO=0 |
| `CMV  IgM DONADOR` | `CMV  IgM DONADOR` | float | 0.0–2.15 | 0 | Título de anticuerpos IgM contra CMV del donador. NEGATIVO=0, número=título |
| `CMV IgG DONADOR` | `CMV IgG DONADOR` | float | 0.0–250.0 | 0 | Título de anticuerpos IgG contra CMV del donador. NEGATIVO=0, >250→250.0 (positivo título alto) |

### Datos del receptor

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `EDAD REC` | `EDAD REC` | float | 5–73 | 0 | Edad del receptor en años |
| `PESO REC.` | `PESO REC.` | float | 18.0–133.0 | 0 | Peso del receptor en kg |
| `GPO ABO RECEPTOR` | `ABO_REC_A/AB/B/O` | one-hot | 0–1 | 1 | Grupo sanguíneo ABO del receptor. A/O (1 caso ambiguo) → NaN |
| ` RH RECEPTOR` | ` RH RECEPTOR` | binaria | 0–1 | 0 | Factor Rh del receptor. POSITIVO=1, NEGATIVO=0 |
| `CMV  IgM RECEPTOR` | `CMV  IgM RECEPTOR` | float | 0.0–7.4 | 1 | Título IgM contra CMV del receptor |
| `CMV IgG RECEPTOR` | `CMV IgG RECEPTOR` | float | 0.0–250.0 | 1 | Título IgG contra CMV del receptor |

### Tipo de trasplante

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `TIPO` | `TIPO_AUTÓLOGO` `TIPO_ALOGÉNICO` `TIPO_HAPLOIDÉNTICO` | one-hot | 0–1 | 0 | Tipo de trasplante. IDÉNTICO (1 caso) agrupado en ALOGÉNICO |

### Protocolo de estimulación con G-CSF

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `ESTIMULACIÓN` | `ESTIMULACION_PEGILADO` | binaria | 0–1 | 0 | Tipo de G-CSF: 0=estándar (filgrastim y biosimilares), 1=filgrastim pegilado |
| `DOSIS DE G-CSF` | `DOSIS DE          G-CSF` | float | 6–18000 | 0 | Dosis de G-CSF administrada (µg) |
| `DÍAS DE G-CSF` | `DÍAS DE          G-CSF` | float | 1–9 | 0 | Días de estimulación con G-CSF |
| `DOSIS PLERIXAFOR mg/kg` | `PLERIXAFOR_DADO` | binaria | 0–1 | 0 | 1 si se administró plerixafor, 0 si no |

### CD34+ durante estimulación (pre-aféresis)

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `CD34+ /µL DÍA 4` | `CD34+ /µL DÍA 4` | float | 0.9–159.1 | 41 | Células CD34+ en sangre periférica el día 4 de estimulación |
| `CD34+ /µL DÍA 5` | `CD34+ /µL DÍA 5` | float | 6.0–224.6 | 4 | Células CD34+ en sangre periférica el día 5 de estimulación |

### Hemograma pre-aféresis del donador

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `PRE WBC  k/µL ` | `PRE WBC  k/µL ` | float | 1.02–91.34 | 2 | Leucocitos totales pre-procedimiento |
| `PRE MNC%` | `PRE MNC%` | float | 9.9–68.0 | 2 | Porcentaje de células mononucleares pre-procedimiento |
| `PRE MNC k/µL` | `PRE MNC k/µL` | float | 0.47–18.99 | 2 | Células mononucleares absolutas pre-procedimiento |
| `PRE HTO %` | `PRE HTO %` | float | 24.7–64.9 | 2 | Hematocrito pre-procedimiento (%) |
| `PRE PLT k/μL` | `PRE PLT k/μL` | float | 16.0–349.0 | 2 | Plaquetas pre-procedimiento |

### Configuración del procedimiento

| Columna original | Columna en X | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `VOLEMIA mL` | `VOLEMIA mL` | float | 720–7286 | 3 | Volemia estimada del donador en mL |
| `CEBADO` | `CEBADO` | binaria | 0–1 | 2 | Si se realizó cebado del circuito. SI=1, NO=0 |
| `DESECHABLE ` | `DESECHABLE` | binaria | 0–1 | 0 | Tipo de desechable: IDL=1, otro=0 |
| `MAQUINA ` | `MAQUINA_EMT-25` `MAQUINA_EMT-50` `MAQUINA_EMT-68` | one-hot | 0–1 | 2 | Máquina de aféresis utilizada. ***→NaN |
| `ACCESO` | `ACCESO_CATÉTER` `ACCESO_PUNCIÓN` `ACCESO_AMO` | one-hot | 0–1 | 0 | Tipo de acceso vascular |
| `EVENTOS ADV EN PROCESO` | `EVENTO_ADV` | binaria | 0–1 | 0 | Si ocurrió algún evento adverso durante el procedimiento. NINGUNO=0, cualquier evento=1 |

---

## Target y

| Columna original | Columna en y | Tipo | Rango | NaN | Descripción |
|---|---|---|---|---|---|
| `Processed WB (liters)` | `Processed WB (liters)` | float | 3.416–28.908 L | 3 | Volumen de sangre total procesada en litros durante la aféresis |

---

## Columnas eliminadas

### IDs y texto libre (13)

| Columna | Motivo |
|---|---|
| `FECHA` | Fecha del procedimiento — ID temporal |
| `FOLIO` | Identificador del paciente |
| `DONADOR` | Nombre del donador — texto libre |
| `RECEPTOR` | Nombre del receptor — texto libre |
| `DX` | Diagnóstico — texto libre, alta cardinalidad |
| `NO. DE RECOLECCIÓN` | Número de aféresis del paciente — no predice WB |
| `CULTIVO M.` | Cultivo microbiológico — texto libre |
| `PROCEDENCIA` | Procedencia del paciente — texto libre |
| `FECHA DE TRASPLANTE` | Fecha post-procedimiento |
| `LUGAR DE INFUSIÓN` | Lugar de infusión — texto libre |
| `OBSERVACIONES` | Notas clínicas — texto libre |
| `SITIO AFECTADO` | Sitio afectado por la enfermedad — texto libre |
| `HCT-Cie` | Código de clasificación — texto libre |

### Leakage directo — derivadas matemáticamente de WB (9)

| Columna | Motivo |
|---|---|
| `VOL. SANGUÍNEO PROCESADO mL` | = Processed WB (liters) × 1000. Correlación 1.0 con y |
| `VOL. TOTAL PROCESADO mL` | = VOL. SANGUÍNEO + ACD. Depende directamente de WB |
| `VOLEMIAS PROCESADAS` | = WB / VOLEMIA. Derivada de WB |
| `ACD TOT` | Anticoagulante proporcional al volumen procesado |
| `VOL. PRODUCTO` | Volumen del producto recolectado (función de WB) |
| `VOLUMEN CALCULADO` | Calculado junto con WB en el protocolo |
| `CE2% CD34+` | = CD34+ cosechados / CD34+ procesados × 100. Denominador depende de WB |
| `CE2% MNC` | Análogo para células mononucleares |
| `% DE PÉRDIDA PLAQUETARIA` | Calculada sobre el producto post-procedimiento |

### Leakage temporal — medidas durante/después del procedimiento (22)

| Columna | Motivo |
|---|---|
| `TIEMPO MIN.` | Duración total del procedimiento — conocida solo al terminar |
| `VEL. INICIAL mL/min` | Velocidad de flujo inicial — intra-procedimiento |
| `VEL. MEDIANA mL/min` | Velocidad mediana — intra-procedimiento |
| `VEL. FINAL mL/min` | Velocidad final — intra-procedimiento |
| `COSECHA WBC k/µL` | Hemograma del producto cosechado — post-procedimiento |
| `COSECHA  MNC%` | % MNC en producto cosechado — post-procedimiento |
| `COSECHA MNC k/µL` | MNC absolutas en producto cosechado — post-procedimiento |
| ` COSECHA CMN X10^9/ VOL TOTAL` | CMN totales en producto — post-procedimiento |
| `COSECHA HTO %` | Hematocrito del producto cosechado — post-procedimiento |
| `COSECHA RBC x10⁶/µL` | Eritrocitos en producto cosechado — post-procedimiento |
| `COSECHA PLT k/µL ` | Plaquetas en producto cosechado — post-procedimiento |
| `COSECHA    CD34+/µL` | CD34+ en producto cosechado — post-procedimiento |
| `COSECHA CD34+TOTAL` | CD34+ totales cosechados — post-procedimiento |
| `COSECHA     CD34+ x10⁶/kg` | CD34+ por kg de peso — post-procedimiento |
| `COSECHA CD45+/μL` | CD45+ en producto cosechado — post-procedimiento |
| `VIABILIDAD %` | Viabilidad celular del producto — post-procedimiento |
| `POST WBC k/µL` | Leucocitos del donador post-procedimiento |
| `POST MNC %` | % MNC del donador post-procedimiento |
| `POST MNC k/µL` | MNC absolutas del donador post-procedimiento |
| `POST HTO %` | Hematocrito del donador post-procedimiento |
| `POST  PLT k/µL ` | Plaquetas del donador post-procedimiento |
| `POST CD34+/µL ` | CD34+ del donador post-procedimiento |

### Outcomes post-trasplante (13)

| Columna | Motivo |
|---|---|
| `CD34+/kg TRASPLANTE` | Dosis de CD34+ infundida al receptor — post-aféresis |
| `CD34+/kg CRIO` | CD34+ por kg después de criopreservación — post-aféresis |
| `VIAB CRIO %` | Viabilidad post-criopreservación — post-aféresis |
| `REC MIELOIDE` | Días hasta recuperación mieloide — semanas post-trasplante |
| `REC PLAQ` | Días hasta recuperación plaquetaria — semanas post-trasplante |
| `EICH AGUDO` | Enfermedad injerto contra huésped aguda — meses post-trasplante |
| `EICH CRONICO` | Enfermedad injerto contra huésped crónica — meses post-trasplante |
| `MORBILIDADES PRETRASPLANTE` | Comorbilidades previas al trasplante |
| `COMPLICACIONES` | Complicaciones post-trasplante — texto libre |
| `INFECCIONES ESPECÍFICAS` | Infecciones post-trasplante — texto libre |
| `MUERTE EN PRIMEROS 100 DÍAS` | Outcome clínico post-trasplante |
| `MUERTE EN PRIMER AÑO` | Outcome clínico post-trasplante |
| `MUERTE RELACIONADA AL TRASPLANTE` | Outcome clínico post-trasplante |
