from shapely.geometry import Point
import pandas as pd
import os

from utils import loadZBSShapeFile, getRootPath

def preprocessCarTrafficInZBS():

    zbs_shp = loadZBSShapeFile(os.path.join(getRootPath(), "data/COVID/zonas_basicas_salud/zonas_basicas_salud.shp"))
    sensors_location = pd.read_csv(os.path.join(getRootPath(), 'data/trafico/raw_data/pmed_ubicacion_07-2020.csv'), sep=';')

    def groupby_zbs(id_point):
        select_location = sensors_location.loc[sensors_location['id'] == id_point]

        if len(select_location) != 1:
            return 'error'
        point = Point(select_location['longitud'], select_location['latitud'])
        for i in range(0, len(zbs_shp['geometry'])):
            if point.within(zbs_shp['geometry'][i]):
                return str(zbs_shp['codigo_geo'][i])


    data = pd.read_csv(os.path.join(getRootPath(), 'data/trafico/raw_data/07-2020.csv'), sep=';')
    grouped_byid = data.groupby('id').mean()
    grouped_byzbs = grouped_byid.groupby(groupby_zbs)
    grouped_byzbs.mean().reset_index().to_csv(os.path.join(getRootPath(), 'data/trafico/07-2020_zbsMap.csv'))

