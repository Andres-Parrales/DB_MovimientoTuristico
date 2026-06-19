# 📐 Arquitectura del Warehouse: Star Schema

> Diseño lógico de base de datos optimizado para analítica avanzada en el sector turístico.



---

## 🏗️ Estructura del Ecosistema
El modelo sigue el principio de **Single Source of Truth (SSOT)**, garantizando que cada dato tenga un origen único y confiable.

| Categoría | Tablas Principales | Propósito Analítico |
| :--- | :--- | :--- |
| 🏷️ **Dimensiones** | `clientes`, `destinos`, `tours` | Segmentación y atributos del viaje. |
| 📈 **Hechos** | `reservas` | Registro central de ventas y métricas de volumen. |
| 💎 **Calidad/Financiero** | `evaluaciones`, `pagos` | Seguimiento de satisfacción y flujo de caja. |

---

## 🛠️ Especificaciones Técnicas

### 🛡️ Integridad y Seguridad
* **ACID Compliance:** Implementación de motores InnoDB para garantizar transacciones atómicas.
* **Referential Integrity:** Uso estricto de llaves foráneas (`FK`) con reglas `ON DELETE RESTRICT` y `ON UPDATE CASCADE`, evitando la creación de registros huérfanos.

### 📊 Preparación para BI (Business Intelligence)
El modelo incluye una **tabla `calendario` (Date Dimension)**, fundamental para el análisis temporal:
* Permite realizar comparativas de **Year-over-Year (YoY)**.
* Facilita la creación de jerarquías automáticas en herramientas como **Power BI** o **Tableau**.

---

## 💡 ¿Por qué este modelo?
1. **Desacoplamiento:** La separación entre dimensiones (atributos) y hechos (transacciones) permite realizar consultas complejas sin degradar el rendimiento.
2. **Escalabilidad:** El esquema está preparado para integrar nuevas dimensiones (ej. `agencias_viajes`, `promociones`) sin necesidad de reestructurar la tabla central.

---
[⬅️ Volver al README principal](../README.md)
