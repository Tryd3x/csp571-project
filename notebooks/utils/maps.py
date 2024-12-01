# This file serves as a primary purpose to load chicago base map
# It can still be used in conjugation with crime data to obtain relevant results for visualization

import geopandas as gpd
import pandas as pd
from shapely import wkt
import plotly.express as px

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
        districts_df = districts_df[districts_df['DIST_NUM'] !=31]

        # Loading Community Areas
        comm_df = pd.read_csv("../assets/maps/comm-areas.csv")
        comm_df['geometry'] = comm_df['the_geom'].apply(wkt.loads)
        comm_df.drop(columns=['the_geom'],inplace=True)

        self.district_gdf = gpd.GeoDataFrame(districts_df, geometry='geometry') 
        self.wards_gdf = gpd.GeoDataFrame(wards_df, geometry='geometry')
        self.comm_gdf = gpd.GeoDataFrame(comm_df, geometry='geometry')
        
    def getWardsGeoDataFrame(self,):
        return self.wards_gdf

    def getDistrictGeoDataFrame(self,):
        return self.district_gdf
    
    def getCommunityGeoDataFrame(self,):
        return self.comm_gdf

    def plot_ward(self,):
        fig =  px.choropleth_mapbox(
            self.wards_gdf,
            geojson=self.wards_gdf.__geo_interface__,
            locations=self.wards_gdf.index,
            mapbox_style="carto-positron",
            zoom=9.4,
            center={"lat": 41.8781, "lon": -87.6298},  # Center on Chicago
            opacity=0.2,
            height = 800,
            title='Chicago Ward Map',
        )
        fig.update_layout(showlegend=False)
        return fig
    
    def plot_district(self,):
        fig =  px.choropleth_mapbox(
            self.district_gdf,
            geojson=self.district_gdf.__geo_interface__,
            locations=self.district_gdf.index,
            mapbox_style="carto-positron",
            zoom=9.4,
            center={"lat": 41.8781, "lon": -87.6298},  # Center on Chicago
            opacity=0.2,
            height = 800,
            title='Chicago District Map',
        )
        fig.update_layout(showlegend=False)
        return fig
    
    def plot_community(self,):
        fig = px.choropleth_mapbox(
            self.comm_gdf,
            geojson=self.comm_gdf.__geo_interface__,
            locations=self.comm_gdf.index,
            mapbox_style="carto-positron",
            zoom=9.4,
            center={"lat": 41.8781, "lon": -87.6298},  # Center on Chicago
            opacity=0.2,
            height = 800,
            title='Chicago Community Map',
        )
        fig.update_layout(showlegend=False)
        return fig
