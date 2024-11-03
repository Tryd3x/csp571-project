# This file serves as a primary purpose to load chicago base map
# It can still be used in conjugation with crime data to obtain relevant results for visualization

import geopandas as gpd
import pandas as pd
from shapely import wkt
import plotly.express as px
import plotly.graph_objects as go

class ChicagoMap:
    def __init__(self,):
        # Loading Wards
        wards_df = pd.read_csv("../assets/maps/wards.csv")
        wards_df['geometry'] = wards_df['the_geom'].apply(wkt.loads)
        wards_df.drop(columns=['the_geom'],inplace=True)

        # Loading Districts
        districts_df = pd.read_csv('../assets/maps/districts.csv')
        districts_df['geometry'] = districts_df['the_geom'].apply(wkt.loads)
        districts_df.drop(columns=['the_geom'],inplace=True)

        self.district_gdf = gpd.GeoDataFrame(districts_df, geometry='geometry') 
        self.wards_gdf = gpd.GeoDataFrame(wards_df, geometry='geometry')
        
    def getWardsGeoDataFrame(self,):
        return self.wards_gdf

    def getDistrictGeoDataFrame(self,):
        return self.district_gdf

    def plot_ward(self,):
        return px.choropleth_mapbox(
            self.wards_gdf,
            geojson=self.wards_gdf.__geo_interface__,
            locations=self.wards_gdf.index,
            mapbox_style="carto-positron",
            zoom=10,
            center={"lat": 41.8781, "lon": -87.6298},  # Center on Chicago
            opacity=0.4,
            height = 800,
            title='Chicago Ward Map',
            hover_name='Ward',
        )
    
    def plot_district(self,):
        return px.choropleth_mapbox(
            self.district_gdf,
            geojson=self.district_gdf.__geo_interface__,
            locations=self.district_gdf.index,
            mapbox_style="carto-positron",
            zoom=10,
            center={"lat": 41.8781, "lon": -87.6298},  # Center on Chicago
            opacity=0.4,
            height = 800,
            title='Chicago District Map',
        )
