# 🏬 Propuesta de Proyecto — Dinámica de Sistemas en la Pérdida de Liquidez por Desalineación de Inventario en Micro-PyMEs Comerciales de Temuco

[← Volver al README principal](../../../README.md)

## El problema

Una micro-pyme comercial de Temuco opera actualmente vendiendo productos de consumo masivo o vestuario a:

- Clientes habituales del sector donde se ubica el local
- Compradores ocasionales atraídos por precio o cercanía
- Clientes de temporada según rubro (escolar, invierno, fiestas, etc.)
- Pequeños revendedores informales de la zona

**El problema central:** el dueño del negocio toma decisiones de compra de inventario basándose en la intuición y en lo que se vendía antes, sin estudiar las tendencias actuales del mercado local. Esto genera una acumulación progresiva de mercadería que no tiene salida — el llamado inventario "hueso" — que congela el capital de trabajo y destruye la liquidez del negocio mes a mes.

A esto se suma que, al no tener caja disponible, la pyme tampoco puede comprar los productos que el mercado de Temuco sí está pidiendo en ese momento, profundizando el problema en un círculo vicioso que termina en insolvencia técnica o cierre.

La pregunta que guía el modelo es:

> **¿En cuántos meses una micro-pyme comercial de Temuco queda en insolvencia por acumulación de inventario obsoleto, y qué estrategia de liquidación y lectura de mercado permite revertir ese proceso?**

---

## Subsistemas identificados

El sistema se divide en dos subsistemas claramente diferenciados, cumpliendo el requisito mínimo del proyecto:

### 📦 Subsistema 1 — Rotación de Inventario (Logístico)

Agrupa las variables relacionadas con el flujo físico de productos en bodega, distinguiendo entre mercadería con salida real y mercadería acumulada que no se vende.

| Variable | Descripción |
|----------|-------------|
| Inventario inmovilizado ("hueso") | Stock acumulado de productos sin salida por obsolescencia, temporada vencida o cambio en la demanda local |
| Tasa de compras erróneas | Volumen de productos adquiridos mensualmente sin respaldo en datos de mercado; depende del índice de desalineación |
| Tasa de liquidación o pérdida | Productos rematados bajo el costo o desechados para liberar espacio y recuperar parte del capital |
| Tiempo promedio de obsolescencia | Parámetro que define en cuántos días un producto sin movimiento pasa a considerarse "hueso" |
| Espacio físico de bodega | Restricción física que, al saturarse, obliga a liquidar antes de reponer |
| Índice de desalineación con el mercado | Variable auxiliar que representa qué tan desconectadas están las decisiones de compra de la demanda real; aumenta cuando no hay presupuesto para estudiar tendencias |

### 💰 Subsistema 2 — Flujo de Caja y Capacidad de Reinversión (Financiero)

Agrupa las variables relacionadas con la salud financiera del negocio, mostrando cómo el capital atrapado en inventario destruye la liquidez operacional.

| Variable | Descripción |
|----------|-------------|
| Capital de trabajo disponible (caja) | Dinero líquido disponible para operar: pagar proveedores, costos fijos y reponer stock |
| Recaudación por ventas efectivas | Ingresos reales generados únicamente por los productos que el mercado sí demanda |
| Costos de almacenamiento y pérdidas financieras | Dinero drenado mensualmente en arriendo de bodega, mermas y costo de oportunidad del capital congelado |
| Margen de ganancia de productos estrella | Parámetro que define la rentabilidad de los productos con salida real |
| Costos fijos mensuales | Arriendo del local, servicios básicos, remuneraciones; se pagan independiente del nivel de ventas |
| Presupuesto asignado a estudio de mercado | Variable que modula el índice de desalineación; si la caja cae, este ítem se elimina primero |
| Umbral de insolvencia | Nivel mínimo de caja por debajo del cual el negocio no puede cubrir sus costos fijos; activa el cierre técnico |

> Total: **13 variables** → cumple holgadamente el mínimo de 10 exigido.

---

## Bucles de retroalimentación

El sistema tiene tres bucles identificables, cumpliendo el requisito mínimo:

### ➕ Bucle R1 — Círculo vicioso de desalineación (Refuerzo)
```
Mala lectura de mercado → Aumenta inventario inmovilizado
→ Aumentan costos de almacenamiento → Disminuye capital de trabajo (caja)
→ Menos presupuesto para estudiar el mercado → Mayor índice de desalineación
→ Más compras erróneas → Más inventario inmovilizado
```

### ➖ Bucle B1 — Liquidación como válvula de escape (Balanceo)
```
Inventario inmovilizado supera umbral de espacio → Se activa liquidación agresiva
→ Recupera parte del capital → Aumenta caja disponible
→ Permite comprar productos con demanda real → Reduce inventario hueso
```

### ➕ Bucle R2 — Círculo virtuoso por ventas efectivas (Refuerzo)
```
Mayor alineación con el mercado → Más productos con salida real
→ Mayor recaudación por ventas efectivas → Mayor caja disponible
→ Mayor presupuesto para estudio de mercado → Menor índice de desalineación
→ Mejores decisiones de compra → Más productos con salida real
```

---

## Escenarios de simulación

| Escenario | Descripción |
|-----------|-------------|
| **Base** | Sin intervención: el dueño sigue comprando por intuición, el inventario hueso crece mes a mes, la caja se drena progresivamente hasta caer bajo el umbral de insolvencia en un horizonte de 6 a 12 meses |
| **Mejora** | Se introduce una regla de liquidación automática (si un producto supera X días sin movimiento, se remata al costo) y un presupuesto mínimo fijo para lectura de mercado, permitiendo que la caja se recupere y el ciclo vicioso se quiebre |

La comparación permite responder: *¿en cuántos meses quiebra técnicamente la pyme sin intervención, y en cuánto tiempo la estrategia de mejora estabiliza la caja y recupera la rentabilidad?*

---

## Estructura del informe (check de requisitos)

| Sección requerida | ¿Cubierta? |
|------------------|-----------|
| Portada | ✅ |
| Resumen | ✅ |
| Introducción | ✅ |
| Definiciones y marco teórico | ✅ |
| Definición del problema | ✅ — fenómeno documentado en micro-pymes comerciales de La Araucanía |
| Identificación de subsistemas | ✅ — 2 subsistemas definidos |
| Identificación de variables | ✅ — 13 variables identificadas |
| Influencias de 1°, 2° y 3° orden | ✅ |
| Diagrama causal | ✅ |
| Bucles de retroalimentación | ✅ — 3 bucles identificados (2 de refuerzo, 1 de balanceo) |
| Datos históricos y supuestos | ✅ — supuestos justificados con datos de SERCOTEC, INE y literatura de gestión de inventarios |
| Diagrama de Forrester | ✅ |
| Construcción del modelo | ✅ |
| Simulación escenario base | ✅ |
| Propuesta de intervención | ✅ — liquidación automática + presupuesto fijo de lectura de mercado |
| Simulación escenario de mejora | ✅ |
| Resultados | ✅ |
| Conclusiones | ✅ |
| Referencias APA 7 | ✅ |

> **Todo el esqueleto del informe está cubierto desde el diseño del problema.**

---

## Supuestos base del modelo

Dado que no se trabaja con una tienda específica, se plantea un caso hipotético representativo de una micro-pyme comercial de Temuco, justificado con fuentes públicas:

| Parámetro | Valor inicial supuesto | Fuente de referencia |
|-----------|----------------------|----------------------|
| Capital de trabajo inicial (caja) | $2.000.000 CLP | SERCOTEC — capital promedio micro-pyme comercial |
| Inventario inicial (unidades) | 500 artículos | Supuesto razonable para local de 30–50 m² |
| Costos fijos mensuales | $800.000 CLP | INE — encuesta de microempresas, rubro comercio |
| Tiempo de obsolescencia promedio | 60 días | Literatura de gestión de inventarios (Chopra & Meindl) |
| Índice de desalineación inicial | 0,4 (escala 0–1) | Supuesto; representa decisiones mayormente intuitivas |
| Margen de productos estrella | 30% | Estimación típica para comercio minorista local |

> Todos los supuestos serán explicitados y justificados en la sección correspondiente del informe.

---

## Herramienta de simulación sugerida

Se propone usar **Python** (con librerías `numpy` y `matplotlib`) para la simulación. Python permite implementar el modelo como un sistema de ecuaciones diferenciales discretas, visualizar la evolución temporal de la caja y el inventario hueso, y comparar ambos escenarios en un mismo gráfico. El script queda además como entregable reutilizable.

Como alternativa, **Vensim** o **Insight Maker** son igualmente válidos si el grupo prefiere una interfaz visual para construir el diagrama de Forrester directamente.

---

## Planificación en 4 semanas

| Semana | Actividades |
|--------|-------------|
| **Semana 1** (29 may – 4 jun) | Entregar propuesta · Definir valores iniciales · Revisar fuentes bibliográficas |
| **Semana 2** (5 – 11 jun) | Construir diagrama causal y de Forrester · Implementar modelo base en Python o Vensim |
| **Semana 3** (12 – 18 jun) | Correr escenario base y de mejora · Analizar resultados · Redactar secciones técnicas |
| **Semana 4** (19 – 27 jun) | Redactar informe completo en LaTeX · Preparar presentación · Revisión final |

> Entrega definitiva: **28 de junio, 23:55 hrs.**

---

## Próximos pasos si se aprueba la propuesta

1. Confirmar valores iniciales de cada variable con fuentes de SERCOTEC e INE
2. Definir la fórmula del índice de desalineación con el mercado
3. Construir el diagrama causal y de Forrester
4. Implementar el modelo en Python o Vensim
5. Correr ambos escenarios y analizar el punto de quiebre técnico vs. punto de estabilización

---

> _Propuesta elaborada para discusión grupal previa a la entrega del 29 de mayo._
