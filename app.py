import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas & ML - PySpark Pipeline",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados inyectados para estética premium
st.markdown("""
<style>
    .main {
        background-color: #0f111a;
        color: #e6edf3;
    }
    .stApp {
        background-color: #0f111a;
    }
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    /* Estilo para las tarjetas de KPI */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        color: #3b82f6;
        font-weight: 700;
    }
    .kpi-icon {
        float: right;
        font-size: 2rem;
        color: #3b82f6;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# Rutas de datos
PATH_PARQUET = "data/ventas_procesadas"
PATH_CSV = "data/ventas.csv"
PATH_MODEL = "models/sales_model.pkl"

# Funciones de carga de datos
@st.cache_data
def load_data():
    df = None
    source = ""
    # Intentar cargar desde Parquet (salida de PySpark)
    if os.path.exists(PATH_PARQUET):
        try:
            # Leer directorio Parquet
            df = pd.read_parquet(PATH_PARQUET)
            source = "Parquet (Procesado por PySpark)"
        except Exception as e:
            st.sidebar.error(f"Error al leer Parquet: {e}")
    
    # Fallback al CSV si no hay Parquet
    if df is None and os.path.exists(PATH_CSV):
        try:
            df = pd.read_csv(PATH_CSV)
            # Calcular columna requerida si es del CSV directamente
            df['total_venta'] = df['cantidad'] * df['precio']
            source = "CSV (Original - Fallback)"
        except Exception as e:
            st.sidebar.error(f"Error al leer CSV: {e}")
            
    return df, source

df, data_source = load_data()

# Título y Header Principal
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>📊 Dashboard de Ventas & Machine Learning</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 30px;'>Visualización en tiempo real del pipeline de datos con PySpark e inferencia de Inteligencia Artificial</p>", unsafe_allow_html=True)

# Panel lateral
st.sidebar.image("https://spark.apache.org/images/spark-logo-trademark.png", width=120)
st.sidebar.title("Configuración")
st.sidebar.markdown("---")

if df is not None:
    st.sidebar.success(f"**Origen de datos:**\n{data_source}")
    st.sidebar.info(f"**Total registros:** {len(df)}")
    
    # Filtro interactivo de productos
    all_products = ["Todos"] + list(df['producto'].unique())
    selected_product = st.sidebar.selectbox("Filtrar por Producto", all_products)
    
    # Filtrar dataframe
    if selected_product != "Todos":
        filtered_df = df[df['producto'] == selected_product]
    else:
        filtered_df = df
else:
    st.sidebar.error("No se encontraron archivos de datos (CSV o Parquet). Por favor corre el script ETL primero.")
    st.error("No hay datos disponibles para mostrar. Asegúrate de tener 'data/ventas.csv' o ejecutar 'process_sales.py'.")
    st.stop()

# ----------------- PANEL PRINCIPAL: KPIs -----------------
st.markdown("### 📈 Métricas de Negocio Clave")
kpi_cols = st.columns(4)

total_revenue = filtered_df['total_venta'].sum()
total_units = filtered_df['cantidad'].sum()
avg_price = filtered_df['precio'].mean()
# Producto estrella
star_product = filtered_df.groupby('producto')['cantidad'].sum().idxmax()
star_product_qty = filtered_df.groupby('producto')['cantidad'].sum().max()

with kpi_cols[0]:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">💰</span>
        <div class="kpi-title">Ingresos Totales</div>
        <div class="kpi-value">${total_revenue:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📦</span>
        <div class="kpi-title">Unidades Vendidas</div>
        <div class="kpi-value">{total_units:,} u.</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🏷️</span>
        <div class="kpi-title">Precio Promedio</div>
        <div class="kpi-value">${avg_price:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⭐</span>
        <div class="kpi-title">Producto Estrella</div>
        <div class="kpi-value">{star_product} <span style="font-size: 1rem; color: #10b981;">({star_product_qty} u.)</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- GRÁFICOS -----------------
st.markdown("### 📊 Gráficos y Visualizaciones")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Ingresos Totales por Producto")
    sales_by_prod = filtered_df.groupby('producto')['total_venta'].sum().reset_index()
    sales_by_prod = sales_by_prod.sort_values(by='total_venta', ascending=False)
    
    fig_sales = px.bar(
        sales_by_prod, 
        x='producto', 
        y='total_venta',
        text_auto='.2s',
        color='total_venta',
        color_continuous_scale=px.colors.sequential.Blues,
        labels={'producto': 'Producto', 'total_venta': 'Ventas Totales ($)'}
    )
    fig_sales.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#e6edf3",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=10, b=20),
        height=350
    )
    fig_sales.update_xaxes(showgrid=False)
    fig_sales.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.markdown("#### Distribución de Cantidades por Venta")
    qty_dist = filtered_df.groupby('producto')['cantidad'].sum().reset_index()
    fig_pie = px.pie(
        qty_dist,
        values='cantidad',
        names='producto',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#e6edf3",
        margin=dict(l=20, r=20, t=10, b=20),
        height=350
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# ----------------- MODELO DE ML INTERACTIVO -----------------
st.markdown("---")
st.markdown("### 🤖 Predicción y Modelado de Inteligencia Artificial (ML)")

# Cargar o entrenar modelo al instante
model_loaded = False
model_data = None

# Función interna para entrenar modelo de forma dinámica
def train_model_on_fly(data):
    le = LabelEncoder()
    data['producto_encoded'] = le.fit_transform(data['producto'])
    X = data[['producto_encoded', 'precio']]
    y = data['cantidad']
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    prod_prices = data.groupby('producto')['precio'].mean().to_dict()
    return {
        'model': rf,
        'label_encoder': le,
        'products_info': prod_prices
    }

if os.path.exists(PATH_MODEL):
    try:
        with open(PATH_MODEL, "rb") as f:
            model_data = pickle.load(f)
        model_loaded = True
        st.info("✅ Modelo cargado con éxito desde `models/sales_model.pkl` (entrenado en el Jupyter Notebook).")
    except Exception as e:
        st.warning(f"Error al cargar el archivo de modelo serializado: {e}. Se entrenará un modelo dinámico temporal.")

if not model_loaded:
    # Entrenar dinámicamente
    model_data = train_model_on_fly(df)
    st.success("🤖 Modelo de Random Forest entrenado dinámicamente en tiempo real para esta sesión utilizando el dataset de ventas.")

# Panel interactivo de inferencia
ml_col1, ml_col2 = st.columns([1, 1])

with ml_col1:
    st.markdown("#### Parámetros del Escenario de Venta")
    # Selector de producto
    products_available = sorted(list(df['producto'].unique()))
    input_product = st.selectbox("Seleccione el Producto a Vender", products_available, key="ml_product")
    
    # Precio base del producto seleccionado
    default_price = float(model_data['products_info'].get(input_product, 100.0))
    
    input_price = st.slider(
        "Establezca el Precio Unitario ($)", 
        min_value=max(10.0, default_price * 0.5), 
        max_value=default_price * 1.5, 
        value=default_price, 
        step=5.0
    )

with ml_col2:
    st.markdown("#### Resultado del Modelo Predictivo")
    
    # Realizar predicción
    try:
        # Codificar el producto
        # Manejar nuevos productos de manera segura
        le = model_data['label_encoder']
        if input_product in le.classes_:
            product_encoded = le.transform([input_product])[0]
        else:
            # Producto desconocido por el encoder
            product_encoded = len(le.classes_)
            
        # Preparar entrada
        features = np.array([[product_encoded, input_price]])
        
        # Predecir cantidad
        predicted_qty = model_data['model'].predict(features)[0]
        predicted_qty_rounded = int(np.round(predicted_qty))
        if predicted_qty_rounded < 1:
            predicted_qty_rounded = 1
            
        # Calcular total venta estimado
        predicted_total = predicted_qty_rounded * input_price
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: rgba(30, 41, 59, 0.6); padding: 25px; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.3); text-align: center;">
            <p style="margin-bottom: 5px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Cantidad Demandada Estimada</p>
            <h2 style="color: #60a5fa; font-size: 3rem; margin: 0 0 10px 0;">{predicted_qty:.2f} <span style="font-size: 1.5rem; color: #e6edf3;">≈ {predicted_qty_rounded} unidades</span></h2>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
            <p style="margin-bottom: 5px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Ingresos Totales Estimados</p>
            <h3 style="color: #10b981; font-size: 2.2rem; margin: 0;">${predicted_total:,.2f}</h3>
            <p style="font-size: 0.8rem; color: #64748b; margin-top: 10px;">Fórmula: Cantidad Estimada Redondeada × Precio Establecido</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error al realizar la predicción del modelo: {e}")

# ----------------- VISUALIZADOR DE DATOS -----------------
st.markdown("---")
st.markdown("### 📋 Tabla de Datos Procesados")
show_data = st.checkbox("Mostrar tabla de datos completa")
if show_data:
    st.dataframe(
        filtered_df, 
        column_config={
            "id_venta": st.column_config.NumberColumn("ID Venta", format="%d"),
            "producto": "Producto",
            "cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
            "precio": st.column_config.NumberColumn("Precio Unitario", format="$%d"),
            "total_venta": st.column_config.NumberColumn("Total Venta", format="$%.2f")
        },
        use_container_width=True
    )
