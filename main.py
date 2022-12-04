import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
import matplotlib.pyplot as plt

from datetime import  datetime
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
data = data.drop(["fecha_segumiento_hosp_ultimo","fecha_dosis3","ubigeo_cdc","dpt_cdc","prov_cdc","dist_cdc","cdc_positividad","flag_vacuna","eess_renaes","eess_diresa","eess_red","eess_nombre","evolucion_hosp_ultimo","fecha_dosis1","fecha_dosis2","fecha_ingreso_hosp","fecha_ingreso_uci","fecha_ingreso_ucin","ubigeo_inei_domicilio"],axis=1)
# Mostrar el mapa finalizado
map_data.plot(column='fallecidos', cmap='plasma', ax=ax, zorder=5, legend=True)
data = data.convert_dtypes()
print(data["fecha_fallecimiento"].tail())
data["fecha_fallecimiento"] = data["fecha_fallecimiento"].apply(pd.to_datetime, yearfirst=True, dayfirst=False)
print(data["fecha_fallecimiento"].isna().sum())
range_dates = pd.Series(pd.date_range(start=str(data["fecha_fallecimiento"].min()), end=str(data["fecha_fallecimiento"].max()), periods=11)).drop(0)
# print(data[data["fecha_fallecimiento"] > range_dates[4]])
# print(range_dates)
options = ["Tabla Principal", "Sexo", "Mapas","Edad"]

with st.sidebar:
    selected = option_menu("Muertos Por Covid Peru Segun: ", options, default_index=0)
if selected == "Tabla Principal":
    st.title("Tabala 50 primeros")
    st.table(data.head(50).fillna({"fabricante_dosis1":"No aplico dosis","fabricante_dosis2":"No aplico dosis","fabricante_dosis3":"No aplico dosis"}))
elif selected == "Sexo":
    st.header("Grafico de barras  de dobler entrada con Criterio de Sexo")
    option = st.selectbox(
        label="Elija una opcion para filtrar", options=data.drop(["sexo","id_persona"], axis=1).columns)
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
elif selected == "Edad":
    st.title("Registro de muertos por covid 19 segun Edad")
    st.write("Variabilidad segun fechas registradas")
    start_time = st.select_slider("Fecha de ultimo registros",options=range_dates.values,format_func=lambda op:datetime.utcfromtimestamp(op.astype(int) * 1e-9))
    st.write("Start time:", start_time)
    data_filter =pd.DataFrame(data.loc[data["fecha_fallecimiento"]<start_time,["edad"]].value_counts()).reset_index()
    data_filter.columns = ["edad","cantidad"]
    print(data_filter)
    st.vega_lite_chart(data_filter, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'edad', 'type': 'quantitative'},
            'y': {'field': 'cantidad', 'type': 'quantitative'},
        },
    })
