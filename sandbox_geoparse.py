import feedparser
import requests
import matplotlib.pyplot as plt
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import folium
import os
%matplotlib notebook

### GDACS GeoRSS
GDACS = 'http://www.gdacs.org/xml/rss.xml'

RSS_URL = [GDACS]

feed = []
iso3 = []
country = []
etype = []
epid = []
evid = []
guid = []
pubdate = []
bbox = []
coords = []
alevel = []
ascore = []

wfpiso3 = ['CHL', 'IDN', 'PHL', 'SDN', 'SSD', 'DRC', 'BGD', 'CAF', 'BWA', 'TCD', 'KHM']

def get_data():
    for url in RSS_URL:
        feeds.append(feedparser.parse(url))

    for feed in feeds:
        for post in feed.entries:
            iso3.append(post.gdacs_iso3)
            country.append(post.gdacs_country)
            etype.append(post.gdacs_eventtype)
            epid.append(post.gdacs_episodeid)
            evid.append(post.gdacs_eventid)
            guid.append(post.guid)
            pubdate.append(post.published)
            bbox.append(post.gdacs_bbox)
            coords.append(post.where)
            alevel.append(post.gdacs_episodealertlevel)
            ascore.append(post.gdacs_alertscore)
            
        guiddf = pd.DataFrame(guid)       #0
        pubdatedf = pd.DataFrame(pubdate) #1
        isodf = pd.DataFrame(iso3)        #2   
        countrydf = pd.DataFrame(country) #3
        etypedf = pd.DataFrame(etype)     #4
        epidf = pd.DataFrame(epid)        #5
        evidf = pd.DataFrame(evid)        #6
        bboxdf = pd.DataFrame(bbox)       #7
        coordf = pd.DataFrame(coords)     #8 #9
        aleveldf = pd.DataFrame(alevel)   #10
        ascoredf = pd.DataFrame(ascore)   #11
        
        frames = [guiddf, pubdatedf, isodf, countrydf, etypedf, epidf, evidf, bboxdf,coordf, aleveldf, ascoredf]
        df = pd.concat(frames, axis=1, ignore_index = True, names=[frames])
        return df[df[2].isin(wfpiso3)] #!IMPORTANT!#
        #return df
        

data = get_data()
data
#f = 'C:/Users/Michael/Desktop/Notebooks/test.csv'
#data.to_csv(f, encoding='utf-8')  

geometry = [Point(xy) for xy in zip(data[8])]
gdacsdf = data.drop([8], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(gdacsdf, crs=crs, geometry=geometry)
gdf.head()

#Same as line 75/56
#geodata = gpd.GeoDataFrame(gdf)
#geodata.head(3)

jsondata = geodata.to_json()

m = folium.Map(tiles='stamentoner') #cartodbpositron #stamentoner #cartodbdark_matter
folium.GeoJson(jsondata).add_to(m)

m.fit_bounds(m.get_bounds())
#m.save(os.path.join('results', 'geopandas_2.html'))
m
