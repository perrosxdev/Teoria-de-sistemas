# 🥚 Propuesta de Proyecto — Dinámica de Sistemas en una Distribuidora de Huevos

## El problema y la Pregunta de Investigación

Una distribuidora de huevos de pequeña escala abastece actualmente a supermercados de la zona, restoranes locales, almacenes de población y un nuevo punto de venta reciente.

El negocio se enfrenta a una **demanda creciente de forma orgánica** a largo plazo, la cual se ve fuertemente acentuada en temporada de verano por la estacionalidad turística. Sin embargo, la **capacidad de reparto** (vehículo propio y personal de entrega) está limitada inicialmente a un valor de 720 cajas/mes.

Cuando la demanda creciente supera esta capacidad logística, se produce un cuello de botella:
1.  Los pedidos se retrasan y se generan ventas no entregadas.
2.  La insatisfacción de los clientes provoca una **pérdida de clientes (fuga/churn)**, afectando la demanda futura.
3.  La empresa debe decidir si invertir en ampliar la flota (un camión adicional por CLP 50.000.000 y costos fijos de personal).

La pregunta general de investigación que guía el modelo es:

> **¿Cuándo conviene invertir en más capacidad de reparto (vehículo y personal) y cómo afecta esta decisión a la rentabilidad del negocio en el tiempo frente a un escenario de demanda creciente?**

---

## Objetivos del Modelo (Qué busca satisfacer)

*   **Identificar el punto de colapso (Cuello de Botella):** Determinar en qué periodo exacto de la simulación la capacidad logística actual se vuelve insuficiente para cubrir los pedidos, estimando las pérdidas iniciales de clientes.
*   **Evaluar el impacto financiero de la inversión:** Simular el comportamiento de la caja (`Margen acumulado`) al introducir egresos por inversión inicial (CLP 5.000.000) y nuevos costos fijos mensuales (chofer y mantenimiento) frente al beneficio de liberar ventas retenidas.
*   **Optimizar el timing de la decisión:** Descubrir si es mejor invertir de manera **proactiva** (anticiparse al verano en el mes 6) o **reactiva** (comprar el camión cuando el colapso ya ocurrió y hay pérdida de clientes), analizando cuál estrategia recupera la inversión más rápido.
*   **Probar la resiliencia del negocio:** Modelar la ley de "límites al crecimiento" para ver cómo interactúan la satisfacción del cliente y la capacidad física de entrega, demostrando que el crecimiento indefinido de ventas es inviable sin infraestructura.

---

## Subsistemas identificados

El modelo se divide en dos subsistemas principales: el **Operacional/Logístico** (flujo de cajas y retención de clientes) y el **Financiero/Inversión** (flujos de dinero).

### 1. Subsistema 1 — Operacional / Logístico (Flujos Físicos y Demanda)

| Variable | Tipo | Unidad | Descripción |
| :--- | :---: | :---: | :--- |
| **Demanda base** | Stock | `cajas` | Nivel que acumula el volumen de demanda base (clientes estables). |
| **Stock de huevos** | Stock | `cajas` | Inventario físico acumulado en la bodega. |
| **Capacidad de reparto** | Stock | `cajas/mes` | Límite logístico mensual de transporte de mercadería. |
| **Tasa de captación** | Flujo | `cajas/mes/mes` | Incremento mensual orgánico de la demanda base. |
| **Tasa de pérdida de clientes**| Flujo | `cajas/mes/mes` | Pérdida de clientes estables debido a la insatisfacción logística. |
| **Tasa de compra** | Flujo | `cajas/mes` | Cajas adquiridas al proveedor por período. |
| **Tasa de despacho** | Flujo | `cajas/mes` | Cajas entregadas a los clientes. Limitada por la demanda, stock y capacidad. |
| **Demanda total** | Auxiliar | `cajas/mes` | Demanda base modulada por la estacionalidad del mes. |
| **Tasa de incumplimiento** | Auxiliar | `Dmnl` | Fracción de pedidos no entregados por falta de transporte. |
| **Estacionalidad** | Exógena | `Dmnl` | Multiplicador de demanda (Lookup de tiempo). |
| **Disponibilidad proveedor** | Exógena | `Dmnl` | Fracción de entrega del proveedor (0.8 en verano, 1.0 el resto del año). |

---

### 2. Subsistema 2 — Financiero / Inversión (Flujos de Dinero)

| Variable | Tipo | Unidad | Descripción |
| :--- | :---: | :---: | :--- |
| **Margen acumulado** | Stock | `CLP` | Las utilidades líquidas retenidas acumuladas en caja. |
| **Ingresos por ventas** | Flujo | `CLP/mes` | Entrada de dinero: cajas despachadas × precio de venta. |
| **Costo de compra** | Flujo | `CLP/mes` | Salida de dinero: cajas compradas × precio de compra unitario. |
| **Costos operacionales** | Flujo | `CLP/mes` | Salida de dinero por costos fijos y variables de distribución. |
| **Inversión en capacidad** | Flujo | `CLP/mes` | Desembolso de capital destinado a la compra del nuevo vehículo. |
| **Gatillo inversión** | Auxiliar | `Dmnl` | Variable lógica de decisión (política de compra reactiva vs. proactiva). |
| **Precio de venta** | Parámetro | `CLP/caja` | Valor unitario cobrado al cliente. |
| **Precio de compra** | Parámetro | `CLP/caja` | Costo unitario cobrado por el proveedor. |
| **Costo de vehículo** | Parámetro | `CLP` | Inversión necesaria para adquirir la capacidad de reparto adicional. |
| **Incremento cap por CLP** | Parámetro | `(cajas/mes)/CLP` | Factor de conversión que traduce la inversión en CLP a capacidad física de reparto. |
| **Costo fijo mantenimiento** | Parámetro | `CLP/caja/mes` | Incremento del costo fijo mensual por unidad de capacidad agregada (salarios, mantención). |

---

## Bucles de Retroalimentación Clave

1.  **Bucle R1 — Crecimiento por Inversión (Refuerzo Virtuoso):**
    $$\text{Margen acumulado} \rightarrow \text{Gatillo inversión} \rightarrow \text{Inversión en capacidad} \rightarrow \text{Capacidad de reparto} \rightarrow \text{Tasa de despacho} \rightarrow \text{Ingresos} \rightarrow \text{Margen acumulado}$$
    La acumulación de caja permite financiar camiones nuevos, aumentando la capacidad logística de entrega, incrementando los ingresos y expandiendo el margen acumulado futuro.
2.  **Bucle B1 — Límite Físico de Despacho (Balanceo):**
    $$\text{Stock de huevos} \rightarrow \text{Tasa de despacho} \rightarrow \text{Stock de huevos}$$
    El despacho consume stock de bodega. La capacidad de reparto actúa como techo que trunca el despacho real.
3.  **Bucle B3 — Destrucción de Demanda por Colapso (Balanceo de Reputación):**
    $$\text{Demanda total} \rightarrow \text{Tasa de incumplimiento} \rightarrow \text{Tasa de pérdida de clientes} \rightarrow \text{Demanda base} \rightarrow \text{Demanda total}$$
    Si la demanda excede la capacidad de reparto, se acumulan pedidos no despachados. Esto eleva la tasa de incumplimiento, destruyendo la satisfacción de los clientes, acelerando la fuga de clientes estables y reduciendo la demanda en periodos posteriores.

---

## Escenarios de Simulación

El modelo evalúa el **timing de la inversión** comparando tres escenarios en base a una demanda que crece orgánicamente un 2% mensual:

1.  **Escenario Base (Sin Inversión):** La distribuidora mantiene su capacidad fija (720 cajas/mes). Al llegar el verano del mes 12, el colapso logístico es total, provocando una masiva pérdida de clientes y estancando las ganancias a largo plazo.
2.  **Escenario Futuro A (Inversión Reactiva):** La distribuidora compra el vehículo (CLP 50.000.000) solo cuando ha acumulado la caja necesaria y la tasa de incumplimiento supera el 10% de forma instantánea. El negocio sufre pérdidas de clientes previas antes de recuperar su capacidad de entrega.
3.  **Escenario Futuro B (Inversión Proactiva):** La distribuidora compra el vehículo de forma anticipada en el mes 8 (antes del verano y del colapso), recurriendo a crédito de capital de trabajo si la caja propia no es suficiente, protegiendo al 100% la base de clientes.
