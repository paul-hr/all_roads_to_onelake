import pandas as pd
from pathlib import Path

# Ruta al archivo parquet
path = Path(r"C:\Users\Paul\OneLake - Microsoft\WP_3\iot_lakehouse.Lakehouse\Files\iot_sensor_data.parquet")

# Leer parquet
df = pd.read_parquet(path)

# Mostrar cantidad de registros
#print(f"Datos: {len(df)} registros")

# Mostrar primeras 5 filas
print(df.info())
