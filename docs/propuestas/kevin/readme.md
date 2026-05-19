# 🛒 Propuesta de Proyecto — Dinámica de Sistemas en el Cierre de Minimarkets Locales

[← Volver al README principal](../../../README.md)

## El problema

Un minimarket de barrio en la Región de La Araucanía opera actualmente atendiendo a:

- Clientes habituales del sector residencial
- Trabajadores de comercios y servicios cercanos
- Familias de sectores populares con preferencia por compra diaria
- Clientes ocasionales de paso

**El problema central:** la llegada progresiva de grandes cadenas de supermercados (Unimarc, Lider, Jumbo) a ciudades como Temuco, Angol y Victoria ha generado una presión competitiva sostenida sobre los minimarkets locales. La diferencia en precios, variedad y horario erosiona gradualmente la base de clientes del negocio pequeño, comprometiendo su viabilidad en el mediano plazo.

A esto se suma que el minimarket no cuenta con estrategias formales de fidelización ni acceso a crédito para modernizar su operación, lo que profundiza la brecha competitiva con el tiempo.

La pregunta que guía el modelo es:

> **¿En cuánto tiempo el ingreso de una cadena de supermercados al barrio lleva al cierre de un minimarket local, y qué estrategias de diferenciación permiten retrasar o revertir ese proceso?**

---

## Subsistemas identificados

El sistema se divide en dos subsistemas claramente diferenciados, cumpliendo el requisito mínimo del proyecto:

### 🏪 Subsistema 1 — Operacional / Comercial

Agrupa las variables relacionadas con el flujo de clientes, ventas y la capacidad del minimarket para sostener su operación cotidiana.

| Variable | Descripción |
|----------|-------------|
| Clientes activos | Número de compradores frecuentes que mantienen el minimarket como primera opción |
| Tasa de captación de clientes | Nuevos clientes atraídos por cercanía, trato personalizado o crédito informal |
| Tasa de deserción de clientes | Clientes que migran hacia la cadena competidora por precio o variedad |
| Volumen de ventas mensual | Unidades o monto total vendido por período |
| Nivel de stock disponible | Inventario en bodega; afecta la capacidad de respuesta a la demanda |
| Presión competitiva | Variable que modula la tasa de deserción según la proximidad y tamaño del competidor |
| Diferenciación percibida | Factor que representa ventajas del minimarket: cercanía, fiado, horario extendido, trato |

### 💰 Subsistema 2 — Financiero / Viabilidad

Agrupa las variables relacionadas con ingresos, costos y la capacidad del negocio para mantenerse operativo o adaptarse.

| Variable | Descripción |
|----------|-------------|
| Ingresos por ventas | Función del volumen vendido y precio promedio |
| Precio de venta promedio | Generalmente más alto que las cadenas; puede ajustarse con márgenes |
| Costos operacionales | Arriendo, servicios básicos, reposición de stock, personal familiar |
| Margen acumulado | Diferencia entre ingresos y costos en el tiempo |
| Capacidad de reinversión | Umbral de margen que permite reponer stock, mejorar local o implementar estrategias |
| Deuda o crédito informal | Pasivo acumulado por compras al proveedor o préstamos para sostener operación |
| Decisión de cierre | Variable que se activa cuando el margen acumulado cae por debajo de un umbral crítico sostenido |

> Total: **14 variables** → cumple holgadamente el mínimo de 10 exigido.

---

## Bucles de retroalimentación

El sistema tiene al menos tres bucles identificables, cumpliendo el requisito mínimo:

### ➕ Bucle R1 — Fidelización y diferenciación (Refuerzo)
```
Mayor diferenciación percibida → Menor tasa de deserción → Más clientes activos
→ Mayor volumen de ventas → Mayores ingresos → Mayor capacidad de reinversión
→ Mejoras en el local o servicio → Mayor diferenciación percibida
```

### ➖ Bucle B1 — Espiral de pérdida de clientes (Balanceo)
```
Entrada de cadena competidora → Aumento de presión competitiva → Mayor deserción de clientes
→ Menor volumen de ventas → Menores ingresos → Menor capacidad de reponer stock
→ Quiebres de stock → Más deserción de clientes
```

### ➖ Bucle B2 — Tensión precio-fidelidad (Balanceo)
```
Intento de bajar precios para competir → Reducción del margen por unidad
→ Menor margen acumulado → Menor capacidad de reinversión → Deterioro del local o servicio
→ Menor diferenciación percibida → Mayor deserción de clientes
```

---

## Escenarios de simulación

| Escenario | Descripción |
|-----------|-------------|
| **Base** | Operación actual sin cambios: el minimarket mantiene su forma de operar tras la llegada de la cadena, sin estrategia de diferenciación ni inversión adicional |
| **Mejora** | Implementación de estrategias de fidelización: crédito informal controlado, horario extendido, entrega a domicilio local y mejora del trato personalizado |

La comparación permite responder: *¿cuánto tiempo sobrevive el minimarket sin intervención, y en qué medida las estrategias de diferenciación extienden o aseguran su viabilidad?*

---

## Estructura del informe (check de requisitos)

| Sección requerida | ¿Cubierta? |
|------------------|-----------|
| Portada | ✅ |
| Resumen | ✅ |
| Introducción | ✅ |
| Definiciones y marco teórico | ✅ |
| Definición del problema | ✅ — fenómeno observable en ciudades de La Araucanía |
| Identificación de subsistemas | ✅ — 2 subsistemas definidos |
| Identificación de variables | ✅ — 14 variables identificadas |
| Influencias de 1°, 2° y 3° orden | ✅ |
| Diagrama causal | ✅ |
| Bucles de retroalimentación | ✅ — 3 bucles identificados |
| Datos históricos y supuestos | ✅ — datos INE, SII, encuestas de comercio minorista regional |
| Diagrama de Forrester | ✅ |
| Construcción del modelo | ✅ |
| Simulación escenario base | ✅ |
| Propuesta de intervención | ✅ — estrategias de diferenciación y fidelización |
| Simulación escenario de mejora | ✅ |
| Resultados | ✅ |
| Conclusiones | ✅ |
| Referencias APA 7 | ✅ |

> **Todo el esqueleto del informe está cubierto desde el diseño del problema.**

---

## Herramienta de simulación sugerida

Se propone usar **Python** (con librerías `numpy` y `matplotlib`) o **Vensim** para la simulación, ambas aceptadas por el enunciado. Python tiene la ventaja de que el modelo queda como un script reutilizable y permite visualizar fácilmente la evolución temporal de las variables clave.

---

## Próximos pasos si se aprueba la propuesta

1. Levantar datos de referencia: número de minimarkets en Temuco o Angol según SII y municipios
2. Definir valores iniciales de cada variable (clientes base, ingresos estimados, costos típicos)
3. Construir el diagrama causal y de Forrester
4. Implementar el modelo en Python o Vensim
5. Correr los dos escenarios y analizar resultados comparativos

---

> _Propuesta elaborada para discusión grupal previa a la entrega del 29 de mayo._
