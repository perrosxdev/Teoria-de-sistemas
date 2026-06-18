# Guía de Preparación: Evaluación de Avance Vensim (Viernes 19 de Junio)
## Enfoque en Timing de Inversión y Demanda Creciente

Esta guía de interrogación te ayudará a ti y a tu grupo a defender con éxito el avance del modelo ante las preguntas específicas detalladas en el correo de evaluación.

---

## 1. Ficha Técnica de la Distribuidora (Definiciones Clave)

| Concepto | Lo que debes decir |
| :--- | :--- |
| **Pregunta de Investigación** | *¿Cuándo conviene invertir en más capacidad de reparto (vehículo y personal) y cómo afecta esta decisión a la rentabilidad del negocio en el tiempo frente a un escenario de demanda creciente?* |
| **Problemática Identificada** | Un **cuello de botella logístico** dinámico:<br>1. **Demanda Creciente (+):** La demanda base crece orgánicamente a una tasa del 2% mensual, sumada a un peak estival en verano (Enero y Febrero) donde la demanda se duplica.<br>2. **Colapso y Fuga de Clientes:** La capacidad actual de reparto (867 cajas/mes) se vuelve insuficiente en temporada alta. Los despachos fallidos generan una **Tasa de incumplimiento** que activa la **fuga (pérdida) de clientes estables**, destruyendo la demanda futura.<br>3. **Dilema de Costos:** Expandir la flota (CLP 5.000.000) añade nuevos costos fijos operativos mensuales (chofer y mantenimiento), los cuales se vuelven pesados en invierno cuando hay capacidad ociosa. |
| **Variable Principal** | **Capacidad de reparto** (Nivel - unidades: `cajas/mes`). Límite físico de entrega. |
| **Subsistemas (2)** | **1. Logístico/Operacional:** Flujos de inventario, demanda creciente y fuga de clientes (cajas).<br>**2. Financiero/Inversión:** Flujos de utilidades líquidas (`Margen acumulado`) en CLP e inversión en flota. |

---

## 2. Guión de Defensa ante las Preguntas del Profesor

### ❓ Pregunta 1: "¿Cuál es su pregunta de investigación y su variable principal?"
*   **Respuesta sugerida:**
    > "Nuestra pregunta de investigación es: *¿Cuándo conviene invertir en más capacidad de reparto y cómo afecta esta decisión a la rentabilidad del negocio en el tiempo frente a un escenario de demanda creciente?*
    > Nuestra variable principal es la **Capacidad de reparto** (medida en `cajas/mes`). Es la variable central porque representa el límite físico logístico del negocio: si la demanda orgánica creciente choca con esta capacidad fija, se generan quiebres en el servicio que ahuyentan permanentemente a los clientes."

---

### ❓ Pregunta 2: "¿Cómo busca el modelo identificar el punto de colapso y qué consecuencias tiene?"
*   **Respuesta sugerida:**
    > "Identificamos el colapso a través de la **Tasa de incumplimiento** (pedidos no entregados sobre la demanda total). El modelo detecta el mes exacto del verano en el cual la demanda excede las 867 cajas/mes de capacidad. 
    > Las consecuencias están modeladas mediante un bucle de retroalimentación negativo: el incumplimiento alimenta la **Tasa de pérdida de clientes**, lo que drena directamente el stock de **Demanda base** para los periodos siguientes. Así simulamos que dar un mal servicio debido a una logística saturada destruye la base de clientes estable del negocio."

---

### ❓ Pregunta 3: "¿Cómo modelaron la comparación de políticas (Proactiva vs. Reactiva) y el timing?"
*   **Respuesta sugerida:**
    > "Modelamos el timing de inversión en la variable **Gatillo inversión** usando una condición que evalúa la variable `Política proactiva`:
    > *   **Política Reactiva (Base):** El camión se compra solo cuando ya colapsó el sistema (Tasa de incumplimiento > 10%) y se ha acumulado la caja. Esto resulta en una pérdida de reputación de la cual el negocio tarda meses en recuperarse.
    > *   **Política Proactiva (Mejora):** El camión se compra de forma anticipada en el mes 6 (antes de la temporada alta de verano) para blindar el servicio y evitar por completo la fuga de clientes.
    > El modelo nos permite comparar en las gráficas temporales cuál estrategia recupera el capital invertido más rápido y genera mayor acumulación neta al mes 12."

---

### ❓ Pregunta 4: "¿Cuáles son los Niveles, Flujos y Auxiliares de su modelo?"
*   **Respuesta sugerida:**
    > "Para mantener la consistencia dimensional con un paso de tiempo mensual (`meses`), definimos:
    > *   **Niveles (Stocks):** `Demanda base` (cajas/mes), `Stock de huevos` (cajas), `Capacidad de reparto` (cajas/mes) y `Margen acumulado` (CLP).
    > *   **Flujos (Rates):** `Tasa de captacion` y `Tasa de perdida de clientes` (cajas/mes/mes), `Tasa de compra` y `Tasa de despacho` (cajas/mes) y los flujos financieros en `CLP/mes`.
    > *   **Auxiliares y Constantes:** `Tasa de incumplimiento`, `Tasa crecimiento base` (0.02), `Precio de venta` (11.500 CLP/caja), `Costo de vehículo` (5.000.000 CLP), `Costo fijo mantenimiento` (200 CLP/caja/mes) y Lookups de `Estacionalidad` y `Disponibilidad proveedor`."

---

### ❓ Pregunta 5: "¿Qué datos históricos usaron para respaldar el modelo?"
*   **Respuesta sugerida:**
    > "Utilizamos los **registros reales del año 2025** (Ventas con IVA: CLP 91.157.157, Compras: CLP 76.990.643 y Ganancia líquida: CLP 11.904.633). 
    > Calibramos las ventas históricas de 2025 para calcular el promedio mensual y normalizar cada mes, generando el Lookup de `Estacionalidad` (donde Enero y Febrero multiplican la demanda por 1.84). 
    > También usamos la ganancia neta real acumulada al mes 12 (CLP 11.904.633) para validar que el escenario base simule correctamente las finanzas reales del negocio antes de proyectar la compra de flota."

---

## 3. Checklist Técnico de Vensim para el Grupo (Antes de Exponer)

1.  **Units Check:** Ejecuta `Model -> Units Check`. Debe indicar *"Units are A.O.K."*.
2.  **Model Check:** Ejecuta `Model -> Check Model` para confirmar que las fórmulas no tengan errores.
3.  **Configuración de Tiempo:** `INITIAL TIME = 1`, `FINAL TIME = 12`, `TIME STEP = 1`, unidad: `Month`.
4.  **Tres Corridas Guardadas:** Ejecuta y guarda tres simulaciones en Vensim:
    *   `Base` (sin inversión: `Politica_proactiva = 0` y `Costo_de_vehiculo` inaccesible).
    *   `Reactiva` (`Politica_proactiva = 0` y compra de camión automática tras colapso).
    *   `Proactiva` (`Politica_proactiva = 1` y compra en el mes 6).
5.  **Gráfico Comparativo:** Prepara una gráfica de `Margen acumulado` y otra de `Demanda base` donde se superpongan las tres corridas. Esto mostrará visualmente el costo de la inacción (Base), el retraso en la recuperación (Reactivo) y el beneficio de la prevención (Proactivo).
