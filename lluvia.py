import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Cargar los datos desde un archivo Excel
path=r"C:\Users\rvelez\OneDrive - Elite Flower\Documentos\mortalidad vs lluvia.xlsx"
df = pd.read_excel(path, sheet_name='Hoja1')

# Renombrar columnas
df.columns = ['semana', 'lluvia_mm', 'mortalidad_frac']

# Extraer año y semana del año
df['año'] = df['semana'] // 100
df['semana_del_año'] = df['semana'] % 100

# Convertir fracción de mortalidad a porcentaje
df['mortalidad_pct'] = df['mortalidad_frac'] * 100

# Preparar variables para el modelo
X = df[['lluvia_mm']].values
y = df['mortalidad_pct'].values

# Crear y ajustar el modelo de regresión lineal
model = LinearRegression()
model.fit(X, y)

# Obtener coeficientes
intercept = model.intercept_
slope = model.coef_[0]
print(f"Modelo: Mortalidad (%) = {intercept:.2f} + {slope:.2f} * Lluvia (mm)")

# Generar predicciones
df['predicciones'] = model.predict(X)

# Visualización
plt.figure(figsize=(8, 5))
sns.scatterplot(x='lluvia_mm', y='mortalidad_pct', data=df, label='Datos reales')
sns.lineplot(x='lluvia_mm', y='predicciones', data=df, color='red', label='Modelo lineal')
plt.title(f'Modelo de regresión\\nMortalidad (%) = {intercept:.2f} + {slope:.2f} * Lluvia (mm)')
plt.xlabel('Precipitación (mm)')
plt.ylabel('Mortalidad (%)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

