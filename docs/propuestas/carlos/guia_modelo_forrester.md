# 🥚 Guía Explicativa del Modelo de Forrester
## Distribuidora de Huevos — Dinámica de Sistemas

---

## 1. Pregunta de Investigación

> **¿Cuándo conviene invertir en capacidad de reparto adicional (vehículo y personal) y cómo afecta esa decisión la rentabilidad y la base de clientes de la distribuidora en un horizonte de 24 meses (dos temporadas de verano)?**

Esta pregunta surge de un problema concreto: la distribuidora enfrenta cada verano un **cuello de botella logístico** — la demanda sube, pero la capacidad de reparto permanece fija. El modelo busca comparar tres decisiones posibles:

- **No invertir (Base):** la flota permanece fija los 24 meses.
- **Invertir reactivamente:** esperar a que haya incumplimiento Y caja suficiente para actuar.
- **Invertir proactivamente:** comprar el vehículo antes del primer verano, anticipando el peak.

El resultado esperado es cuantificar cuándo cada política protege mejor la Demanda base y el Margen acumulado.

---

## 2. Variable de Modelación Principal

**`Capacidad de reparto`** es la variable central del modelo. Es el techo real del sistema: sin importar cuánto stock haya en bodega ni cuán alta sea la demanda, si esta variable está saturada, el negocio no puede despachar más.

### ¿Está bien modelada?

Sí. En el modelo de Forrester, `Capacidad de reparto` es un **stock (Level)** que comienza en **720 cajas/mes** (calibrado con datos históricos 2025) y solo puede aumentar cuando se gatilla la inversión.

```
Capacidad de reparto = INTEG( Inversion en capacidad × Incremento cap por CLP,  720 )
```

- Valor inicial 720 cajas/mes ≈ 200 cajas/semana, consistente con el volumen fuera de temporada.
- `Incremento cap por CLP = 0,00004328 (cajas/mes)/CLP` → el vehículo de $50.000.000 agrega **≈2.164 cajas/mes** adicionales de capacidad.

La capacidad actúa directamente como restricción en `Tasa de despacho`:

```
Tasa de despacho = MIN( Capacidad de reparto, MIN( Demanda total, Stock de huevos / Paso de tiempo ) )
```

Este **MIN triple** garantiza que el sistema nunca despache más de lo que puede transportar, más de lo que piden, ni más de lo que tiene en bodega. Es la implementación directa del cuello de botella.

---

## 3. Problemática Identificada

### El problema central

La distribuidora opera con un único vehículo de reparto familiar. En los meses de verano (enero-febrero), la demanda puede ser hasta **1,84 veces el promedio** del resto del año (factor de estacionalidad calibrado con datos 2025). En esos mismos meses, el proveedor reduce su disponibilidad un **20%** por presión de la cadena de abastecimiento. Esta doble presión —más demanda, menos stock— colapsa el sistema.

**Consecuencias en cadena (Bucle B3):**

1. La Capacidad de reparto no alcanza → `Tasa de despacho < Demanda total`
2. Sube la `Tasa de incumplimiento` (pedidos no entregados / pedidos totales)
3. La `Tasa de fuga logística` (lookup no lineal) convierte incumplimiento en pérdida de clientes
4. La `Demanda base` se erosiona → el segundo verano parte con menos clientes que el primero
5. Si no hubo inversión, el negocio entra en un ciclo de declive acumulado

### Datos históricos que validan el problema

| Mes 2025 | Ventas CLP | Ganancia líquida | Observación |
|----------|-----------|-----------------|-------------|
| Enero | $13.948.263 | $2.520.178 | Peak verano — mayor volumen del año |
| Febrero | $13.771.471 | $4.264.757 | Segundo mes de peak — mayor margen |
| Marzo | $6.403.502 | $86.334 | Caída brusca — baja demanda + costos |
| Octubre | $6.929.610 | $260.452 | Inicio de temporada alta — compras suben |
| Diciembre | $9.637.905 | $545.771 | Transición al segundo verano |

La brecha entre enero-febrero y el resto del año es evidente. El modelo reproduce este patrón mediante el **lookup de Estacionalidad**, que aplica factores de 1,84 en enero y 1,81 en febrero al stock `Demanda base`.

---

## 4. Propuesta: Del Estado Actual al Estado Futuro

### 4.1 Escenario Base (estado actual) — `Politica proactiva = 0`

El negocio no realiza ninguna inversión en capacidad durante los 24 meses. La flota permanece fija en 720 cajas/mes. Cada verano genera incumplimiento y erosiona la `Demanda base`.

**Comportamiento esperado:**
- Verano mes 12-13: incumplimiento ~30-50% → fuga de clientes comienza
- Demanda base cae progresivamente
- Margen acumulado crece menos porque se despacha menos de lo que se podría vender
- Segundo verano (mes 24): demanda reducida + capacidad igual = colapso más severo

### 4.2 Escenario Reactivo (primer paso de mejora) — `Politica proactiva = 1`

El negocio invierte cuando se cumplen dos condiciones simultáneas:

```
Gatillo reactivo = 1   si:   Margen acumulado > $50.000.000   Y   Tasa de incumplimiento > 0,1
```

El problema de esta política es que **llega tarde**: primero falla, luego pierde clientes, y solo entonces invierte. La fuga ya ocurrió. La inversión recupera capacidad, pero la Demanda base ya cayó, así que la capacidad adicional queda subutilizada un tiempo.

### 4.3 Escenario Proactivo (estado futuro ideal) — `Politica proactiva = 2`

El negocio compra el vehículo en el **mes 8**, antes de que llegue el primer verano (meses 12-13):

```
Gatillo proactivo = 1   si:   Tiempo >= Mes de compra (= 8)
```

No requiere que haya incumplimiento. No espera señal de colapso. La inversión se hace anticipadamente, cuando el margen acumulado todavía es positivo.

La **diferencia clave** respecto al escenario Base es que la Capacidad de reparto sube *antes* del peak estacional. Cuando llega enero (mes 13), la Tasa de despacho puede satisfacer la Demanda total sin incumplimiento → la Demanda base se mantiene o crece → el margen acumulado es mayor porque se vende más en el peak.

### 4.4 ¿Qué cambia entre escenarios?

| Variable afectada | Escenario Base | Escenario Reactivo | Escenario Proactivo |
|------------------|---------------|-------------------|---------------------|
| Capacidad de reparto | Fija en 720 c/mes | Sube ~mes 15-18 | Sube mes 8 |
| Tasa de incumplimiento | Alta en veranos | Alta → baja tras inversión | Casi 0 en veranos |
| Demanda base (mes 24) | Reducida (erosión) | Parcialmente recuperada | Mantenida o mayor |
| Margen acumulado (mes 24) | Menor (menos despacho) | Intermedio | Mayor (peak aprovechado) |
| Fuga de clientes | Persistente | Ocurre pero se frena | Mínima o nula |

---

## 5. Bucles de Retroalimentación

El modelo tiene **cuatro bucles** identificados.

---

### B1 — Límite logístico (Balanceo)

```
Stock de huevos → (+) Tasa de despacho → (−) Stock de huevos
```

Cada caja que se despacha sale de bodega. Si el stock baja, la próxima entrega disponible baja también. Este bucle es el **freno natural del inventario**: el negocio no puede despachar más de lo que tiene almacenado. La `Capacidad de reparto` opera como techo fijo sobre este bucle: aunque haya stock, si la capacidad está saturada, el despacho no supera ese techo. En verano, este techo es el factor dominante.

---

### B2 — Reposición de inventario (Balanceo)

```
Stock de huevos → (−) Necesidad de compra → (+) Tasa de compra → (+) Stock de huevos
```

Es el bucle de control de inventario. El negocio tiene un **Inventario Objetivo de 1.300 cajas**. La Necesidad de compra mide la brecha entre ese objetivo y el stock actual:

```
Necesidad de compra = MAX(0, 1300 − Stock de huevos)
```

Mientras más alejado esté el stock del objetivo, más se compra; a medida que el stock se acerca, la compra se reduce. Esto es más realista que comprar en función de la demanda — evita sobre-comprar o sub-comprar según la estacionalidad. El `MIN` con la disponibilidad del proveedor agrega la restricción de que en enero-febrero el proveedor solo puede cubrir el 80% de lo solicitado.

---

### R1 — Crecimiento por inversión (Refuerzo)

```
Margen acumulado → (+) Inversión en capacidad → (+) Capacidad de reparto
→ (+) Tasa de despacho → (+) Ingresos por ventas → (+) Margen acumulado
```

Es el único bucle de refuerzo del modelo. Cuando el negocio acumula suficiente margen **y decide invertir**, la capacidad de reparto sube, lo que permite despachar más, generar más ingresos, y acumular aún más margen. Es un ciclo virtuoso — pero solo se activa si se gatilla la inversión. En el escenario Base, **R1 nunca se activa** porque `Vehiculo comprado` no cambia de 0 a 1 y la `Inversión en capacidad` permanece en 0.

---

### B3 — Destrucción de demanda por colapso (Balanceo) ← Bucle clave

```
Demanda total → (+) Tasa de incumplimiento → (+) Tasa de fuga logística
→ (+) Tasa de pérdida de clientes → (−) Demanda base → (−) Demanda total
```

Este es el **bucle más importante del modelo** y la razón de ser de la propuesta de intervención. Es un arquetipo clásico de "límites al crecimiento" en dinámica de sistemas.

**Mecánica:** cuando la Capacidad de reparto no alcanza para satisfacer la Demanda total, la Tasa de incumplimiento sube. Ese incumplimiento, a través de un **lookup no lineal** (Tasa de fuga logística), se convierte en pérdida de clientes:

| Tasa de incumplimiento | Tasa de fuga logística |
|-----------------------|-----------------------|
| 0% | 0% |
| 10% | 2% (los clientes toleran retrasos pequeños) |
| 30% | 10% |
| 50% | 25% (la relación se acelera) |
| 70% | 30% |
| 100% | 32% |

Los clientes perdidos reducen la Demanda base, lo que hace que el segundo verano empiece con menos pedidos que el primero.

**Por qué es el bucle clave:** responde directamente la pregunta de investigación. Sin inversión, B3 se activa cada verano y erosiona progresivamente la base de clientes. Con inversión proactiva (R1), la Tasa de incumplimiento se mantiene cerca de 0, B3 no se activa, y la Demanda base se sostiene o crece.

---

## 6. Por qué se usan MIN, MAX, IF THEN ELSE y Lookups

### MIN — Restricción de la variable más limitante

| Ecuación | Por qué MIN |
|----------|------------|
| `Tasa de despacho = MIN(Cap. reparto, MIN(Demanda total, Stock/Paso))` | El sistema solo puede despachar tanto como lo permita el cuello de botella más estrecho: vehículo, pedidos o stock. Si usáramos suma o promedio, el modelo podría "despachar" más de lo físicamente posible. |
| `Tasa de compra = MIN(Necesidad de compra, Disp. proveedor × Cap. máx.)` | El proveedor no siempre puede surtir todo lo que el negocio necesita. El MIN garantiza que la compra nunca supera lo que el proveedor puede entregar ese mes. |

### MAX — Piso para evitar valores negativos o absurdos

| Ecuación | Por qué MAX |
|----------|------------|
| `Tasa de incumplimiento = MAX(0, (Dem. total − Tasa despacho) / Dem. total)` | Si el despacho iguala o supera la demanda, la fórmula daría 0 o negativo. MAX(0, …) asegura que el incumplimiento nunca sea negativo — semánticamente, "incumplimiento negativo" no existe. |
| `Necesidad de compra = MAX(0, Inventario Objetivo − Stock)` | Si el stock ya supera el objetivo, no hay necesidad de comprar más. MAX(0, …) evita que el modelo "devuelva" huevos al proveedor. |

### IF THEN ELSE — Lógica de decisión y seguridad

| Ecuación | Por qué IF THEN ELSE |
|----------|---------------------|
| `Tasa de pérdida = IF THEN ELSE(Demanda base > Demanda mínima, DB × fuga, 0)` | Sin este freno, la fuga podría llevar la Demanda base a valores negativos (imposibles en realidad). El condicional detiene la pérdida cuando ya se llegó al mínimo viable de clientes. |
| `Pulso de compra = IF THEN ELSE(Gatillo activo = 1 AND Vehiculo < 1, 1/Paso, 0)` | Garantiza que la inversión ocurra exactamente una vez. Si no se pusiera la condición `Vehiculo < 1`, el modelo gastaría el costo del vehículo cada mes que el gatillo esté activo. |
| `Gatillo activo = IF THEN ELSE(Pol = 2, GP, IF THEN ELSE(Pol = 1, GR, 0))` | Selecciona el escenario activo según el valor de `Politica proactiva`. Funciona como un switch de simulación: cambiar una constante cambia toda la lógica de decisión. |

### WITH LOOKUP — Relaciones no lineales calibradas con datos reales

| Lookup | Por qué es no lineal |
|--------|---------------------|
| `Estacionalidad` (función de `MODULO(Tiempo, 12)`) | La demanda no sube linealmente en verano — tiene un perfil específico calibrado mes a mes con los datos 2025. Un factor lineal no capturaría el doble peak enero-febrero ni la caída brusca de marzo. `MODULO` hace que el ciclo se repita automáticamente cada 12 meses sin listar los puntos dos veces. |
| `Disponibilidad proveedor` (función de `MODULO(Tiempo, 12)`) | El proveedor no reduce disponibilidad gradualmente — cae a 0,8 en enero y febrero de cada año y luego vuelve al 100%. Un lookup capta este comportamiento discreto. |
| `Tasa de fuga logística` (función de `Tasa de incumplimiento`) | La fuga de clientes no es proporcional al incumplimiento — al principio los clientes toleran pequeños retrasos, pero si la falla es severa, el abandono se acelera. Una relación lineal subestimaría el daño en episodios graves. |

---

## 7. Resumen para la Presentación

| Pregunta | Respuesta del modelo |
|----------|---------------------|
| ¿Cuál es la variable principal? | `Capacidad de reparto` — stock que actúa como techo logístico del sistema |
| ¿Cuál es el bucle más importante? | B3 — destrucción de demanda: sin inversión, cada verano erosiona la base de clientes |
| ¿Qué diferencia al escenario Base del Proactivo? | En Base: vehículo no se compra, capacidad fija, fuga acumulada. En Proactivo: vehículo mes 8, capacidad ampliada antes del peak, fuga evitada |
| ¿Cómo se modela la decisión de invertir? | Flag `Vehiculo comprado` (stock 0→1) + `Pulso de compra` (flujo de un solo paso) evitan gasto repetido |
| ¿Por qué se usan MIN y MAX? | Para respetar restricciones físicas reales: no despachar más del cuello de botella, no comprar más de lo que el proveedor puede dar, no perder más clientes de los que existen |
| ¿Qué mide la Tasa de incumplimiento? | Fracción de pedidos no entregados. Es el disparador de B3 y del gatillo reactivo de inversión |

---

*Documento elaborado como material de apoyo para la defensa del proyecto — Teoría de Sistemas.*
