#!pip install geopandas, pandas, fiona
import geopandas
import pandas as pd
import fiona
import matplotlib.pyplot as plt

### read & prep Points file with Longitude & Latitude columns
points_df = pd.read_csv('./points.csv')
points_gdf = geopandas.GeoDataFrame(
    points_df, geometry=geopandas.points_from_xy(points_df.Longitude, points_df.Latitude))
print(points_gdf.head())

### read & prep Polygon (KML) file
geopandas.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
df1 = geopandas.read_file('./polygons.kml', driver='KML')
# convert Description column of KML file into DataFrame
df2 = pd.concat(list(map(lambda x : pd.read_html(x)[0].T.iloc[1:],geopandas.read_file('./polygons.kml')['Description'].values)))
# reindex resulting DataFrame
df2 = pd.DataFrame(df2.values,columns=[''])

polygons_df = pd.concat([df1,df2],1)
polygons_gdf = geopandas.GeoDataFrame(polygons_df)
print(polygons_gdf.head())

# use spatial joins
joined_gdf = geopandas.sjoin(points_gdf, polygons_gdf, how='left', op='within')
print(joined_gdf.head())

joined_df.to_csv("joined.csv", columns=['PointName', 'PolygonName'], index=False)
