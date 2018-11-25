import feedparser
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import folium
import os
%matplotlib notebook

### GeoRSS
GDACS = 'http://www.gdacs.org/xml/rss.xml'
COPERNICUS_RAPID_MAPPING = 'http://emergency.copernicus.eu/mapping/activations-rapid/feed'
EONET = 'https://eonet.sci.gsfc.nasa.gov/api/v2.1/events/rss.xml'
NOAA_TSUNAMI = 'https://ptwc.weather.gov/feeds/ptwc_rss_pacific.xml'

RSS_URLS = [GDACS, NOAA_TSUNAMI, COPERNICUS_RAPID_MAPPING]

feeds = []
guid = []
xy = []
title = []
desc = []
link = []

for url in RSS_URLS:
    feeds.append(feedparser.parse(url))

for feed in feeds:
    for post in feed.entries:
        guid.append(post.guid)
        xy.append(post.where)
        title.append(post.title)
        desc.append(post.description)
        link.append(post.link)
        
    #print len(guid, title, coords)
    df_guid['guid'] = pd.DataFrame(guid)
    df_xy = pd.DataFrame(xy)
    df_title['title'] = pd.DataFrame(title)
    df_desc['desc'] = pd.DataFrame(desc)
    df_link['link'] = pd.DataFrame(link)
    
    frames = [df_guid['guid'], df_xy, df_title['title'], df_desc['desc'], df_link['link']]
    
    data = pd.concat([df_guid['guid'], df_xy, df_title['title'], df_desc['desc'], df_link['link']],axis=1, ignore_index=False)

#data
#f = 'C:/Users/Michael/Desktop/Notebooks/test.csv'
#data.to_csv(f, encoding='utf-8')

geometry = [Point(xy) for xy in zip(data['coordinates'])]
df = data.drop(['coordinates'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
gdf.head(3)

geodata = gpd.GeoDataFrame(gdf)
geodata.head(3)

jsondata = geodata.to_json()

m = folium.Map(tiles='stamentoner') #cartodbpositron #stamentoner #cartodbdark_matter
folium.GeoJson(jsondata).add_to(m)

m.fit_bounds(m.get_bounds())
#m.save(os.path.join('results', 'geopandas_2.html'))
m
