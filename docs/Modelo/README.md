# Modelo de Simulación — Distribuidora de Huevos
**Herramienta:** Vensim (archivo `Modelo.mdl`)
**Horizonte de simulación:** 96 meses (8 años)
**Paso de tiempo:** 1 mes

---

## Descripción del sistema

Este modelo de Dinámica de Sistemas representa el comportamiento operacional y financiero de una distribuidora de huevos. El problema central que se modela es la tensión entre la capacidad de reparto limitada y una demanda creciente con estacionalidad: cuando la empresa no puede despachar todo lo que los clientes demandan, pierde clientes, lo que deteriora el negocio a largo plazo. La decisión de invertir en un camión adicional busca resolver esta presión.

El modelo responde tres preguntas clave:

- ¿Cuándo y bajo qué condiciones conviene comprar un camión adicional?
- ¿Cuánto aporta realmente el camión al negocio una vez comprado?
- ¿Qué ocurre con la demanda y los ingresos si no se expande la capacidad?

---

## Cumplimiento de requisitos mínimos

| Requisito | Cantidad mínima | Presente en el modelo |
|---|---|---|
| Subsistemas | 2 | ✅ 4 subsistemas |
| Variables totales | 10 | ✅ 43 variables |
| Stocks / niveles | 2 | ✅ 6 stocks |
| Flujos | 2 | ✅ 8 flujos |
| Variables auxiliares / parámetros | 2 | ✅ 29 auxiliares y parámetros |
| Bucles de retroalimentación | 1 | ✅ 4 bucles (B1, B2, B3, R1) |
| Escenarios comparables | 2 | ✅ 3 escenarios (base, reactivo, proactivo) |

---

## Subsistemas

El modelo se organiza en cuatro subsistemas interconectados.

### Subsistema 1 — Demanda de clientes

Modela la evolución de la cartera de clientes del negocio. La demanda puede crecer mediante captación de nuevos clientes, o contraerse cuando el negocio no cumple con los pedidos.

**Stocks:**
- `Demanda Base` — nivel de demanda mensual sostenida por los clientes actuales (inicial: 700 cajas/mes)

**Flujos:**
- `Tasa de captacion` — clientes nuevos que se incorporan cada mes
- `Tasa de perdida de clientes` — clientes que se van por incumplimiento logístico

**Variables auxiliares y parámetros clave:**

| Variable | Unidad | Función | Fuente / supuesto |
|---|---|---|---|
| `Demanda total` | Caja/Month | Demanda real ajustada por estacionalidad | `Demanda Base × Estacionalidad` |
| `Estacionalidad` | Dmnl | Factor multiplicador mensual de la demanda | Calibrado con datos reales de ventas 2025 del negocio |
| `Tasa de crecimiento base` | 1/Month | Velocidad de captación orgánica | Supuesto: 2% mensual (crecimiento moderado) |
| `Mercado potencial` | Caja/Month | Techo máximo de demanda alcanzable en la zona | Supuesto: 1.200 cajas/mes, estimado de la demanda del sector |
| `Fraccion de mercado Disponible` | Dmnl | Porción del mercado aún no capturada | `(Mercado potencial − Demanda Base) / Mercado potencial` |
| `Clientes potenciales Restantes` | Caja/Month | Demanda no satisfecha del mercado disponible | `MAX(0, Mercado potencial − Demanda Base)` |
| `Tasa de incumplimiento` | Dmnl | Fracción de la demanda total que no se pudo despachar | `MAX(0, (Demanda total − Tasa de despacho) / Demanda total)` |
| `Tasa de fuga logistica` | Dmnl | Proporción de clientes que se pierden según el incumplimiento | Tabla lookup no lineal calibrada con supuesto de umbral de tolerancia |
| `Demanda minima` | Caja/Month | Nivel mínimo bajo el cual no se aplica pérdida de clientes | Supuesto: 200 cajas/mes |

---

### Subsistema 2 — Inventario y logística

Modela el flujo físico de cajas: las compras al proveedor y los despachos a los clientes.

**Stocks:**
- `Stock de huevos` — inventario físico disponible (inicial: 750 cajas)

**Flujos:**
- `Tasa de compra` — cajas que ingresan al inventario desde el proveedor
- `Tasa de despacho` — cajas que salen del inventario hacia los clientes

**Variables auxiliares y parámetros clave:**

| Variable | Unidad | Función | Fuente / supuesto |
|---|---|---|---|
| `Inventario Objetivo` | Caja | Meta de stock según si hay camión o no | 850 sin camión / 2.000 con camión (supuesto operacional) |
| `Necesidad de compra` | Caja | Diferencia entre inventario objetivo y stock actual | `MAX(0, Inventario Objetivo − Stock de huevos)` |
| `Disponibilidad proveedor` | Dmnl | Factor de disponibilidad mensual del proveedor | Tabla lookup: 0.8 en enero-febrero, 1.0 resto del año (dato real del proveedor) |
| `Capacidad maxima proveedor` | Caja/Month | Límite máximo de compra mensual al proveedor | Supuesto: 1.500 cajas/mes |
| `Paso de tiempo` | Month | Unidad de tiempo del modelo | 1 mes |

---

### Subsistema 3 — Finanzas

Acumula el resultado económico del negocio mes a mes, incorporando ingresos, costos operacionales y la eventual inversión en el camión.

**Stocks:**
- `Margen acumulado` — resultado financiero neto acumulado (inicial: 12.000.000 CLP)

**Flujos:**
- `Ingresos por ventas` — entrada al margen: `Tasa de despacho × Precio de venta`
- `Costo de compra` — salida: `Tasa de compra × Precio de compra`
- `Costos operacionales` — salida: costos fijos + costo variable por caja despachada
- `Inversion en capacidad` — salida única al momento de comprar el camión

**Variables auxiliares y parámetros clave:**

| Variable | Unidad | Valor | Fuente / supuesto |
|---|---|---|---|
| `Precio de venta` | CLP/Caja | 33.000 | Precio de mercado actual del negocio |
| `Precio de compra` | CLP/Caja | 24.000 | Costo real al proveedor |
| `Costo variable reparto` | CLP/Caja | 500 | Costo estimado de combustible y desgaste por caja |
| `Costo fijo mantenimiento` | CLP/(Caja/Month)/Month | 200 | Supuesto: proporcional a la capacidad instalada |
| `Costos fijos mensuales` | CLP/Month | 700.000 + mantenimiento camión | Base fija del negocio más mantenimiento variable del camión |
| `Costo de vehiculo` | CLP | 50.000.000 | Cotización real de camión de reparto en Chile |
| `Margen unitario de venta` | CLP/Caja | 8.500 | `33.000 − 24.000 − 500` |

---

### Subsistema 4 — Camión de reparto

Evalúa la decisión de inversión, el uso efectivo del camión y la recuperación de la inversión (ROI).

**Stocks:**
- `Capacidad Reparto` — capacidad máxima de despacho mensual (inicial: 720 cajas/mes, aumenta al comprar el camión)
- `Vehiculo comprado` — acumula el pulso de compra; pasa de 0 a 1 al adquirir el camión
- `Beneficio acumulado del camion` — beneficio neto generado por el camión desde su compra (inicial: 0 CLP)

**Flujos:**
- `Inversion en capacidad` — flujo que incrementa `Capacidad Reparto` al momento de la compra
- `Pulso de compra` — pulso único que activa la compra cuando el gatillo lo indica
- `Beneficio neto del camion` — flujo mensual neto atribuible al camión

**Variables auxiliares y parámetros clave:**

| Variable | Unidad | Función | Fuente / supuesto |
|---|---|---|---|
| `Camion en uso` | Dmnl | Indica si el camión está operativo (se apaga si demanda < umbral) | Lógica condicional: evita pagar mantenimiento en meses de baja demanda |
| `Demanda minima para camion` | Caja/Month | Umbral bajo el cual se deja de usar el camión | Supuesto: 700 cajas/mes |
| `Capacidad base sin camion` | Caja/Month | Capacidad de referencia histórica sin inversión | 867 cajas/mes (valor histórico del negocio) |
| `Capacidad atribuible al camion` | Caja/Month | Capacidad incremental por la inversión | `MAX(0, Capacidad Reparto − 867)` |
| `Despacho atribuible al camion` | Caja/Month | Despacho posible solo gracias al camión | `MIN(Tasa de despacho, Capacidad atribuible)` si camión en uso |
| `Beneficio bruto del camion` | CLP/Month | Margen generado por ventas atribuibles al camión | `Despacho atribuible × Margen unitario de venta` |
| `Mantenimiento del camion` | CLP/Month | Costo de mantener la capacidad extra; se anula si no está en uso | `Camion en uso × Capacidad atribuible × 200` |
| `ROI del camion` | Dmnl | Retorno acumulado sobre la inversión | `Beneficio acumulado / 50.000.000`; ROI = 1 significa que el camión se pagó a sí mismo |
| `Incremento capacidad por CLP` | (Caja/Month)/CLP | Conversión de CLP invertidos a capacidad de reparto | 4.328×10⁻⁵ (calculado a partir del costo y la capacidad del vehículo) |

---

## Bucles de retroalimentación

### B1 — Saturación de mercado *(balanceo)*
`Demanda Base` ↑ → `Fraccion de mercado Disponible` ↓ → `Tasa de captacion` ↓ → `Demanda Base` se estabiliza

El crecimiento se frena naturalmente al acercarse al mercado potencial.

### B2 — Fuga por incumplimiento *(balanceo)*
`Capacidad Reparto` insuficiente → `Tasa de incumplimiento` ↑ → `Tasa de fuga logistica` ↑ → `Tasa de perdida de clientes` ↑ → `Demanda Base` ↓

Este bucle es el principal mecanismo de presión para invertir en capacidad. Si no se actúa, el negocio pierde clientes de forma persistente.

### R1 — Crecimiento orgánico *(refuerzo)*
`Demanda Base` ↑ → `Tasa de captacion` ↑ → `Demanda Base` ↑

Activo mientras haya mercado disponible. Se combina con B1 para producir crecimiento en S.

### B3 — Reposición de inventario *(balanceo)*
`Stock de huevos` ↓ → `Necesidad de compra` ↑ → `Tasa de compra` ↑ → `Stock de huevos` ↑

Mantiene el inventario cerca del objetivo. Su velocidad está limitada por la disponibilidad del proveedor.

---

## Escenarios de simulación

El modelo compara tres escenarios controlados por la variable `Politica proactiva`:

### Escenario 0 — Base (sin intervención)
`Politica proactiva = 0`

El negocio opera sin comprar el camión. La capacidad de reparto permanece en 720 cajas/mes. A medida que la demanda crece, el incumplimiento aumenta, activando B2 y erosionando la cartera de clientes. Representa la situación actual sin cambios.

**Qué se espera ver:** El margen acumulado crece inicialmente pero se estanca o cae a medida que la fuga de clientes supera la captación.

### Escenario 1 — Intervención reactiva
`Politica proactiva = 1`

Se compra el camión únicamente cuando se cumplen dos condiciones simultáneas: el margen acumulado supera los 50.000.000 CLP (hay liquidez) y la tasa de incumplimiento supera el 10% (hay presión real). La compra ocurre tarde, después de que el daño en la demanda ya comenzó.

```
Gatillo reactivo = 1  si  Margen acumulado > 50.000.000  Y  Tasa de incumplimiento > 0.1
```

**Qué se espera ver:** Recuperación de la demanda y el margen después de la compra, pero con una pérdida de clientes acumulada en el período previo.

### Escenario 2 — Intervención proactiva *(configuración actual)*
`Politica proactiva = 2`

Se compra el camión en el mes 8, antes de que el incumplimiento se vuelva un problema grave. La capacidad se expande anticipadamente, permitiendo capturar más demanda desde temprano.

```
Gatillo proactivo = 1  si  Tiempo ≥ 8 meses
```

**Qué se espera ver:** Mayor margen acumulado al final del horizonte, mejor retención de clientes, y ROI positivo del camión dentro del período simulado.

### Objetivo de la comparación

| Indicador a comparar | Variable en Vensim |
|---|---|
| Resultado financiero total | `Margen acumulado` |
| Evolución de la cartera de clientes | `Demanda Base` |
| Pérdida de servicio | `Tasa de incumplimiento` |
| Retorno de la inversión | `ROI del camion` |
| Momento de recuperación del camión | `Beneficio acumulado del camion` |

---

## Supuestos explícitos

| Supuesto | Justificación |
|---|---|
| Mercado potencial = 1.200 cajas/mes | Estimación conservadora de la demanda del sector en la zona de operación |
| Tasa de crecimiento base = 2% mensual | Crecimiento orgánico moderado, consistente con un negocio establecido en expansión |
| Costo fijo mensual base = 700.000 CLP | Dato real del negocio (arriendos, sueldos base, servicios) |
| Costo del vehículo = 50.000.000 CLP | Cotización de mercado para camión de reparto de capacidad mediana en Chile |
| Disponibilidad proveedor = 80% en enero-febrero | Restricción real observada en el proveedor durante temporada alta |
| Estacionalidad calibrada con datos reales de ventas 2025 | Datos sintéticos generados a partir de los registros reales del negocio |
| Capacidad base sin camión = 867 cajas/mes | Valor histórico observado de la capacidad de reparto antes de cualquier inversión |
| Umbral de uso del camión = 700 cajas/mes | Por debajo de este nivel, el mantenimiento no se justifica económicamente |

---

## Estructura de archivos

```
Modelo.mdl      ← modelo principal de Vensim
README.md       ← este documento
```

Para abrir el modelo: Vensim PLE o Vensim Pro (versión 8.x o superior).
El resultado de la simulación se guarda automáticamente en `current.vdfx`.