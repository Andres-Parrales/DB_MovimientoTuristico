
---

### 2. `SCHEMA/README.md`

```markdown
# 📐 Arquitectura del Warehouse: Star Schema

Modelo de datos optimizado para la analítica del sector turístico. El diseño sigue el principio de **Single Source of Truth (SSOT)**.



### Capas del Ecosistema
| Categoría | Tablas Principales | Rol |
| :--- | :--- | :--- |
| **Dimensiones** | `clientes`, `destinos`, `tours` | Datos descriptivos y atributos del viaje. |
| **Hechos** | `reservas` | Métrica central de ventas y volumen transaccional. |
| **Calidad** | `evaluaciones`, `pagos` | Indicadores de satisfacción y flujo financiero. |

* **Integridad ACID:** Garantizada mediante llaves foráneas (`FK`) con reglas `ON DELETE RESTRICT`.
* **BI Ready:** Esquema preparado para integraciones con **Power BI / Tableau** mediante la tabla `calendario`.