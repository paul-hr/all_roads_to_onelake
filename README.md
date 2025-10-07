# Ejemplos de Integración y Gestión de Datos con OneLake

Este repositorio contiene ejemplos prácticos de integración y gestión de datos utilizando OneLake de Microsoft Fabric. Los ejemplos demuestran varios casos de uso y escenarios para el manejo eficiente de datos en entornos empresariales.

## Descripción General

OneLake proporciona una solución de almacenamiento unificada que elimina los silos de datos, permite el intercambio fluido de datos entre espacios de trabajo y ofrece patrones de acceso familiares para profesionales de datos de todo tipo.

## Beneficios Clave de OneLake

- **Almacenamiento Unificado:** Todos los datos en un lugar, eliminación de silos de datos, formato Delta estandarizado
- **Poder de los Accesos Directos:** Sin duplicación de datos, acceso inmediato a fuentes externas, gobernanza unificada
- **Experiencia Familiar:** Integración nativa con Explorador de Archivos, compatibilidad con API ADLS Gen2, autoservicio para usuarios
- **Rendimiento y Eficiencia de Costos:** Separación de cómputo/almacenamiento, modelo de pago por uso, optimización automática

## Casos de Uso

### Caso 1: Intercambio de Datos Multifuncional

Este ejemplo demuestra cómo una sola copia de datos puede ser utilizada en múltiples espacios de trabajo a través de accesos directos de OneLake.

**Estructura:**

```
ESPACIOS DE TRABAJO:
├── ventas-analytics
│   ├── ventas_diarias (Trabajo de Copia desde Azure SQL)
│   ├── catalogo_productos (Carga manual)
│   └── Panel de Power BI
│
├── marketing-insights
│   ├── Acceso Directo → ventas_diarias (desde ventas-analytics)
│   ├── datos_campanas (Carga manual)
│   └── Análisis de segmentación de clientes
│
└── panel-ejecutivo
    ├── Acceso Directo → ventas_diarias
    ├── Acceso Directo → datos_campanas
    └── Panel consolidado nivel C

```

**Beneficios:** Una copia de datos con múltiples usos, los accesos directos eliminan duplicación, almacenamiento unificado para toda la organización.

### Caso 2: Integración de Datos Históricos desde Almacenamiento en la Nube

Este ejemplo muestra cómo acceder a datos históricos almacenados en AWS S3 sin duplicarlos en OneLake.

```
CASO: E-commerce con Datos Históricos en S3

BUCKET AWS S3:
├── s3://retail-data/historical/
│   ├── /year=2023/sales_data.parquet
│   ├── /year=2022/sales_data.parquet
│   └── /year=2021/sales_data.parquet
↓
ACCESO DIRECTO ONELAKE:
├── analytics-workspace/
│   ├── aws_ventas_historicas → Bucket S3
│   ├── ventas_actuales (Replicación)
│   └── Análisis combinado histórico + actual

```

**Implementación:**

1. Crear Acceso Directo al bucket S3
2. Combinar con datos actuales en OneLake
3. Análisis unificado: 3 años de histórico + datos en tiempo real
4. Sin costo de almacenamiento para datos históricos

**Consulta de Ejemplo:**

```sql
SELECT TOP (10) 
    *
FROM [lakeh].[dbo].[historical]
WHERE YEAR([transaction_date]) = 2021;

```

### Caso 3: Experiencia de Acceso a Datos Familiar

Este ejemplo muestra cómo los científicos de datos pueden acceder a los datos de OneLake a través de interfaces familiares como el Explorador de Windows.

```
EXPERIENCIA FAMILIAR:

CIENTÍFICO DE DATOS:
├── Abre Explorador de Windows
├── Ve OneLake como unidad de red
├── Navega: /analytics-workspace/tables/
├── Abre: datos_cliente.parquet
└── Usa directamente en Python/R

```

**Código Python de Ejemplo:**

```python
import pandas as pd

# OneLake aparece como unidad local
df = pd.read_parquet("OneLake/analytics-workspace/datos_cliente/")
print(f"Datos: {len(df)} registros")

```

**Ejemplo de Ruta Local:**

```
C:\Users\Paul\OneLake - Microsoft\WP_3\iot_lakehouse.Lakehouse\Files\iot_sensor_data.parquet

```
### Caso 4: Mirroring de Snowflake para Análisis Híbrido

Este ejemplo demuestra cómo replicar datos de una base en Snowflake a OneLake en Microsoft Fabric, permitiendo sincronización en tiempo real y queries unificadas sin ETL manual. Se utiliza una tabla de clientes en Snowflake que se mirrors a Fabric, y se verifica la propagación de cambios (por ejemplo, una actualización de correo).
```
BASE SNOWFLAKE:
├── DEMO (Esquema)
│   └── customers (Tabla: NAME STRING, EMAIL STRING, COUNTRY STRING, CREATED_AT TIMESTAMP)
│       ├── Registros iniciales:
│       │   - ("Juan Pérez", "juan.perez@ejemplo.com", "Perú")
│       │   - ("María Gómez", "maria.gomez@ejemplo.com", "Chile")
│       │   - ("Paul Smith", "paul.smith@ejemplo.com", "USA")
↓
MIRRORING DESDE FABRIC:
├── analytics-workspace/
│   ├── snowflake_mirror → Tabla customers de Snowflake
│   └── Queries unificadas en Fabric (ej. con datos legacy + nuevos)
↓
ACTUALIZACIÓN:
- En Snowflake: UPDATE customers SET EMAIL = 'maria.nueva@ejemplo.com' WHERE NAME = 'María Gómez';
- En Fabric: El cambio se refleja en tiempo real en la tabla mirrored.


```
Implementación:
1. Configurar conexión a Snowflake en Microsoft Fabric (usando credenciales y permisos).
2. Crear un mirroring de la base de datos/esquema completo o tabla específica desde el portal de Fabric.
3. Ejecutar queries en Snowflake para insertar/actualizar datos.
4. Verificar en Fabric: Los cambios se sincronizan automáticamente (incremental, sin downtime).
5. Beneficios: Transición suave de legacy en Snowflake a análisis en Fabric, governance automática, costos optimizados (solo compute de Snowflake para queries originales).

Código Snowflake de INSERT & UPDATE:
```
-- Crear esquema si no existe (opcional, para mantener ordenado)
CREATE SCHEMA IF NOT EXISTS DEMO;

-- Crear tabla customers
CREATE OR REPLACE TABLE DEMO.customers (
    NAME STRING,
    EMAIL STRING,
    COUNTRY STRING,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar registros iniciales
INSERT INTO DEMO.customers (NAME, EMAIL, COUNTRY)
VALUES 
    ('Juan Pérez', 'juan.perez@ejemplo.com', 'Perú'),
    ('María Gómez', 'maria.gomez@ejemplo.com', 'Chile'),
    ('Paul Smith', 'paul.smith@ejemplo.com', 'USA');

-- Actualización de ejemplo (cambio que se propaga a Fabric)
UPDATE DEMO.customers 
SET EMAIL = 'maria.nueva@ejemplo.com' 
WHERE NAME = 'María Gómez';
```
Consulta despues en Fabric:
```
SELECT TOP (10) 
    *
FROM [lakehouse].[dbo].[customers]
ORDER BY CREATED_AT DESC;
-- Verás el email actualizado: 'maria.nueva@ejemplo.com'
```

## Comenzando

Para usar estos ejemplos:

1. Configurar un espacio de trabajo de Microsoft Fabric
2. Crear un Lakehouse en tu espacio de trabajo
3. Seguir los pasos de implementación específicos para cada caso de uso
4. Adaptar los ejemplos a tus fuentes de datos y requisitos específicos

## Requisitos

- Suscripción a Microsoft Fabric
- Permisos apropiados para crear y gestionar recursos
- Para fuentes de datos externas: credenciales de conexión y derechos de acceso

## Contribución

Siéntete libre de contribuir con ejemplos adicionales o mejoras a los existentes enviando un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.
