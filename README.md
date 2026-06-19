# TurismoAnalytics V1.0: Core de Inteligencia Turística

Ecosistema de datos diseñado para el análisis del ciclo de vida del viajero, desde la reserva hasta la evaluación de servicios.

![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![Model](https://img.shields.io/badge/Model-Star_Schema-blue)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20SQL%20%7C%20ETL-orange)

---

## Guía de Despliegue Profesional

### 1. Entorno de Ejecución y Dependencias

Para ejecutar el pipeline, se requiere **Python 3.x** y las siguientes librerías:

```bash
pip install pandas sqlalchemy pymysql faker tqdm
```

### 2. Estructura de Datos

Inicializa el motor de base de datos ejecutando el script de esquema:

```sql
SOURCE SCHEMA/schema_turismo.sql;
```

### 3. Orquestación del Pipeline

Edita los parámetros de conexión en:

```text
ETL/pipeline_turismo.py
```

```python
USER = "tu_usuario"
PASSWORD = "tu_password"
HOST = "localhost"
DB = "turismo_analytics"
```

Ejecuta el proceso de carga:

```bash
python ETL/pipeline_turismo.py
```

---

## Detalle Técnico

### Esquema

Modelo dimensional orientado al análisis de datos turísticos y la construcción de indicadores estratégicos.

### Pipeline ETL

Proceso automatizado encargado de la generación, transformación y carga de datos sintéticos hacia la base de datos analítica.

---

## Análisis de Implementación

El desarrollo de este sistema permitió profundizar en la generación de datos sintéticos de alta fidelidad. El reto técnico fue asegurar que las relaciones entre dimensiones y hechos mantuvieran una integridad absoluta, garantizando que el modelo sea apto para análisis de BI complejos.

Este proyecto consolida mi capacidad para diseñar estructuras de datos escalables que facilitan la extracción de indicadores clave.

---

## Roadmap de Mejora

### Calidad de Datos

Implementar pruebas de calidad de datos automatizadas para monitorear la integridad durante la ingesta.

### Escalabilidad

Migrar la infraestructura hacia una arquitectura basada en microservicios para mejorar la concurrencia en la carga de grandes volúmenes de datos.
