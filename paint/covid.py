import pandas as pd
import plotly.express as px
import os

from utils import loadZBSJson, getRootPath

#stat (must be an string) to choose from:
# - casos_confirmados_activos_ultimos_14dias
# - tasa_incidencia_acumulada_activos_ultimos_14dias
# - casos_confirmados_ultimos_14dias
# - tasa_incidencia_acumulada_ultimos_14dias
# - casos_confirmados_totales
# - tasa_incidencia_acumulada_total
def paintCovidCasesInZBS(stat):

    df = pd.read_csv(os.path.join(getRootPath(), "data/COVID/covid19_tia_zonas_basicas_salud_s.csv"), sep= ';')
    df_lastweek = df.loc[df['fecha_informe'] == df['fecha_informe'][0]]
    df_lastweek['codigo_geometria'] = df_lastweek['codigo_geometria'].str.rstrip()

    zbs = loadZBSJson(os.path.join(getRootPath(), "data/COVID/zonas_basicas_salud/zonas_basicas_salud.json"))

    fig = px.choropleth_mapbox(df_lastweek, geojson=zbs, featureidkey='properties.codigo_geo', locations='codigo_geometria', color=stat,
                               color_continuous_scale="OrRd",
                               mapbox_style="carto-positron",
                               hover_name = "zona_basica_salud",
                               hover_data = [stat],
                               center = {"lat": 40.417008, "lon": -3.703795}
                               #labels={'casos_confirmados_ultimos_14dias': 'Casos últimos 14 días'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
