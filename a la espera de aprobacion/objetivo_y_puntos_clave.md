# Objetivo del Modelo y Puntos Claves: Crecimiento y Timing de Inversión

Este documento detalla qué busca resolver el modelo de simulación en Vensim (enfoque de Capacidad de Reparto con Demanda Creciente) y cuáles son las palancas de decisión, dinámica sistémica y objetivos de la pauta.

---

## 1. ¿Qué busca satisfacer (Objetivos del Modelo)?

El modelo en Vensim responde a la pregunta de investigación analizando cinco dimensiones clave del comportamiento del sistema:

### A. Identificar el punto de colapso (Cuello de Botella)
*   **Objetivo:** Determinar en qué momento exacto del tiempo (mes/semana) la capacidad de reparto actual (867 cajas/mes) es superada por el crecimiento orgánico de la demanda más la estacionalidad veraniega.
*   **Dinámica:** Se mide a través de la variable `Tasa de incumplimiento` (pedidos no entregados / demanda total). El punto de colapso ocurre cuando esta tasa es mayor a cero, generando retrasos y gatillando la pérdida de clientes.

### B. Evaluar el impacto financiero de la inversión
*   **Objetivo:** Simular la liquidez de caja (`Margen acumulado`) al introducir la salida de capital inicial (CLP 5.000.000) y los nuevos costos fijos operacionales (salarios de chofer, seguros y mantenimiento mensual) versus el flujo de ingresos recuperado al liberar las ventas retenidas.

### C. Optimizar el timing de la decisión (Proactivo vs. Reactivo)
*   **Objetivo:** Evaluar dos políticas de inversión:
    *   **Política Reactiva (Estado Actual):** Se invierte solo cuando hay pérdidas reales de clientes y se ha acumulado la caja necesaria.
    *   **Política Proactiva (Estado Futuro):** Se invierte anticipadamente en el mes 6 (antes de la temporada de verano), usando financiamiento externo si es necesario, para evitar que la insatisfacción del cliente se active.
*   **Resultado:** Comparar en las gráficas temporales cuál de las dos estrategias recupera la inversión más rápido y acumula mayor capital al final de la simulación.

### D. Probar la resiliencia del negocio (Límite Físico de Crecimiento)
*   **Objetivo:** Mostrar la interacción entre satisfacción del cliente, demanda y capacidad de reparto. Demuestra la ley sistémica de "límites al crecimiento": el negocio no puede crecer infinitamente en ventas sin expandir su infraestructura física, ya que la incapacidad logística destruye la reputación y ahuyenta la demanda.

---

## 2. Estructura de Bucles Causales Clave

1.  **Bucle de Refuerzo R1 (Crecimiento por Inversión):**
    $$\text{Margen acumulado} \rightarrow \text{Inversión} \rightarrow \text{Capacidad de reparto} \rightarrow \text{Tasa de despacho} \rightarrow \text{Ingresos} \rightarrow \text{Margen acumulado}$$
2.  **Bucle de Balanceo B1 (Límite Logístico):**
    $$\text{Stock de huevos} \rightarrow \text{Tasa de despacho} \rightarrow \text{Stock de huevos}$$
3.  **Bucle de Balanceo B3 (Destrucción de Demanda por Colapso):**
    $$\text{Demanda} \rightarrow \text{Tasa de incumplimiento} \rightarrow \text{Pérdida de clientes} \rightarrow \text{Demanda}$$
    Si la demanda excede la capacidad de reparto, se acumulan retrasos y pedidos perdidos. Esto eleva la tasa de incumplimiento, aumentando la fuga de clientes y reduciendo la demanda en los meses siguientes.

---

## 3. Claves para la Defensa ante el Profesor

*   **Defensa del timing:** Justifica ante el profesor que la compra de camiones proactiva (antes de que colapse el sistema) protege la base de clientes activos, mientras que la compra reactiva resulta en una pérdida de prestigio de la cual el negocio tarda meses en recuperarse.
*   **El dilema de los costos fijos:** Explica que el modelo muestra con realismo que añadir capacidad de reparto aumenta el costo fijo de operación mensual del negocio (sueldo del conductor adicional), por lo que si la demanda no crece lo suficiente en invierno, el nuevo camión puede reducir el margen mensual neto fuera de temporada.
