# 🚗 Propuesta de Proyecto — Dinámica de Sistemas en una App de Transporte Compartido
---

# El problema

Una aplicación local de transporte compartido conecta actualmente a:

- Estudiantes universitarios
- Trabajadores de oficina
- Usuarios nocturnos de fin de semana
- Clientes frecuentes en sectores céntricos
- Conductores independientes registrados en la plataforma

El problema central: en horarios punta y fines de semana, la demanda de viajes aumenta rápidamente, pero la cantidad de conductores disponibles no crece al mismo ritmo. Esto provoca largos tiempos de espera, cancelaciones y pérdida de usuarios hacia aplicaciones competidoras.

Además, durante eventos masivos y períodos de alta congestión, los conductores tienden a desconectarse debido al tráfico o baja rentabilidad percibida, empeorando aún más el servicio.

La pregunta que guía el modelo es:

> ¿Cuándo conviene aumentar incentivos o incorporar más conductores, y cómo afecta esa decisión la rentabilidad y calidad del servicio en el tiempo?

---

# Subsistemas identificados

El sistema se divide en dos subsistemas claramente diferenciados, cumpliendo el requisito mínimo del proyecto.

---

# 🚘 Subsistema 1 — Operacional / Servicio

Agrupa las variables relacionadas con el funcionamiento diario de la plataforma y la operación de los viajes.

| Variable                      | Descripción                                  |
|-------------------------------|----------------------------------------------|
| Conductores activos           | Conductores conectados y disponibles         |
| Solicitudes de viaje          | Viajes solicitados por usuarios              |
| Viajes completados            | Cantidad de trayectos realizados             |
| Tiempo promedio de espera     | Minutos que espera el pasajero               |
| Cancelaciones                 | Viajes cancelados por usuarios o conductores |
| Tráfico vehicular             | Nivel de congestión urbana                   |
| Horarios punta                | Factor temporal que aumenta demanda          |
| Distancia promedio de viaje   | Trayecto medio recorrido                     |
| Disponibilidad de conductores | Relación entre oferta y demanda              |
| Satisfacción del usuario      | Percepción de calidad del servicio           |

---

# 💰 Subsistema 2 — Financiero / Crecimiento

Agrupa las variables relacionadas con ingresos, costos y expansión de la plataforma.

| Variable                     | Descripción                          |
|------------------------------|--------------------------------------|
| Ingresos por viajes          | Comisión obtenida por trayecto       |
| Tarifas dinámicas            | Ajuste de precio según demanda       |
| Incentivos a conductores     | Bonos para aumentar disponibilidad   |
| Costos operacionales         | Servidores, soporte y marketing      |
| Usuarios activos             | Clientes frecuentes de la app        |
| Conductores registrados      | Total de conductores afiliados       |
| Inversión en publicidad      | Captación de usuarios y conductores  |
| Ganancia acumulada           | Diferencia entre ingresos y costos   |
| Tasa de abandono de usuarios | Usuarios que dejan la plataforma     |
| Capacidad de expansión       | Posibilidad de crecer a nuevas zonas |

---

**Total: 20 variables → cumple ampliamente el mínimo de 10 exigido.**

---

# Bucles de retroalimentación

El sistema tiene al menos tres bucles identificables, cumpliendo el requisito mínimo.

---

## ➕ Bucle R1 — Crecimiento de la plataforma (Refuerzo)

Margen acumulado → Mayor inversión en publicidad e incentivos  
→ Más conductores registrados  
→ Mayor disponibilidad de viajes  
→ Menor tiempo de espera  
→ Mayor satisfacción de usuarios  
→ Más usuarios activos  
→ Más solicitudes de viaje  
→ Más ingresos  
→ Mayor margen acumulado

---

## ➖ Bucle B1 — Saturación del servicio (Balanceo)

Aumento de solicitudes  
→ Menos conductores disponibles  
→ Mayor tiempo de espera  
→ Más cancelaciones  
→ Disminución de satisfacción  
→ Pérdida de usuarios

---

## ➖ Bucle B2 — Congestión y rentabilidad (Balanceo)

Mayor tráfico vehicular  
→ Viajes más largos  
→ Menor cantidad de viajes por conductor  
→ Menor rentabilidad para conductores  
→ Conductores se desconectan  
→ Menor disponibilidad del servicio

---

# Escenarios de simulación

| Escenario | Descripción                                                                                                         |
|-----------|---------------------------------------------------------------------------------------------------------------------|
| Base      | Operación actual: cantidad fija de conductores, sin incentivos dinámicos y tarifas normales                         |
| Mejora    | Implementación de incentivos automáticos en horarios punta + tarifas dinámicas + campañas para reclutar conductores |

La comparación permite responder:

> ¿La inversión en incentivos y expansión mejora suficientemente la disponibilidad y ganancias como para justificar su costo operativo?

---

# Estructura del informe (check de requisitos)

| Sección requerida                | ¿Cubierta?                                                       |
|----------------------------------|------------------------------------------------------------------|
| Portada                          | ✅                                                               |
| Resumen                          | ✅                                                               |
| Introducción                     | ✅                                                               |
| Definiciones y marco teórico     | ✅                                                               |
| Definición del problema          | ✅ — problema urbano y tecnológico real                          |
| Identificación de subsistemas    | ✅ — 2 subsistemas definidos                                     |
| Identificación de variables      | ✅ — 20 variables identificadas                                  |
| Influencias de 1°, 2° y 3° orden | ✅                                                               |
| Diagrama causal                  | ✅                                                               |
| Bucles de retroalimentación      | ✅ — 3 bucles identificados                                      |
| Datos históricos y supuestos     | ✅ — datos públicos de movilidad urbana y supuestos justificados |
| Diagrama de Forrester            | ✅                                                               |
| Construcción del modelo          | ✅                                                               |
| Simulación escenario base        | ✅                                                               |
| Propuesta de intervención        | ✅ — incentivos y tarifas dinámicas                              |
| Simulación escenario de mejora   | ✅                                                               |
| Resultados                       | ✅                                                               |
| Conclusiones                     | ✅                                                               |
| Referencias APA 7                | ✅                                                               |

---

# Datos y fuentes posibles

El modelo puede respaldarse usando:

- Datos de congestión urbana
- Datos de movilidad pública
- APIs de mapas y tráfico
- Reportes de apps de transporte
- Estudios de tiempos de viaje urbanos
- Datos municipales de tránsito

También pueden utilizarse supuestos razonables como:

- Tiempo promedio de espera inicial
- Cantidad estimada de conductores activos
- Tasa de cancelación promedio
- Incremento de demanda en horarios punta

---

# Herramienta de simulación sugerida

Se propone usar:

- Python (`numpy`, `matplotlib`, `pandas`)
o
- Vensim

Python tiene la ventaja de permitir:

- simulaciones dinámicas,
- gráficos personalizados,
- análisis de escenarios,
- y reutilización futura del modelo como herramienta de negocio.

---

# Próximos pasos si se aprueba la propuesta

1. Levantar datos históricos o estimados:
   - tiempos de espera,
   - demanda por horarios,
   - tráfico,
   - número de conductores.

2. Definir valores iniciales de las variables.

3. Construir el diagrama causal y el diagrama de Forrester.

4. Implementar el modelo en Python o Vensim.

5. Simular:
   - escenario base,
   - escenario con incentivos,
   - escenario con expansión.

6. Analizar:
   - rentabilidad,
   - satisfacción de usuarios,
   - estabilidad del sistema,
   - crecimiento sostenible de la plataforma.
