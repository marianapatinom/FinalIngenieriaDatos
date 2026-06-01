import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Análisis de Ventas y Modelado Predictivo de Demanda\n",
    "\n",
    "Este cuaderno contiene el análisis exploratorio de datos (EDA) y el entrenamiento de un modelo de Machine Learning para predecir la cantidad de productos vendidos a partir del tipo de producto y su precio unitario.\n",
    "\n",
    "### Objetivos:\n",
    "1. Cargar y explorar los datos de ventas procesados en Parquet.\n",
    "2. Visualizar patrones clave en las ventas.\n",
    "3. Desarrollar un modelo de regresión (Random Forest) para estimar la demanda (cantidad).\n",
    "4. Exportar el modelo entrenado para su uso interactivo en la aplicación de Streamlit."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import os\n",
    "import pickle\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from sklearn.preprocessing import LabelEncoder\n",
    "from sklearn.metrics import mean_squared_error, r2_score\n",
    "\n",
    "# Configuración de visualizaciones\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "plt.rcParams['figure.figsize'] = (10, 6)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Carga de Datos Procesados\n",
    "Cargamos el archivo Parquet procesado por el pipeline de PySpark."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Nota: Si el pipeline de PySpark no se ha ejecutado, cargamos el CSV directamente como respaldo\n",
    "data_path_parquet = \"data/ventas_procesadas\"\n",
    "data_path_csv = \"data/ventas.csv\"\n",
    "\n",
    "if os.path.exists(data_path_parquet):\n",
    "    print(\"Cargando datos desde Parquet (procesado con PySpark)...\")\n",
    "    df = pd.read_parquet(data_path_parquet)\n",
    "else:\n",
    "    print(\"Cargando datos desde CSV (respaldo)...\")\n",
    "    df = pd.read_csv(data_path_csv)\n",
    "    df['total_venta'] = df['cantidad'] * df['precio']\n",
    "\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Análisis Exploratorio y Visualización\n",
    "Veamos un resumen estadístico y algunas gráficas clave."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"Resumen Estadístico:\")\n",
    "print(df.describe())\n",
    "\n",
    "print(\"\\nTotal de ingresos por producto:\")\n",
    "ingresos_prod = df.groupby('producto')['total_venta'].sum().sort_values(ascending=False)\n",
    "print(ingresos_prod)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gráfico de barras de ventas totales por producto\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.barplot(x=ingresos_prod.index, y=ingresos_prod.values, palette=\"viridis\")\n",
    "plt.title(\"Ingresos Totales por Producto\")\n",
    "plt.xlabel(\"Producto\")\n",
    "plt.ylabel(\"Ventas Totales ($)\")\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "os.makedirs(\"data\", exist_ok=True)\n",
    "plt.savefig(\"data/ingresos_por_producto.png\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Preparación de Datos para Machine Learning\n",
    "Queremos entrenar un modelo para predecir la **cantidad** vendida basada en el **producto** y su **precio**. Esto simula una curva de demanda del mercado."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Codificar la variable categórica 'producto'\n",
    "le = LabelEncoder()\n",
    "df['producto_encoded'] = le.fit_transform(df['producto'])\n",
    "\n",
    "# Características (X) y Objetivo (y)\n",
    "X = df[['producto_encoded', 'precio']]\n",
    "y = df['cantidad']\n",
    "\n",
    "# División en entrenamiento y prueba\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "\n",
    "print(f\"Dimensiones de entrenamiento: {X_train.shape}\")\n",
    "print(f\"Dimensiones de prueba: {X_test.shape}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Entrenamiento del Modelo (Random Forest Regressor)\n",
    "Entrenamos un modelo de bosque aleatorio para capturar relaciones no lineales en el precio y la demanda."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "model = RandomForestRegressor(n_estimators=100, random_state=42)\n",
    "model.fit(X_train, y_train)\n",
    "\n",
    "# Predicciones\n",
    "y_pred = model.predict(X_test)\n",
    "\n",
    "# Evaluación\n",
    "mse = mean_squared_error(y_test, y_pred)\n",
    "r2 = r2_score(y_test, y_pred)\n",
    "\n",
    "print(f\"Error Cuadrático Medio (MSE): {mse:.4f}\")\n",
    "print(f\"Coeficiente de Determinación (R^2): {r2:.4f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Exportar el Modelo\n",
    "Guardamos el modelo entrenado y el `LabelEncoder` para poder utilizarlos en la aplicación interactiva de Streamlit (`app.py`)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Crear directorio de modelos si no existe\n",
    "os.makedirs(\"models\", exist_ok=True)\n",
    "\n",
    "# Guardar modelo y codificador\n",
    "model_data = {\n",
    "    'model': model,\n",
    "    'label_encoder': le,\n",
    "    'products_info': df.groupby('producto')['precio'].mean().to_dict()\n",
    "}\n",
    "\n",
    "with open(\"models/sales_model.pkl\", \"wb\") as f:\n",
    "    pickle.dump(model_data, f)\n",
    "\n",
    "print(\"¡Modelo y codificador de etiquetas guardados con éxito en 'models/sales_model.pkl'!\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("notebook.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1)

print("notebook.ipynb creado exitosamente.")
