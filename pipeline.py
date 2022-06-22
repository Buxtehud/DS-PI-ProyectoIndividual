import pandas as pd
import numpy as np

df_clientes = pd.read_csv('./Datasets/Clientes.csv', delimiter=';', encoding='utf-8')
df_compra = pd.read_csv('./Datasets/Compra.csv')
df_gasto = pd.read_csv('./Datasets/Gasto.csv')
df_local = pd.read_csv('./Datasets/Localidades.csv')
df_prov = pd.read_csv('./Datasets/Proveedores.csv', encoding='iso-8859-1')
df_suc = pd.read_csv('./Datasets/Sucursales.csv', delimiter=';')
df_venta = pd.read_csv('./Datasets/Venta.csv')

# ------------Para tabla ventas----------------------------------


def get_moda(df, element_id, referencia, target):
    """Obtiene la moda de una columna target filtrando a través de la columna referencia"""
    df_moda = df[df[referencia] == element_id].mode()
    return df_moda[target][0]


def input_moda(df, element_id, referencia, target):
    """Cambia todos los valores de las columnas al valor de la moda"""
    moda = get_moda(df, element_id, referencia, target)
    df.loc[(df[target] != moda) & (df[referencia] == element_id), target] = moda


productos = [x for x in df_venta['IdProducto'].unique()] # Obtengo todos los Id únicos de cada producto

# Todos los productos iguales (mismo IdProduct) se venden al mismo Precio
for product in productos:
    input_moda(df_venta, product, 'IdProducto', 'Precio')