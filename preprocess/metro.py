from shapely.geometry import Point
import pandas as pd
import os

from utils import loadZBSShapeFile, getRootPath

def preprocessMetroUsageInZBS():

    zbs_shp = loadZBSShapeFile(os.path.join(getRootPath(), "data/COVID/zonas_basicas_salud/zonas_basicas_salud.shp"))
    station_location = pd.read_csv(os.path.join(getRootPath(), 'data/metro/raw_data/mapas_metro.csv'))


    def groupby_zbs(id_point):
        select_location = station_location.iloc[[id_point]]

        if len(select_location) != 1:
            return 'error'
        point = Point(select_location['longitud'], select_location['latitud'])
        for i in range(0, len(zbs_shp['geometry'])):
            if point.within(zbs_shp['geometry'][i]):
                return str(zbs_shp['codigo_geo'][i])

    data = pd.read_csv(os.path.join(getRootPath(), 'data/metro/raw_data/mapas_metro.csv'))
    grouped_byzbs = data.groupby(groupby_zbs)
    grouped_byzbs_sum = grouped_byzbs.sum().reset_index()
    grouped_byzbs_sum.to_csv(os.path.join(getRootPath(), 'data/metro/zbsMap_metro.csv'))

