import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

df_canal = pd.read_csv('./Datasets/CanalDeVenta.csv')
df_clientes = pd.read_csv('./Datasets/Clientes.csv', delimiter=';', encoding='utf-8')
df_compra = pd.read_csv('./Datasets/Compra.csv')
df_gasto = pd.read_csv('./Datasets/Gasto.csv')
df_local = pd.read_csv('./Datasets/Localidades.csv')
df_prov = pd.read_csv('./Datasets/Proveedores.csv', encoding='iso-8859-1')
df_suc = pd.read_csv('./Datasets/Sucursales.csv', delimiter=';')
df_tipo = pd.read_csv('./Datasets/TiposDeGasto.csv')
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


# -------------Para tabla clientes--------------------------------------


df_clientes = df_clientes.drop(columns='col10')
df_provincias = df_local.loc[:,['provincia_id','provincia_nombre']].drop_duplicates()


def get_apellidos(df, columna):
    apellidos = []
    for nombre in df[columna]:
        if isinstance(nombre, str):
            words = nombre.split(' ')
            apellidos.append(words[-1])
        else:
            apellidos.append(float('NaN'))
    return apellidos


def get_names(element):
    if isinstance(element, str):
        names = element.split(' ')[:-1]
        return ' '.join(names)


def nombre_apellido(df):
    apellidos = get_apellidos(df, 'Nombre_y_Apellido')
    df.insert(3, 'Apellido', apellidos)
    df['Nombre_y_Apellido'] = df['Nombre_y_Apellido'].apply(get_names)
    df.rename(columns={'Nombre_y_Apellido':'Nombre'}, inplace=True)


nombre_apellido(df_clientes)


def provincia_to_id(element):
    '''Obtengo el Id de la provincia y reemplazo su nombre'''
    if isinstance(element, str):
        s = df_provincias[df_provincias['provincia_nombre'].apply(lambda x: fuzz.partial_ratio(x,element)) > 80]['provincia_id']
        f = s[0]
        return f
    else:
        return element


df_clientes['Provincia'] = df_clientes['Provincia'].apply(provincia_to_id)
df_clientes.rename(columns={'Provincia':'IdProvincia'}, inplace=True)



def replace_comma(stringed):
    try:
        with_comma = stringed.replace(',','.')
        return float(with_comma)
    except:
        return float('NaN')


df_clientes.X = df_clientes.X.apply(replace_comma)
df_clientes.Y = df_clientes.Y.apply(replace_comma)