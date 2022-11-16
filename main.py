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
print(data.tail())
data_na = data.dropna()
print(data['flag_vacuna'].value_counts())
print(data.groupby('flag_vacuna')['fecha_fallecimiento'].count())
print(data['fecha_dosis1'].count() - data['fecha_dosis1'].isna().count())
fec_fall = data['fecha_fallecimiento']
print(data.isna().sum())
print(data['dep_domicilio'].value_counts())
print(data.columns.array)
options = [""]
with st.sidebar:
    selected = option_menu("Muertos Por Covid Peru Segun: ", list(data.columns.array),
                           icons=['house', 'gear'], menu_icon="cast", default_index=1)
st.text(selected)
