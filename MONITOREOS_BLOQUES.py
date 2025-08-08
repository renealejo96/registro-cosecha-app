import pandas as pd
path=r"C:\Users\rvelez\OneDrive - Elite Flower\Documentos\Documento RENE VELEZ\ESTADOS DE CULTIVO\2025\Estado Cultivo PYGAN 2025-25-1.xlsx"
df = pd.read_excel(path, sheet_name='MUESTREO')
print("Columnas disponibles:", df.columns)
col_bloque="BLQ"
col_plantas="Suma de # PLANTAS"
df = df[[col_bloque, col_plantas]].copy()
# Parámetros estadísticos
Z = 1.96  # Nivel de confianza 95%
E = 0.05  # Margen de error (5%)
p = 0.5   # Proporción esperada de mortalidad

# Tamaño de muestra sin ajuste
n0 = (Z**2 * p * (1 - p)) / E**2
df["Muestra_Ajustada"] = n0 / (1 + ((n0 - 1) / df[col_plantas]))
df["Muestra_Ajustada"] = df["Muestra_Ajustada"].round().astype(int)
print(df)