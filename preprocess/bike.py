import pandas as pd
import os
import geopandas as gpd
import json
from shapely.geometry import Point


from utils import getRootPath, loadZBSShapeFile

def preprocessBikeTravelsEveryHour(year, month):

  filepath = os.path.join(getRootPath(), 'data/bike/raw_data/' + year + month + '_movements.json')
  df = pd.read_json(open(filepath).read(), lines=True)
  df['unplug_hourTime'] = df['unplug_hourTime'].str[11:-1]
  hour = df.groupby('unplug_hourTime').count().reset_index()
  hour = hour[['unplug_hourTime', '_id']]
  hour = hour.rename(columns={"_id": "travels"})
  hour.to_csv(os.path.join(getRootPath(), 'data/bike/'+ year + month + '_movements_hour.csv'))


def preprocessBikeTravelsSankeyZip(year, month):

    zip_shp = gpd.read_file(open(os.path.join(getRootPath(), "data/distritos/MADRID.json")).read())

    locations = pd.read_json(open(os.path.join(getRootPath(), "data/bike/raw_data/stations_location.json")))

    filepath = os.path.join(getRootPath(), 'data/bike/raw_data/' + year + month + '_movements.json')
    df = pd.read_json(open(filepath).read(), lines=True)

    def groupby_zipCode(id_point):

          idunplug_station = df.iloc[id_point]['idunplug_station']
          idplug_station = df.iloc[id_point]['idplug_station']

          lon_idunplug_station = locations[locations['id'] == idunplug_station]['longitude']
          lat_idunplug_station = locations[locations['id'] == idunplug_station]['latitude']
          lon_idplug_station = locations[locations['id'] == idplug_station]['longitude']
          lat_idplug_station = locations[locations['id'] == idplug_station]['latitude']

          unplug_station = Point(lon_idunplug_station, lat_idunplug_station)
          plug_station = Point(lon_idplug_station, lat_idplug_station)

          print(id_point)

          #zip_shp[unplug_station.within(zip_shp['geometry'][i])]

          for i in range(0, len(zip_shp['geometry'])):
            if unplug_station.within(zip_shp['geometry'][i]):
              origin_zip = zip_shp['COD_POSTAL'][i]
            if plug_station.within(zip_shp['geometry'][i]):
              dest_station = zip_shp['COD_POSTAL'][i]

          return origin_zip + ',' + dest_station

    grouped_byzip = df.groupby(groupby_zipCode)
    grouped_byzip_count = grouped_byzip.count().reset_index()

    new = grouped_byzip_count["index"].str.split(",", n=1, expand=True)
    grouped_byzip_count["origin_zip"] = new[0]
    grouped_byzip_count["dest_zip"] = new[1]
    grouped_byzip_count = grouped_byzip_count[['origin_zip', 'dest_zip', '_id']]
    grouped_byzip_count = grouped_byzip_count.rename(columns={"_id": "travels"})

    grouped_byzip_count.to_csv(os.path.join(getRootPath(), 'data/bike/' + year + month + '_movements_inZip.csv'))

def preprocessBikeTravelsSankeyDistritos(year, month):

    if not(os.path.exists(os.path.join(getRootPath(), 'data/bike/stations_locations_PROCESSED.csv'))):
        preprocessStationsLocation()

    locations = pd.read_csv(os.path.join(getRootPath(), 'data/bike/stations_locations_PROCESSED.csv'))




    filepath = os.path.join(getRootPath(), 'data/bike/raw_data/' + year + str(month) + '_movements.json')
    df = pd.read_json(open(filepath).read(), lines=True)
    df_movs = df[['_id', 'user_day_code', 'idunplug_station', 'idplug_station']]

    df_movsJoin1 = df_movs.merge(locations, left_on='idunplug_station', right_on='id', how='inner')
    df_movsJoin1.rename(
        columns={'name': 'unplug_stationName', 'address': 'unplug_stationAddress', 'longitude': 'unplug_stationLong',
                 'latitude': 'unplug_stationLat',
                 'barrio': 'unplug_stationBarrio', 'distrito': 'unplug_stationDistrito',
                 'cod_postal': 'unplug_stationZipCode'}, inplace=True)

    df_movsJoin1 = df_movsJoin1[['_id', 'user_day_code', 'idunplug_station', 'idplug_station',
                                 'unplug_stationName', 'unplug_stationAddress', 'unplug_stationLong',
                                 'unplug_stationLat',
                                 'unplug_stationBarrio', 'unplug_stationDistrito', 'unplug_stationZipCode']]

    df_movsJoin2 = df_movsJoin1.merge(locations, left_on='idplug_station', right_on='id', how='inner')
    df_movsJoin2.rename(columns={'name': 'plug_stationName', 'address': 'plug_stationAddress',
                                 'longitude': 'plug_stationLong', 'latitude': 'plug_stationLat',
                                 'barrio': 'plug_stationBarrio', 'distrito': 'plug_stationDistrito',
                                 'cod_postal': 'plug_stationZipCode'}, inplace=True)

    df_movs_loc = df_movsJoin2[['_id', 'user_day_code', 'idunplug_station', 'idplug_station',
                                'unplug_stationName', 'unplug_stationAddress', 'unplug_stationLong',
                                'unplug_stationLat',
                                'unplug_stationBarrio', 'unplug_stationDistrito', 'unplug_stationZipCode',

                                'plug_stationName', 'plug_stationAddress', 'plug_stationLong', 'plug_stationLat',
                                'plug_stationBarrio', 'plug_stationDistrito', 'plug_stationZipCode']]


    grouped_byName = df_movs_loc.groupby(['unplug_stationDistrito', 'plug_stationDistrito'])
    grouped_byName_count = grouped_byName.count().reset_index()
    grouped_byName_count = grouped_byName_count[['unplug_stationDistrito', 'plug_stationDistrito', '_id']]
    grouped_byName_count = grouped_byName_count.rename(columns={"_id": "travels"})

    grouped_byName_count.to_csv(os.path.join(getRootPath(), 'data/bike/' + year + str(month) + '_movements_Distritos.csv'))



#FUNCIONES PREPROCESS STATIONS LOCATIONS
def get_zipcode(long_st, lat_st):
    zip_shp_MADRID = gpd.read_file(open(os.path.join(getRootPath(), "data/distritos/MADRID.json")).read())

    lon_station = long_st
    lat_station = lat_st
    station_Point = Point(lon_station, lat_station)

    zipcode = 'Not Found'
    for i in range(0, len(zip_shp_MADRID['geometry'])):

        if station_Point.within(zip_shp_MADRID['geometry'][i]):
            zipcode = zip_shp_MADRID['COD_POSTAL'][i]

    return zipcode


def get_distrito(long_st, lat_st):
    zip_shp_DISTRICTS = gpd.read_file(open(os.path.join(getRootPath(), "data/distritos/distrito_geojson.geojson")).read())

    lon_station = long_st
    lat_station = lat_st
    station_Point = Point(lon_station, lat_station)

    distrito = 'Not Found'
    for i in range(0, len(zip_shp_DISTRICTS['geometry'])):

        if station_Point.within(zip_shp_DISTRICTS['geometry'][i]):
            distrito = zip_shp_DISTRICTS['label'][i]

    return distrito


def get_barrio(long_st, lat_st):
    zip_shp_BARRIOS = gpd.read_file(open(os.path.join(getRootPath(), "data/distritos/barrios.geojson")).read())

    lon_station = long_st
    lat_station = lat_st
    station_Point = Point(lon_station, lat_station)

    barrio = 'Not Found'
    for i in range(0, len(zip_shp_BARRIOS['geometry'])):

        if station_Point.within(zip_shp_BARRIOS['geometry'][i]):
            barrio = zip_shp_BARRIOS['name'][i]

    return barrio

#Añadir en file locations barrio, zipcode y distrito
def preprocessStationsLocation ():
    locations = pd.read_json(open(os.path.join(getRootPath(), "data/bike/raw_data/stations_location.json")))
    locations = locations[['name', 'address', 'longitude', 'latitude', 'id']]

    locations['barrio'] = locations.apply(lambda x: get_barrio(x.longitude, x.latitude), axis=1)
    locations['distrito'] = locations.apply(lambda x: get_distrito(x.longitude, x.latitude), axis=1)
    locations['cod_postal'] = locations.apply(lambda x: get_zipcode(x.longitude, x.latitude), axis=1)

    locations.to_csv(os.path.join(getRootPath(), 'data/bike/stations_locations_PROCESSED.csv'))


    return locations




