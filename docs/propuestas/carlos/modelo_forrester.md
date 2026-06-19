# 🥚 Modelo Dinámica de Sistemas — Distribuidora de Huevos
## Versión adoptada: Tiempo de Inversión con Demanda Creciente y Fuga de Clientes

[← Volver a la Propuesta del Proyecto](./readme.md) · [Ver datos históricos 2025 →](./DATOS_HISTORICOS.md)

---

## 1. Diagrama Causal (CLD) — actualizado

```mermaid
flowchart TD
    E([Estacionalidad]):::exo
    DP([Disp. proveedor]):::exo
    Ti([Tiempo]):::exo

    subgraph S1["🚛 Subsistema 1 — Operacional / Demanda"]
        DB[["Demanda base"]]:::stock
        DM["Demanda mínima"]:::param
        TCap(("Tasa de captación")):::flow
        TPC(("Tasa de pérdida\nde clientes")):::flow
        DT{"Demanda total"}:::aux
        IO["Inventario objetivo"]:::param
        NC{"Necesidad\nde compra"}:::aux
        CMP["Cap. máx.\nproveedor"]:::param
        TC(("Tasa de compra")):::flow
        SH[["Stock de huevos"]]:::stock
        CR[["Cap. de reparto"]]:::stock
        TD(("Tasa de despacho")):::flow
        TI{"Tasa de\nincumplimiento"}:::aux
        TF{"Tasa de fuga\nlogística (lookup)"}:::aux
    end

    subgraph S2["💰 Subsistema 2 — Financiero / Inversión"]
        PV["Precio de venta"]:::param
        IV(("Ingresos por ventas")):::flow
        CC(("Costo de compra")):::flow
        CO{"Costos\noperacionales"}:::aux
        MA[["Margen acumulado"]]:::stock
        VC[["Vehículo comprado\n(flag 0/1)"]]:::stock
        GR{"Gatillo reactivo"}:::aux
        GP{"Gatillo proactivo"}:::aux
        GA{"Gatillo activo"}:::aux
        PP["Política proactiva"]:::param
        IC(("Inversión en\ncapacidad")):::flow
    end

    E -->|+| DT
    E -->|-| DP
    DB -->|+| DT
    DT -->|+| TI

    IO -->|+| NC
    SH -->|-| NC
    NC -->|+| TC
    DP -->|+| TC
    CMP -->|+| TC
    TC -->|+| SH
    SH -->|+| TD
    CR -->|+| TD
    TD -->|-| SH

    TD -->|-| TI
    TI -->|+| TF
    TF -->|+| TPC
    DM -->|umbral| TPC
    TPC -->|-| DB
    TCap -->|+| DB

    PV -->|+| IV
    TD -->|+| IV
    IV -->|+| MA
    CC -->|-| MA
    CO -->|-| MA
    IC -->|-| MA

    MA -->|+| GR
    TI -->|+| GR
    Ti -->|+| GP
    PP -->|selecciona rama| GA
    GR -->|si PP≠1| GA
    GP -->|si PP=1| GA
    GA -->|gatilla una vez| VC
    VC -->|+| IC
    IC -->|+| CR
    CR -->|+| CO

    TC -.-> CC

    classDef exo   fill:#FAEEDA,stroke:#BA7517,color:#633806
    classDef stock fill:#EEEDFE,stroke:#534AB7,color:#26215C,font-weight:bold
    classDef flow  fill:#D4EDDA,stroke:#28A745,color:#155724
    classDef aux   fill:#E1F5EE,stroke:#0F6E56,color:#04342C
    classDef param fill:#FFF3CD,stroke:#856404,color:#533F03
```

> **Cambio clave respecto a la versión anterior:** `Tasa de compra` ya no depende directamente de `Demanda total`. Ahora responde a una lógica de **reposición hacia un inventario objetivo** (`Necesidad de compra = Inventario objetivo − Stock de huevos`), acotada por lo que el proveedor puede entregar ese mes (`Disponibilidad proveedor × Cap. máx. proveedor`). Esto agrega un bucle de control de inventario nuevo (ver **B2** en la sección 2) que no existía en la versión anterior del modelo.

---

## 2. Bucles de retroalimentación

```mermaid
flowchart LR
    subgraph R1["🔄 R1 — Crecimiento por inversión (Refuerzo)"]
        MAr[["Margen acumulado"]] -->|+| ICr(("Inversión en capacidad"))
        ICr -->|+| CRr[["Cap. de reparto"]]
        CRr -->|+| TDr(("Tasa de despacho"))
        TDr -->|+| IVr(("Ingresos"))
        IVr -->|+| MAr
    end

    subgraph B1["🔄 B1 — Límite logístico (Balanceo)"]
        SHb[["Stock de huevos"]] -->|+| TDb(("Tasa de despacho"))
        TDb -->|−| SHb
        CRb["Cap. de reparto"] -->|techo| TDb
    end

    subgraph B2["🔄 B2 — Reposición de inventario (Balanceo)"]
        SHb2[["Stock de huevos"]] -->|−| NCb2{"Necesidad de compra"}
        NCb2 -->|+| TCb2(("Tasa de compra"))
        TCb2 -->|+| SHb2
    end

    subgraph B3["🔄 B3 — Destrucción de demanda por colapso (Balanceo)"]
        DTb3{"Demanda total"} -->|+| TIb3{"Tasa de\nincumplimiento"}
        TDb3(("Tasa de despacho")) -->|−| TIb3
        TIb3 -->|+| TFb3{"Tasa de fuga"}
        TFb3 -->|+| TPCb3(("Tasa de pérdida\nde clientes"))
        TPCb3 -->|−| DBb3[["Demanda base"]]
        DBb3 -->|+| DTb3
    end
```

**B3 sigue siendo el bucle clave de la propuesta** — es un arquetipo de "límites al crecimiento". Con 24 meses de simulación, el primer verano (mes 12-13) genera incumplimiento y empieza a erosionar `Demanda base`; el segundo verano (mes 24) parte con una `Demanda base` ya reducida si no hubo inversión, mostrando el costo acumulado de la inacción.

**B2 es nuevo en esta versión.** Antes, `Tasa de compra` simplemente seguía a la `Demanda total`, lo que podía sobre-comprar o sub-comprar según la estacionalidad. Ahora el negocio compra para cerrar la brecha entre el `Stock de huevos` y un `Inventario objetivo` fijo (1.300 cajas), acotado por la capacidad real del proveedor. Es un bucle de balanceo clásico de control de inventario: mientras más lejos esté el stock del objetivo, más se compra; a medida que el stock se acerca al objetivo, la compra se reduce.

---

## 3. Variables del modelo — tabla completa con herramienta Vensim

### 3.1 Stocks — Stock Tool (Box Variable / Level)

| Variable | Valor inicial | Unidad | Ecuación INTEG | Descripción |
|----------|:-------------:|--------|-----------------|-------------|
| `Demanda base` | 700 | cajas/mes | `INTEG(Tasa de captacion − Tasa de perdida de clientes, 700)` | Volumen de clientes estables, antes de aplicar estacionalidad |
| `Stock de huevos` | 800 | cajas | `INTEG(Tasa de compra − Tasa de despacho, 800)` | Inventario físico en bodega |
| `Capacidad de reparto` | 720 | cajas/mes | `INTEG(Inversion en capacidad * Incremento cap por CLP, 720)` | Techo logístico de despacho mensual |
| `Margen acumulado` | 12.000.000 | CLP | `INTEG(Ingresos por ventas − (Costo de compra + Costos operacionales + Inversion en capacidad), 12.000.000)` | Caja líquida acumulada |
| `Vehiculo comprado` | 0 | Dmnl (flag) | `INTEG(Pulso de compra, 0)` | Flag que pasa de 0 a 1 una sola vez cuando se gatilla la inversión — evita que se gaste dinero repetidamente |
| **`Tiempo`** *(nuevo)* | 0 | mes | `INTEG(1, 0)` | Reloj propio del modelo (equivalente al `Time` de Vensim), usado por los lookups de `Estacionalidad` y `Disponibilidad proveedor` vía `MODULO(Tiempo,12)`, y por `Gatillo proactivo` |

### 3.2 Flujos — Flow Tool (Rate)

| Variable | Unidad | Ecuación | Descripción |
|----------|--------|----------|-------------|
| `Tasa de captacion` | cajas/mes/mes | `Demanda base * Tasa crecimiento base` | Crecimiento orgánico mensual de clientes estables |
| **`Tasa de perdida de clientes`** *(con piso)* | cajas/mes/mes | `IF THEN ELSE(Demanda base > Demanda minima, Demanda base * Tasa de fuga logistica, 0)` | Pérdida de clientes por insatisfacción logística; se detiene si la base de clientes ya cayó al mínimo viable, evitando que el stock se vuelva negativo |
| **`Tasa de compra`** *(lógica de reposición)* | cajas/mes | `MIN(Necesidad de compra, Disponibilidad proveedor * Capacidad maxima proveedor)` | Compra lo necesario para alcanzar el inventario objetivo, acotado por lo que el proveedor puede entregar ese mes |
| `Tasa de despacho` | cajas/mes | `MIN(Capacidad de reparto, Demanda total, Stock de huevos / Paso de tiempo)` | Ventas físicas despachadas. La división por `Paso de tiempo` es una salvaguarda numérica de Vensim para que el stock nunca se vuelva negativo en un paso de integración — no es un error de unidades |
| `Ingresos por ventas` | CLP/mes | `Tasa de despacho * Precio de venta` | Entrada financiera mensual |
| `Costo de compra` | CLP/mes | `Tasa de compra * Precio de compra` | Salida financiera por pago al proveedor |
| `Inversion en capacidad` | CLP/mes | `Pulso de compra * Costo de vehiculo` | Gasta el costo del vehículo **una sola vez**, en el instante exacto en que `Vehiculo comprado` pasa de 0 a 1 — ver detalle en sección 4 |
| `Pulso de compra` | Dmnl/mes | `IF THEN ELSE(Gatillo activo = 1 :AND: Vehiculo comprado < 1, 1 / Paso de tiempo, 0)` | Genera el pulso de activación del flag, una sola vez |

### 3.3 Variables auxiliares — Auxiliary Tool

| Variable | Unidad | Ecuación | Descripción |
|----------|--------|----------|-------------|
| `Demanda total` | cajas/mes | `Demanda base * Estacionalidad` | Demanda estacional del mes actual |
| `Tasa de incumplimiento` | Dmnl | `MAX(0, (Demanda total − Tasa de despacho) / Demanda total)` | Fracción de pedidos no entregados |
| **`Necesidad de compra`** *(nuevo)* | cajas | `MAX(0, Inventario Objetivo − Stock de huevos)` | Brecha entre el inventario objetivo (dinámico: 850 antes del vehículo, 2.000 después) y el stock actual; es la que dispara la compra |
| `Costos operacionales` | CLP/mes | `Costos fijos mensuales + (Tasa de despacho * Costo variable reparto)` | Costos totales de operación |
| `Costos fijos mensuales` | CLP/mes | `200000 + (Capacidad de reparto − 867) * Costo fijo mantenimiento` | Escala con la capacidad agregada — más realista que un costo fijo plano |
| `Gatillo reactivo` | Dmnl (booleano) | `IF THEN ELSE(Margen acumulado > Costo de vehiculo AND Tasa de incumplimiento > 0.1, 1, 0)` | Se activa solo si hay caja Y hay colapso ya ocurriendo |
| **`Gatillo proactivo`** *(en función de `Tiempo`)* | Dmnl (booleano) | `IF THEN ELSE(Tiempo >= Mes de compra, 1, 0)` | Se activa desde el mes definido en adelante, independiente del estado de caja |
| **`Inventario Objetivo`** *(variable auxiliar)* | Caja | `IF THEN ELSE(Vehiculo comprado = 1, 2000, 850)` | Objetivo de stock dinámico: 850 cajas con el furgón actual, 2.000 cajas una vez comprado el camión. Al cambiar de valor, `Necesidad de compra` aumenta y el modelo empieza a comprar más para llenar la bodega gradualmente |
| `Gatillo activo` | Dmnl (booleano) | `IF THEN ELSE( Politica proactiva = 2, Gatillo proactivo, IF THEN ELSE( Politica proactiva = 1, Gatillo reactivo, 0 ) )` | Selecciona qué política manda según el escenario simulado — **ver nota de verificación en la sección 6** sobre cómo esta fórmula lee los valores de `Politica proactiva` |

### 3.4 Lookups — Auxiliary Tool con WITH LOOKUP

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Tasa de fuga logistica` | Lookup de `Tasa de incumplimiento` | Puntos: `(0,0) (0.1,0.02) (0.3,0.10) (0.5,0.25) (0.7,0.30) (1,0.32)` — fuga no lineal, crece más rápido cuando el incumplimiento es severo |
| `Estacionalidad` | Lookup de `MODULO(Tiempo,12)` | Puntos mensuales (ver sección 5). Enero (1,84) y febrero (1,81) son los factores más altos del año, consistentes con el peak histórico de compras y ventas de 2025 registrado en [DATOS_HISTORICOS.md](./DATOS_HISTORICOS.md), donde ambos meses superaron ampliamente el promedio del resto del año. El `MODULO` hace que el ciclo se repita cada 12 meses sin necesidad de listar los puntos dos veces |
| `Disponibilidad proveedor` | Lookup de `MODULO(Tiempo,12)` | Cae a 0,8 en los meses 0, 1, 12, 13 y 24 (enero-febrero de cada año) — el −20 % de disponibilidad estival asumido en la propuesta original, ahora aplicado de forma cíclica con `MODULO` en lugar de repetir manualmente los puntos año por año |

### 3.5 Constantes — Constant Tool

| Constante | Valor | Unidad | Justificación |
|-----------|:-----:|--------|----------------|
| `Tasa crecimiento base` | 0,02 | 1/mes | Crecimiento orgánico mensual estimado — **brecha a validar con datos reales** (ver sección 9) |
| `Precio de venta` | 33.000 | CLP/caja | Ajustado a la escala de los registros reales 2025 (ver [DATOS_HISTORICOS.md](./DATOS_HISTORICOS.md)); conviene confirmar contra el precio promedio efectivo por caja despachada (ver sección 9) |
| `Precio de compra` | 24.000 | CLP/caja | Ajustado a la escala de los registros reales 2025; mismo comentario que el precio de venta |
| `Costo de vehiculo` | 50.000.000 | CLP | Estimado de mercado para vehículo de reparto adicional (actualizado al alza respecto a la versión anterior del modelo) |
| `Incremento cap por CLP` | 0,00004328 | (cajas/mes)/CLP | Traduce el costo del vehículo (50.000.000 CLP) en ≈2.164 cajas/mes adicionales de capacidad |
| `Costo variable reparto` | 500 | CLP/caja | Combustible, peajes por caja despachada |
| `Costo fijo mantenimiento` | 200 | CLP/caja/mes | Sueldo chofer + mantención, prorrateado por capacidad agregada |
| `Mes de compra` | 8 | mes | Mes en que se activa la compra si la política es proactiva (antes del primer verano, mes 12-13) |
| `Politica proactiva` | 2 *(valor configurado actualmente)* | Dmnl | Bandera de escenario: `0`=Base, `1`=Reactivo, `2`=Proactivo. `Gatillo activo` ya implementa las tres ramas correctamente (ver sección 5) |
| **`Inventario Objetivo`** *(variable auxiliar)* | — | Caja | Ya no es una constante fija. Toma el valor 850 antes de la compra del vehículo y 2.000 después. Ver ecuación en sección 3.3 |
| **`Paso de tiempo`** *(renombrado)* | 1 | mes | Equivalente al `TIME STEP` de Vensim, ahora referenciado explícitamente por nombre en `Tasa de despacho` y `Pulso de compra` |
| **`Demanda minima`** *(referenciada, valor pendiente)* | ❓ | cajas/mes | Usada en `Tasa de perdida de clientes` como piso de la fuga de clientes — falta definir su valor en el bloque de constantes (ver sección 9) |
| **`Capacidad maxima proveedor`** *(referenciada, valor pendiente)* | ❓ | cajas/mes | Usada en `Tasa de compra` como techo de lo que el proveedor puede entregar — falta definir su valor en el bloque de constantes (ver sección 9) |

---

## 4. Detalle de la corrección del gasto repetido (el error más importante)

**Por qué era un error:** en la propuesta original, `Inversión en capacidad` se recalculaba cada mes a partir de `Gatillo inversion`. Si la política era proactiva, `STEP(1,6)` sube a 1 en el mes 6 y **nunca vuelve a bajar** — Vensim seguiría ejecutando `Costo de vehiculo / Paso de tiempo` en cada paso posterior, gastando el costo del vehículo mensualmente de forma indefinida.

**Cómo se corrige:** se agrega el stock `Vehiculo comprado`, que solo puede pasar de 0 a 1 una vez. El flujo `Inversion en capacidad` se activa únicamente en el instante en que ese cambio ocurre:

```
Vehiculo comprado = INTEG( Pulso de compra, 0 )
    UNITS: Dmnl

Pulso de compra =
    IF THEN ELSE( Gatillo activo = 1 :AND: Vehiculo comprado < 1, 1 / Paso de tiempo, 0 )
    UNITS: Dmnl/mes

Inversion en capacidad =
    Pulso de compra * Costo de vehiculo
    UNITS: CLP/mes
```

Con esto, en el paso de integración donde se activa el gatillo, `Pulso de compra` vale `1/Paso de tiempo` exactamente durante ese paso, lo que multiplicado por `Paso de tiempo` en la integración entrega el costo completo del vehículo **una sola vez**. En el paso siguiente, `Vehiculo comprado` ya es 1, así que `Pulso de compra` vuelve a 0 y el gasto no se repite.

---

## 5. Ecuaciones completas para Vensim

```
════════════════════════════════════════════════════════════
 CONTROL DE SIMULACIÓN
════════════════════════════════════════════════════════════

INITIAL TIME = 0      UNITS: mes
FINAL TIME   = 24     UNITS: mes   (2 años → 2 veranos)
TIME STEP    = 1      UNITS: mes
SAVEPER      = TIME STEP

════════════════════════════════════════════════════════════
 STOCKS
════════════════════════════════════════════════════════════

Demanda base = INTEG( Tasa de captacion - Tasa de perdida de clientes, 700 )
    UNITS: cajas/mes

Stock de huevos = INTEG( Tasa de compra - Tasa de despacho, 750 )
    UNITS: cajas

Capacidad de reparto = INTEG( Inversion en capacidad * Incremento cap por CLP, 720 )
    UNITS: cajas/mes

Margen acumulado = INTEG(
    Ingresos por ventas - (Costo de compra + Costos operacionales + Inversion en capacidad),
    12000000 )
    UNITS: CLP

Vehiculo comprado = INTEG( Pulso de compra, 0 )
    UNITS: Dmnl
Tiempo = INTEG(
    1,0
)


════════════════════════════════════════════════════════════
 FLUJOS
════════════════════════════════════════════════════════════

Tasa de captacion =
    Demanda base * Tasa crecimiento base
    UNITS: cajas/mes/mes

Tasa de perdida de clientes =
    IF THEN ELSE(Demanda Base > Demanda minima, Demanda Base * Tasa de fuga logistica, 0)
    UNITS: cajas/mes/mes

Tasa de compra =
    MIN(Necesidad de compra, Disponibilidad proveedor * Capacidad maxima proveedor)
    UNITS: cajas/mes

Tasa de despacho =
    MIN( Capacidad Reparto, MIN( Demanda total, Stock de huevos/ Paso de tiempo) )
    UNITS: cajas/mes

Ingresos por ventas =
    Tasa de despacho * Precio de venta
    UNITS: CLP/mes

Costo de compra =
    Tasa de compra * Precio de compra
    UNITS: CLP/mes

Pulso de compra =
    IF THEN ELSE(
        Gatillo Activo = 1 :AND: Vehiculo comprado < 1,
        1/Paso de tiempo,
        0 )
    UNITS: Dmnl/mes

Inversion en capacidad =
    Pulso de compra * Costo de vehiculo
    UNITS: CLP/mes

════════════════════════════════════════════════════════════
 VARIABLES AUXILIARES
════════════════════════════════════════════════════════════

Demanda total =
    Demanda base * Estacionalidad
    UNITS: cajas/mes

Tasa de incumplimiento =
    MAX( 0, (Demanda total - Tasa de despacho) / Demanda total )
    UNITS: Dmnl

Costos fijos mensuales =
    200000 + (Capacidad de reparto - 867) * Costo fijo mantenimiento
    UNITS: CLP/mes

Costos operacionales =
    Costos fijos mensuales + (Tasa de despacho * Costo variable reparto)
    UNITS: CLP/mes

Gatillo reactivo =
    IF THEN ELSE(
            Margen acumulado > Costo de Vehiculo :AND: Tasa de incumplimiento > 0.1,
            1, 0 )
    UNITS: Dmnl

Gatillo proactivo =
    IF THEN ELSE(Tiempo >= Mes de compra, 1, 0)
    UNITS: Dmnl

Gatillo activo =
    IF THEN ELSE( Politica proactiva = 2, Gatillo proactivo,
        IF THEN ELSE( Politica proactiva = 1, Gatillo reactivo, 0 ) )
    UNITS: Dmnl

Necesidad de compra =
    MAX(0, Inventario Objetivo - Stock de huevos)
    UNITS: Dmnl

Inventario Objetivo =
    IF THEN ELSE(Vehiculo comprado = 1, 2000, 850)
    UNITS: Caja


════════════════════════════════════════════════════════════
 LOOKUPS
════════════════════════════════════════════════════════════

Tasa de fuga logistica( Tasa de incumplimiento ) =
    WITH LOOKUP( Tasa de incumplimiento,
    ([(0,0)-(0.5,0.3)],(0,0), (0.1,0.02), (0.3,0.1), (0.5,0.25), (0.7,0.3), (1,0.32)))
    UNITS: Dmnl

Estacionalidad = WITH LOOKUP( MODULO ( Tiempo , 12 ),
    ([(0,0)-(24,2)],(0,1.84), (1,1.81), (2,0.84), (3,0.78), (4,0.9), (5,0.75), (6,0.84), (7,0.67), (8,0.69), (9,0.91), (10,0.71), (11,1.27))
    )
    UNITS: Dmnl

Disponibilidad proveedor = WITH LOOKUP( MODULO ( Tiempo , 12 ),
    ([(0,0)-(25,1.1)],
    (0,0.8),(1,0.8),(2,1.0),(3,1.0),(4,1.0),(5,1.0),
    (6,1.0),(7,1.0),(8,1.0),(9,1.0),(10,1.0),(11,1.0),
    (12,0.8),(13,0.8),(14,1.0),(15,1.0),(16,1.0),(17,1.0),
    (18,1.0),(19,1.0),(20,1.0),(21,1.0),(22,1.0),(23,1.0),
    (24,0.8)) )
    UNITS: Dmnl

════════════════════════════════════════════════════════════
 CONSTANTES
════════════════════════════════════════════════════════════

Tasa crecimiento base   = 0.02       UNITS: 1/mes
Precio de venta         = 33000      UNITS: CLP/caja
Precio de compra        = 24000       UNITS: CLP/caja
Costo de vehiculo       = 50000000    UNITS: CLP
Incremento cap por CLP  = 0,00004328     UNITS: (cajas/mes)/CLP
Costo variable reparto  = 500        UNITS: CLP/caja
Costo fijo mantenimiento = 200       UNITS: CLP/caja/mes
Mes de compra           = 8          UNITS: mes
Politica proactiva      = 2          UNITS: Dmnl
    ~ Controla el escenario de simulación activo:
      0 = Base (sin inversión — negocio no amplía flota en ningún caso)
      1 = Reactivo (invierte cuando Margen acumulado > Costo del Vehiculo :AND: Tasa de incumplimiento > 0.1)
      2 = Proactivo (invierte anticipadamente en el mes definido por Mes de compra)
Paso de tiempo          = 1          UNITS: mes
```

---

## 6. Escenarios de simulación

| Escenario *(según comentario de la constante)* | `Politica proactiva` | `Mes de compra` | Comportamiento esperado |
|-----------|:---------------------:|:----------------:|---------------------------|
| **Base (sin inversión)** | 0 | — | Capacidad fija en 720 cajas/mes, sin ampliar flota. El primer verano genera incumplimiento y empieza a erosionar la `Demanda base` |
| **Reactivo** | 1 | — (se activa solo) | Espera a que `Margen acumulado > Costo de vehiculo` (50.000.000) Y `Tasa de incumplimiento > 0,1`. Sufre fuga de clientes antes de invertir, luego recupera capacidad |
| **Proactivo** | 2 *(valor configurado actualmente)* | 8 | Invierte en el mes 8, antes del primer verano (que cae en los meses 12-13 según `Estacionalidad`), independiente del estado de `Margen acumulado`. Protege la `Demanda base` desde el inicio |
---

## 7. Trazabilidad de variables — verificación rápida antes de correr Check Model

| Variable | Alimenta a | Es alimentada por |
|----------|------------|---------------------|
| `Tasa crecimiento base` | `Tasa de captacion` | — |
| `Demanda base` | `Tasa de captacion`, `Tasa de perdida de clientes`, `Demanda total` | `Tasa de captacion`, `Tasa de perdida de clientes` (INTEG) |
| `Demanda minima` | `Tasa de perdida de clientes` | — *(constante, valor pendiente — ver sección 9)* |
| `Estacionalidad` | `Demanda total` | `Tiempo` (vía `MODULO`, lookup) |
| `Demanda total` | `Tasa de incumplimiento`, `Tasa de despacho` | `Demanda base`, `Estacionalidad` |
| `Inventario Objetivo` | `Necesidad de compra` | — |
| `Necesidad de compra` | `Tasa de compra` | `Inventario Objetivo`, `Stock de huevos` |
| `Capacidad maxima proveedor` | `Tasa de compra` | — *(constante, valor pendiente — ver sección 9)* |
| `Disponibilidad proveedor` | `Tasa de compra` | `Tiempo` (vía `MODULO`, lookup) |
| `Tasa de compra` | `Stock de huevos`, `Costo de compra` | `Necesidad de compra`, `Disponibilidad proveedor`, `Capacidad maxima proveedor` |
| `Stock de huevos` | `Tasa de despacho`, `Necesidad de compra` | `Tasa de compra`, `Tasa de despacho` (INTEG) |
| `Capacidad de reparto` | `Tasa de despacho`, `Costos fijos mensuales` | `Inversion en capacidad` (INTEG) |
| `Paso de tiempo` | `Tasa de despacho`, `Pulso de compra` | — |
| `Tasa de despacho` | `Stock de huevos`, `Ingresos por ventas`, `Tasa de incumplimiento`, `Costos operacionales` | `Capacidad de reparto`, `Demanda total`, `Stock de huevos`, `Paso de tiempo` |
| `Tasa de incumplimiento` | `Tasa de fuga logistica`, `Gatillo reactivo` | `Demanda total`, `Tasa de despacho` |
| `Tasa de fuga logistica` | `Tasa de perdida de clientes` | `Tasa de incumplimiento` (lookup) |
| `Tasa de perdida de clientes` | `Demanda base` (INTEG) | `Demanda base`, `Demanda minima`, `Tasa de fuga logistica` |
| `Precio de venta` | `Ingresos por ventas` | — |
| `Ingresos por ventas` | `Margen acumulado` | `Tasa de despacho`, `Precio de venta` |
| `Precio de compra` | `Costo de compra` | — |
| `Costo de compra` | `Margen acumulado` | `Tasa de compra`, `Precio de compra` |
| `Costo fijo mantenimiento` | `Costos fijos mensuales` | — |
| `Costos fijos mensuales` | `Costos operacionales` | `Capacidad de reparto`, `Costo fijo mantenimiento` |
| `Costo variable reparto` | `Costos operacionales` | — |
| `Costos operacionales` | `Margen acumulado` | `Costos fijos mensuales`, `Tasa de despacho`, `Costo variable reparto` |
| `Costo de vehiculo` | `Gatillo reactivo`, `Inversion en capacidad` | — |
| `Margen acumulado` | `Gatillo reactivo` | `Ingresos por ventas`, `Costo de compra`, `Costos operacionales`, `Inversion en capacidad` (INTEG) |
| `Tiempo` | `Estacionalidad`, `Disponibilidad proveedor`, `Gatillo proactivo` | — (INTEG de constante 1) |
| `Mes de compra` | `Gatillo proactivo` | — |
| `Politica proactiva` | `Gatillo activo` | — |
| `Gatillo reactivo` | `Gatillo activo` | `Margen acumulado`, `Costo de vehiculo`, `Tasa de incumplimiento` |
| `Gatillo proactivo` | `Gatillo activo` | `Tiempo`, `Mes de compra` |
| `Gatillo activo` | `Pulso de compra` | `Politica proactiva`, `Gatillo reactivo`, `Gatillo proactivo` |
| `Vehiculo comprado` | `Pulso de compra` (INTEG) | `Pulso de compra` (INTEG) |
| `Pulso de compra` | `Vehiculo comprado`, `Inversion en capacidad` | `Gatillo activo`, `Vehiculo comprado` |
| `Incremento cap por CLP` | `Capacidad de reparto` (INTEG) | — |
| `Inversion en capacidad` | `Margen acumulado`, `Capacidad de reparto` (INTEG) | `Pulso de compra`, `Costo de vehiculo` |

---

## 8. Herramienta Vensim por variable — resumen rápido

| Herramienta | Variables |
|-------------|-----------|
| **Stock / Box Variable (Level)** | `Demanda base`, `Stock de huevos`, `Capacidad de reparto`, `Margen acumulado`, `Vehiculo comprado`, `Tiempo` |
| **Rate / Flow** | `Tasa de captacion`, `Tasa de perdida de clientes`, `Tasa de compra`, `Tasa de despacho`, `Ingresos por ventas`, `Costo de compra`, `Pulso de compra`, `Inversion en capacidad` |
| **Auxiliary** | `Demanda total`, `Tasa de incumplimiento`, `Necesidad de compra`, `Inventario Objetivo`, `Costos fijos mensuales`, `Costos operacionales`, `Gatillo reactivo`, `Gatillo proactivo`, `Gatillo activo` |
| **Auxiliary con WITH LOOKUP** | `Tasa de fuga logistica`, `Estacionalidad`, `Disponibilidad proveedor` |
| **Constant** | `Tasa crecimiento base`, `Precio de venta`, `Precio de compra`, `Costo de vehiculo`, `Incremento cap por CLP`, `Costo variable reparto`, `Costo fijo mantenimiento`, `Mes de compra`, `Politica proactiva`, `Paso de tiempo`, `Demanda minima` *(pendiente)*, `Capacidad maxima proveedor` *(pendiente)* |

---

## 9. Brechas de información pendientes (heredadas de la propuesta original + nuevas de esta versión)

1. **Tasa de fuga real de clientes** — el lookup actual es una estimación razonable pero no calibrada con datos del negocio. Si tienen registros de clientes que dejaron de comprar tras un atraso, esto se puede ajustar.
2. **Crecimiento orgánico mensual (2%)** — verificar contra el historial de clientes nuevos fuera de temporada alta.
3. **Costo real de chofer/mantención adicional** — ajustar `Costo fijo mantenimiento` con una cotización real de la zona.
4. **`Demanda minima` y `Capacidad maxima proveedor`** *(nuevo)* — ambas están referenciadas en las ecuaciones de la sección 5 (`Tasa de perdida de clientes` y `Tasa de compra`, respectivamente) pero todavía no tienen un valor asignado en el bloque de constantes. Hay que definirlas antes de correr la simulación completa, o Vensim arrojará error de variable sin definir al hacer Check Model.
5. **Precio de venta y de compra (33.000 / 24.000 CLP/caja)** *(nuevo)* — confirmar que coinciden con el precio promedio real por caja en 2025. Los datos de [DATOS_HISTORICOS.md](./DATOS_HISTORICOS.md) están en CLP totales mensuales, no en CLP/caja, así que falta el dato de cantidad de cajas mensuales para hacer la división y validar la calibración.

---

*Modelo basado en la propuesta del compañero, con correcciones técnicas para evitar gasto repetido de inversión, una lógica de reposición de inventario hacia un objetivo, y horizonte de simulación extendido a 24 meses.*
*Proyecto final — Teoría de Sistemas.*