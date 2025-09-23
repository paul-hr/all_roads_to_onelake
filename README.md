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

### Caso 3: Descubrimiento de Datos de Autoservicio

Este ejemplo ilustra cómo los nuevos analistas pueden descubrir y acceder rápidamente a los datos sin sobrecarga administrativa.

```
FLUJO DE DESCUBRIMIENTO:

NUEVO ANALISTA:
├── Abre Catálogo OneLake
├── Busca: "cliente"
├── Encuentra: datos_cliente (en ventas-analytics)
├── Ve vista previa + metadatos
└── Crea acceso directo en su espacio de trabajo
↓
RESULTADO INMEDIATO:
├── Acceso de autoservicio a datos
├── Sin duplicación de datos
├── Gobernanza automática
└── Análisis en minutos, no semanas

```

### Caso 4: Experiencia de Acceso a Datos Familiar

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
