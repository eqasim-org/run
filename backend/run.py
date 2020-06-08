from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)
api = Api(app)

import geopandas as gpd
import shapely.geometry as geo
import numpy as np
import pandas as pd

center = geo.Point(651791.0, 6862293.0)
radius = 10000

df_iris = gpd.read_file("../data/CONTOURS-IRIS.shp")
df_iris = df_iris[df_iris.geometry.centroid.distance(center) < radius]
# df_iris = df_iris.translate(-center.x, -center.y)

df_population = pd.read_excel(
    "../data/base-ic-evol-struct-pop-2015.xls",
    skiprows = 5
)
df_population = df_population[["IRIS", "P15_POP"]].rename(columns = { "IRIS": "CODE_IRIS" })
df_iris = pd.merge(df_iris, df_population, how = "left", on = "CODE_IRIS")

class Network(Resource):
    def get(self):
        def transform(iris_id, iris_name, population, shape):
            data = geo.mapping(shape)
            data.update(dict(properties = { "iris_id": iris_id, "iris_name": iris_name, "population": population }))
            return data

        return [
            transform(*item)
            for item in df_iris[["CODE_IRIS", "NOM_IRIS", "P15_POP", "geometry"]].itertuples(index = False)
        ]

api.add_resource(Network, '/network')

if __name__ == '__main__':
    app.run(debug = True)
