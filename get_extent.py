import fiona
from fiona import errors
import rasterio
from rasterio import RasterioIOError
import os
import pandas as pd
import numpy as np
import geopandas
from geopandas import GeoDataFrame
import shapely
from shapely.geometry import Point


shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
csv_ex = "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv"

def get_extent_for_vector(shapefile):
    lats = []
    lons = []
    with fiona.open(shapefile, 'r') as src:
        for feat in src:
            coords = feat['geometry']['coordinates'][0] # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
            [(lons.append(x), lats.append(y)) for x, y in coords]

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    print('South extent: {}\nNorth extent: {}\nWest extent: {}\nEast extent: {}'.format(min_lat,
                                                                                        max_lat,
                                                                                        min_lon,
                                                                                        max_lon))
#get_extent_for_vector(shp_fn)


def get_extent_for_raster(raster):
    ds = rasterio.open(raster, 'r')
    print(ds.bounds)

#get_extent_for_raster(rast_ex)



# Now I need to turn this into a function and make it into a bounding box
df = pd.read_csv("/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv")
geometry = [Point(xy) for xy in zip(df.Long, df.Lat)]
df = df.drop(['Long', 'Lat'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
print(gdf)

#stopped here
bounds = geopandas.GeoSeries.bounds()

geoser = geopandas.GeoSeries(gdf)

gdf.bounds()


# this is unsuccessful
def get_extent_csv(file_path):
    df = pd.read_csv(file_path)
    for col in df: #hmm I think I need it to skip the first row, possibly by setting index, I think this is already default?
        coords = df.iterrows()
        print(coords)

get_extent_csv(csv_ex)


'''
This: https://gis.stackexchange.com/questions/174159/convert-a-pandas-dataframe-to-a-geodataframe
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df.Lon, df.Lat)]
df = df.drop(['Lon', 'Lat'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)

Maybe this: https://gis.stackexchange.com/questions/114066/handling-kml-csv-with-geopandas-drivererror-unsupported-driver-ucsv

import pandas as pd
import geopandas as gp
from shapely.geometry import Point

stations = pd.read_csv('../data/stations.csv')
stations['geometry'] = stations.apply(lambda z: Point(z.X, z.Y), axis=1)
stations = gp.GeoDataFrame(stations)

Maybe this: https://gist.github.com/tchajed/93c347aeb2b24f034ea3

'''

# Old pandas code
for row, col in df1.iterrows():
    if col['Circumference'] > 0.0:
        dense = missbark(bk_mass=col['DryMassBark'], ba=col['bark_area'], circ=col['Circumference'], cnb=col['CircNoBark'], thick=col['avg_thickness'])
    else:
        dense = bark(bk_mass=col['DryMassBark'], ba=col['bark_area'], thick=col['avg_thickness'])

    df1['bark_density'][row] = dense

'''
#Bonus Points!
def get_extent_for_csv(file_path, long_col_name=None, lat_col_name=None):
    """
    potential example with geopandas: https://gist.github.com/nygeog/2731427a74ed66ca0e420eaa7bcd0d2b
    
    # outline
    
    1. figure out column names if they're not provided 
    2. convert to point geodataframe (geopandas)
    """
    if long_col_name is None:
        # do stuff to figure out the long_col_name
        pass
'''
#need to put fiona error
# def get_extent_if_possible(file_path):
#     try:
#         extent = get_extent_for_vector(file_path)
#     except RasterioIOError:
#         extent = get_extent_for_raster(file_path)
#
#     return extent


def get_extent_if_possible(file_path):
    try:
        extent = get_extent_for_vector(file_path)
    except errors.FionaValueError:
        extent = get_extent_for_raster(file_path)

    return extent


get_extent_if_possible(shp_fn)
get_extent_if_possible(rast_ex)