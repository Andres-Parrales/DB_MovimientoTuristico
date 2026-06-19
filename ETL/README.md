#  Pipeline ETL: Ingesta y Transformación

Proceso automatizado para la carga de datos sintéticos de alta fidelidad, diseñado para escalabilidad analítica.



##  Métricas de Generación (Data Scale)
| Entidad | Volumen | Complejidad |
| :--- | :--- | :--- |
| **Reservas** | 50,000 | Alta (Cálculos de totales y descuentos). |
| **Clientes** | 5,000 | Perfiles únicos con metadata geográfica. |
| **Tours** | 500 | Catálogo segmentado por categoría y destino. |
| **Evaluaciones** | 35,000 | Generación probabilística (70% de tasa de respuesta). |

##  Especificaciones Técnicas
* **Calidad de Datos:** Validación de tipos y recortes preventivos en `VARCHAR` para evitar errores de truncamiento (`Data too long`).
* **Resiliencia:** Uso de `try-except` con logs detallados mediante `tqdm` para monitorizar el progreso en tiempo real.
* **Orquestación:** Carga secuencial por niveles de dependencia para garantizar la integridad referencial.

##  El Valor Agregado
1. **Modelado Dimensional:** Diseño de estructuras de datos orientadas a la analítica (KPIs de venta).
2. **Ingeniería ETL:** Desarrollo de scripts modulares, robustos y fáciles de mantener.
3. **Visión de Negocio:** Capacidad para transformar datos crudos en métricas de satisfacción del cliente y rendimiento operativo.
