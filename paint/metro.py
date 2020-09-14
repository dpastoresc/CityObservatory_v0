import os
import pandas as pd
import plotly.express as px

from preprocess.metro import preprocessMetroUsageInZBS
from utils import loadZBSJson, getRootPath

#stat (must be an string) to choose from:
# - Ent_2014
# - Util_2014
# - Ent_2015
# - Util_2015
# - Ent_2016
# - Util_2016
# - Ent_2017
# - Util_2017
# - Ent_2018
# - Util_2018
# - Ent_2019
# - Util_2019
def paintMetroUsageInZBS(stat):
    if not(os.path.exists(os.path.join(getRootPath(), 'data/metro/zbsMap_metro.csv'))):
        preprocessMetroUsageInZBS()

    grouped_byzbs_sum = pd.read_csv(os.path.join(getRootPath(), 'data/metro/zbsMap_metro.csv'), dtype={'index': object})
    zbs_json = loadZBSJson(os.path.join(getRootPath(), "data/COVID/zonas_basicas_salud/zonas_basicas_salud.json"))
    station_location = pd.read_csv(os.path.join(getRootPath(), 'data/metro/raw_data/mapas_metro.csv'))

    fig_loc = px.scatter_mapbox(station_location,
                            lat="lat",
                            lon="long",
                            hover_name="name_Est",
                            mapbox_style="carto-positron",
                            )

    fig = px.choropleth_mapbox(grouped_byzbs_sum, geojson=zbs_json, featureidkey='properties.codigo_geo', locations='index', color=stat,
                               color_continuous_scale="OrRd",
                               mapbox_style="carto-positron",
                               hover_data = [stat],
                               center = {"lat": 40.417008, "lon": -3.703795}
                               #labels={'casos_confirmados_ultimos_14dias': 'Casos últimos 14 días'}
                               )

    fig.add_trace(fig_loc.data[0])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
