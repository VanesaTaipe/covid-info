import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
"""['id_persona', 'fecha_fallecimiento', 'edad', 'sexo',
       'criterio_fallecido', 'ubigeo_cdc', 'dpt_cdc', 'prov_cdc', 'dist_cdc',
       'cdc_positividad', 'flag_vacuna', 'fecha_dosis1', 'fabricante_dosis1',
       'fecha_dosis2', 'fabricante_dosis2', 'fecha_dosis3',
       'fabricante_dosis3', 'flag_hospitalizado', 'eess_renaes', 'eess_diresa',
       'eess_red', 'eess_nombre', 'fecha_ingreso_hosp', 'flag_uci',
       'fecha_ingreso_uci', 'fecha_ingreso_ucin', 'con_oxigeno',
       'con_ventilacion', 'fecha_segumiento_hosp_ultimo',
       'evolucion_hosp_ultimo', 'ubigeo_inei_domicilio', 'dep_domicilio',
       'prov_domicilio', 'dist_domicilio']"""
url = "TB_FALLECIDO_HOSP_VAC.csv"
data = pd.read_csv(url, index_col='id_persona')
data_na = data.dropna()

print(data.loc[data['dist_domicilio'] == 'LIMA', "edad"])
data.info(verbose=False)
# Mapear Rango de Fechas

data["fecha_fallecimiento"] = data["fecha_fallecimiento"].aggregate(pd.to_datetime, axis=0, yearfirst=True, dayfirst=False).head()
print(data["fecha_fallecimiento"].head())
range_dates = pd.Series(pd.date_range(start=str(data["fecha_fallecimiento"].min()), end=str(data["fecha_fallecimiento"].max()), periods=6))
print(data[data["fecha_fallecimiento"] > range_dates[4]])
# criterios_de_grafica
options = ["Localidad Departamento"]
# with st.sidebar:
#     selected = option_menu("Muertos Por Covid Peru Segun: ", options,
#                            icons=['house', 'gear'], menu_icon="cast", default_index=0)
# if selected == "Localidad Departamento":
#     muertos_by_fecha = data.groupby("fecha_fallecimiento")["sexo"].count()
#     st.line_chart(muertos_by_fecha)
