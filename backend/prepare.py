import geopandas as gpd
import shapely.geometry as geo
import numpy as np
import pandas as pd
from tqdm import tqdm
import pickle

center = geo.Point(651791.0, 6862293.0)
radius = 10000

df_iris = gpd.read_file("../data/CONTOURS-IRIS.shp")
df_iris = df_iris[df_iris.geometry.centroid.distance(center) < radius]

df_iris = df_iris[["CODE_IRIS", "geometry"]].rename(
    columns = { "CODE_IRIS": "iris_id" }
)

df_municipality = df_iris.copy()
df_municipality["municipality_id"] = df_municipality["iris_id"].str[:-4]
del df_municipality["iris_id"]
df_municipality = df_municipality.dissolve("municipality_id").reset_index()

df_trips = pd.read_csv("../data/trips_alpha1.0.csv", sep = ";")

df_trips["origin_geometry"] = [
    geo.Point(*p) for p in tqdm(zip(df_trips["origin_x"], df_trips["origin_y"]), total = len(df_trips))
]

df_trips["destination_geometry"] = [
    geo.Point(*p) for p in tqdm(zip(df_trips["destination_x"], df_trips["destination_y"]), total = len(df_trips))
]

df_trips = gpd.GeoDataFrame(df_trips, geometry = "origin_geometry")

print("Filtering origin geometry")
df_trips = df_trips.set_geometry("origin_geometry")
df_trips = df_trips[df_trips.centroid.distance(center) < radius]

print("Filtering destination geometry")
df_trips = df_trips.set_geometry("destination_geometry")
df_trips = df_trips[df_trips.centroid.distance(center) < radius]

print("Joining origin municipality")
df_trips = df_trips.set_geometry("origin_geometry")
df_trips = gpd.sjoin(df_trips, df_municipality, op = "within").drop(["index_right"], axis = 1)
df_trips = df_trips.rename(columns = { "municipality_id": "origin_municipality_id" })

print("Joining destination municipality")
df_trips = df_trips.set_geometry("destination_geometry")
df_trips = gpd.sjoin(df_trips, df_municipality, op = "within").drop(["index_right"], axis = 1)
df_trips = df_trips.rename(columns = { "municipality_id": "destination_municipality_id" })

with open("../data/trips.p", "wb+") as f:
    pickle.dump(df_trips, f)

print(df_trips)
