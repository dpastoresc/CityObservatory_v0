import geopandas as gpd
import os
import json

def getRootPath():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CityObservatory')

def ZBSShapeFileToJson(shapeFilepath):
    data = gpd.read_file(shapeFilepath)
    #transforms read data to lat and long from utm
    data_latlong = data.to_crs('epsg:4326')
    #stores the info in a json
    data_latlong.to_file(shapeFilepath[:shapeFilepath.rfind('.')] + '.json', driver='GeoJSON')

def loadZBSShapeFile(shpfilePath):
    if not(os.path.exists(shpfilePath)):
        print("File, " + shpfilePath + "does not exist")
        exit(-1)
    data = gpd.read_file(shpfilePath)
    #transforms read data to lat and long from utm
    return data.to_crs('epsg:4326')


def loadZBSJson(jsonpath):
    if not(os.path.exists(jsonpath)):
        ZBSShapeFileToJson(jsonpath[:jsonpath.rfind('.')] + '.shp')
    with open(jsonpath) as f:
        return json.load(f)
