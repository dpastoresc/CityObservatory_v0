import pandas as pd
import plotly.express as px
import os

from preprocess.traffic import preprocessCarTrafficInZBS
from utils import loadZBSJson, getRootPath

def paintTraficSensorLocations():
    token = 'pk.eyJ1IjoiY3RhcmF6b25hIiwiYSI6ImNrZDkxcW1sYjBwOWkycnM4NDRpbXViYnYifQ.jK8gChNK_dzVpKlrKKfJgA'

    df = pd.read_csv(os.path.join(getRootPath(), 'data/trafico/raw_data/pmed_ubicacion_07-2020.csv'), sep=';')

    px.set_mapbox_access_token(token)
    fig = px.scatter_mapbox(df, lat="latitud", lon="longitud", hover_name="nombre",
                             color_discrete_sequence=["blue"], zoom=10, height=500)

    return fig

#stat (must be an string) to choose from:
# - intensidad
# - ocupacion
# - carga
# - vmed
def paintCarTrafficInZBS(stat):
    if not(os.path.exists(os.path.join(getRootPath(), 'data/trafico/07-2020_zbsMap.csv'))):
        preprocessCarTrafficInZBS()

    grouped_byzbs_mean = pd.read_csv(os.path.join(getRootPath(), 'data/trafico/07-2020_zbsMap.csv'))

    zbs_json = loadZBSJson(os.path.join(getRootPath(), "data/COVID/zonas_basicas_salud/zonas_basicas_salud.json"))


    fig = px.choropleth_mapbox(grouped_byzbs_mean, geojson=zbs_json, featureidkey='properties.codigo_geo', locations='index', color=stat,
                               color_continuous_scale="OrRd",
                               mapbox_style="carto-positron",
                               hover_data = [stat],
                               center = {"lat": 40.417008, "lon": -3.703795}
                               #labels={'casos_confirmados_ultimos_14dias': 'Casos últimos 14 días'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig



