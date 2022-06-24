import os

import ee
import folium
import webbrowser
from local.credentails import service_account

from geojson import geoJSON

credentials = ee.ServiceAccountCredentials(service_account, 'pKey.json')

ee.Initialize(credentials)


def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)


folium.Map.add_ee_layer = add_ee_layer


def addNDVI(image):
    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
    return image.addBands(ndvi)


def show_ndvi():
    lat, lon = geoJSON['coordinates'][1], geoJSON['coordinates'][0]

    point = ee.Geometry(geo_json=geoJSON)
    img_col = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')

    image = ee.Image(img_col.filterBounds(point).sort('CLOUD_COVER').first())
    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')

    ndvi_vis_params = {
        'min': -1, 'max': 1,
        'palette': ['blue', 'white', 'green']
    }

    ndvi_col = img_col.map(addNDVI)

    ndvi_col_vis_params = {'bands': ['B4', 'B3', 'B2'], 'max': 0.3}

    map = folium.Map(location=[lat, lon], zoom_start=12)
    map.add_ee_layer(ndvi_col.qualityMosaic('NDVI'), ndvi_col_vis_params, 'NDVI')
    map.add_ee_layer(ndvi, ndvi_vis_params, 'simple NDVI')
    map.add_child(folium.LayerControl())
    map.save('index.html')


def get_map():
    lat, lon = geoJSON['coordinates'][1], geoJSON['coordinates'][0]

    map = folium.Map(location=[lat, lon], zoom_start=12)
    map.save('index.html')


def edit_geojson(latitude, longitude):
    geoJSON['coordinates'][1] = latitude
    geoJSON['coordinates'][0] = longitude
