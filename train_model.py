import pandas as pd
import numpy as np
import os
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def train():
    print("Iniciando entrenamiento del modelo de Machine Learning...")
    
    # 1. Cargar datos procesados
    path_parquet = "data/ventas_procesadas"
    if not os.path.exists(path_parquet):
        print("Error: No se encontraron los datos Parquet. Corriendo simulación de datos primero...")
        return
        
    df = pd.read_parquet(path_parquet)
    
    # 2. Codificar la columna de producto
    le = LabelEncoder()
    df['producto_encoded'] = le.fit_transform(df['producto'])
    
    # 3. Preparar variables
    X = df[['producto_encoded', 'precio']]
    y = df['cantidad']
    
    # 4. Entrenar el Regresor RandomForest
    print("Ajustando regresor Random Forest...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 5. Guardar modelo y codificador
    os.makedirs("models", exist_ok=True)
    model_data = {
        'model': model,
        'label_encoder': le,
        'products_info': df.groupby('producto')['precio'].mean().to_dict()
    }
    
    path_model = "models/sales_model.pkl"
    with open(path_model, "wb") as f:
        pickle.dump(model_data, f)
        
    print(f"¡Modelo de Machine Learning entrenado y guardado con éxito en: {path_model}!")

if __name__ == "__main__":
    train()
