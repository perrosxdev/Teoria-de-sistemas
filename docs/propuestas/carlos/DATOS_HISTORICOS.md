# 📊 Datos Históricos — Distribuidora de Huevos (solo 2025)

[← Volver a la Propuesta del Proyecto](./PROPUESTA.md)

## Fuente de los datos

Los datos corresponden a registros reales de compras y ventas del negocio, expresados en pesos chilenos (CLP), con IVA. Este documento contiene exclusivamente los registros del año **2025** para uso en la calibración del modelo.

---

## 🛒 Compras al proveedor (2025)

| Año  | Mes        | Monto (con IVA)     |
|------|------------|--------------------:|
| 2025 | Enero      | CLP 10.949.251      |
| 2025 | Febrero    | CLP 8.696.410       |
| 2025 | Marzo      | CLP 6.300.765       |
| 2025 | Abril      | CLP 5.646.407       |
| 2025 | Mayo       | CLP 6.418.327       |
| 2025 | Junio      | CLP 5.290.740       |
| 2025 | Julio      | CLP 5.033.491       |
| 2025 | Agosto     | CLP 3.925.841       |
| 2025 | Septiembre | CLP 3.894.156       |
| 2025 | Octubre    | CLP 6.619.672       |
| 2025 | Noviembre  | CLP 5.227.146       |
| 2025 | Diciembre  | CLP 8.988.437       |
| **TOTAL 2025** |       | **CLP 76.990.643** |

---

## 🧾 Ventas y Ganancia Líquida (2025)

| Año  | Mes        | Monto (con IVA)     | Ganancia Líquida    |
|------|------------|--------------------:|--------------------:|
| 2025 | Enero      | CLP 13.948.263      | CLP 2.520.178       |
| 2025 | Febrero    | CLP 13.771.471      | CLP 4.264.757       |
| 2025 | Marzo      | CLP 6.403.502       | CLP 86.334          |
| 2025 | Abril      | CLP 5.946.503       | CLP 252.182         |
| 2025 | Mayo       | CLP 6.829.576       | CLP 345.587         |
| 2025 | Junio      | CLP 5.672.716       | CLP 320.988         |
| 2025 | Julio      | CLP 6.351.411       | CLP 1.107.496       |
| 2025 | Agosto     | CLP 5.061.587       | CLP 954.408         |
| 2025 | Septiembre | CLP 5.241.099       | CLP 1.131.885       |
| 2025 | Octubre    | CLP 6.929.610       | CLP 260.452         |
| 2025 | Noviembre  | CLP 5.363.514       | CLP 114.595         |
| 2025 | Diciembre  | CLP 9.637.905       | CLP 545.771         |
| **TOTAL 2025** |       | **CLP 91.157.157** | **CLP 11.904.633**  |

---

## 📌 Observaciones relevantes para el modelo

- **Estacionalidad visible:** Los meses de enero y febrero concentran los mayores volúmenes tanto de compra como de venta, consistente con el peak de verano descrito en la propuesta.
- **Margen variable:** La ganancia líquida mensual fluctúa significativamente — desde CLP 86.334 (marzo 2025) hasta CLP 4.264.757 (febrero 2025) — lo que refleja la sensibilidad del negocio al precio del proveedor y al volumen despachado.
- **Ganancia líquida acumulada (2025):** CLP 11.904.633
- **Margen promedio sobre ventas (con IVA):** ~13,1% (ganancia acumulada / ventas con IVA)

---

> _Datos levantados del sistema de gestión del negocio real. Usados como valores iniciales y de calibración para el modelo de dinámica de sistemas._
