import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
import matplotlib.pyplot as plt

# cargando la data
url = "TB_FALLECIDO_HOSP_VAC.csv"
url_json = "peru_distrital_simple.geojson.json"
data = pd.read_csv(url)
map_data = gpd.read_file(url_json)
map_data.dropna(inplace=True)
print(map_data.head())
print(map_data.NOMBPROV.value_counts().index)

# Mapa de cantidad de fallecidos por distrito en el Perú
subData = data[['id_persona', 'ubigeo_cdc']]  # Solo los datos q necesitamos
subData = subData.groupby('ubigeo_cdc').count().reset_index()
fallecidos = []
for dist in map_data['IDDIST']:
    values = subData[subData['ubigeo_cdc'] == int(dist)]['id_persona'].values
    if len(values) > 0:
        fallecidos.append(values[0])
    else:
        fallecidos.append(0)
map_data['fallecidos'] = fallecidos
fig, ax = plt.subplots(figsize=(20, 20))

# Control del título y los ejes
ax.set_title('Cantidad de fallecidos por distrito', pad=20, fontdict={'fontsize': 20, 'color': '#4873ab'})
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Mostrar el mapa finalizado
map_data.plot(column='fallecidos', cmap='plasma', ax=ax, zorder=5, legend=True)
print(data.isnull().sum())
data["fecha_fallecimiento"] = data["fecha_fallecimiento"].aggregate(pd.to_datetime, axis=0, yearfirst=True, dayfirst=False).head()
print(data["fecha_fallecimiento"].head())
range_dates = pd.Series(pd.date_range(start=str(data["fecha_fallecimiento"].min()), end=str(data["fecha_fallecimiento"].max()), periods=6))
print(data[data["fecha_fallecimiento"] > range_dates[4]])
print(data.dtypes)

options = ["Localidad Departamento", "Sexo", "Mapas"]

with st.sidebar:
    selected = option_menu("Muertos Por Covid Peru Segun: ", options, default_index=0)
if selected == "Localidad Departamento":
    muertos_by_fecha = data.groupby("fecha_fallecimiento")["sexo"].count()
    st.line_chart(muertos_by_fecha)

elif selected == "sexo":
    option = st.selectbox(
        label="Elija una opcion para filtrar", options=data.drop("sexo", axis=1).columns)
    data2 = pd.concat([data.loc[data["sexo"] == 'M', [option]].value_counts(), data.loc[data["sexo"] == 'F', [option]].value_counts()], axis=1)
    index = pd.Index(data2.index.values)
    data_by_sex = pd.DataFrame(data2.values, index=index, columns=["M", "F"])
    st.bar_chart(data_by_sex)
elif selected == "Mapas":
    st.pyplot(fig)
    option = st.selectbox(
        label="Elija una region", options=map_data.NOMBPROV.value_counts().index.values)
    ax = map_data[map_data.NOMBPROV == option].plot(figsize=(10, 10), column='fallecidos', legend=True)
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.title(f'Cant. fallecidos - {option.capitalize()} provincia')
    ax.axis('scaled')
    st.pyplot(ax.figure, clear_figure=True)
