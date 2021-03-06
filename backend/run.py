from flask import Flask, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import request
import matsim
import threading

app = Flask(__name__)
CORS(app)
api = Api(app)

import geopandas as gpd
import shapely.geometry as geo
import numpy as np
import pandas as pd
import json, pickle
from tqdm import tqdm

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
df_municipality = df_municipality.dissolve("municipality_id")

df_households = pd.read_csv("../data/output/households.csv", sep = ";")
df_persons = pd.read_csv("../data/output/persons.csv", sep = ";")
df_activities = gpd.read_file("../data/output/activities.gpkg")

df_activities = df_activities[df_activities["purpose"] == "home"]
df_activities = gpd.sjoin(df_activities, df_iris, op = "within")

df_population = pd.merge(df_activities, df_persons, on = "person_id")
df_population = pd.merge(df_population, df_households, on = "household_id")

df_services = pd.read_csv("../data/services_price_2500.csv", sep = ";")
df_services["pickup_time"] = df_services["departure_time"] + df_services["waiting_time"]
df_services = df_services[["departure_time", "pickup_time", "origin_x", "origin_y"]]
df_services["id"] = np.arange(len(df_services))

population = matsim.read_population("../data/output_plans.xml.gz")

with open("../data/trips.p", "rb") as f:
    df_trips = pickle.load(f)

class SkimMatrixManager:
    def __init__(self, df):
        self.df = df
        self.matrices = {}

    def calculate(self, identifier, settings):
        self.matrices[identifier] = dict(
            status = {
                "state": "processing", "progress": 0.0
            }
        )

        attribute = settings["attribute"]
        metric = settings["metric"]

        df_output = []

        unique_origins = self.df["origin_municipality_id"].unique()
        unique_destinations = self.df["destination_municipality_id"].unique()

        total_count = len(unique_origins) * len(unique_destinations)
        current_count = 0

        destination_filters = {}

        for origin in unique_origins:
            f_origin = self.df["origin_municipality_id"] == origin

            for destination in unique_destinations:
                if not destination in destination_filters:
                    destination_filters[destination] = self.df["destination_municipality_id"] == destination

                f_destination = destination_filters[destination]

                df_relation = self.df[f_origin & f_destination]

                df_output.append(dict(
                    origin_municipality_id = origin, destination_municipality_id = destination,
                    value = df_relation[attribute].aggregate(metric)
                ))

                current_count += 1
                self.matrices[identifier]["status"]["progress"] = current_count / total_count

                print(current_count / total_count)

        df_output = pd.DataFrame.from_records(df_output)

        self.matrices[identifier]["data"] = df_output
        self.matrices[identifier]["status"] = dict(state = "done")

    def get_status(self, identifier):
        return self.matrices[identifier]["status"]

    def get_data(self, identifier):
        return self.matrices[identifier]["data"]

skim_matrix_manager = SkimMatrixManager(df_trips)
#skim_matrix_manager.calculate("abc", { "attribute": "travel_time", "metric": "mean" })

class SkimMatrixLayerStatus(Resource):
    def get(self, identifier):
        return skim_matrix_manager.get_status(identifier)

class SkimMatrixLayerCalculate(Resource):
    def get(self, identifier, attribute, metric):
        threading.Thread(target = lambda: skim_matrix_manager.calculate(identifier, dict(
            attribute = attribute,
            metric = metric
        ))).start()

class SkimMatrixLayerData(Resource):
    def get(self, identifier):
        df_data = skim_matrix_manager.get_data(identifier)
        return json.loads(df_data.to_json(orient = "records"))

class SkimMatrixLayerShape(Resource):
    def get(self, identifier):
        return json.loads(df_municipality.reset_index().to_json())

def gini(x):
    """Compute Gini coefficient of array of values"""
    diffsum = 0
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))
    return diffsum / (len(x)**2 * np.mean(x))

class RequestsLayer(Resource):
    def get(self):
        return json.loads(df_services.to_json(orient = "records"))

class ActivitiesLayer(Resource):
    def get(self, person_id):
        for person in population:
            if person["id"] == person_id:
                return person["activities"]

class PersonsLayer(Resource):
    def get(self):
        persons = []

        for person in population:
            for activity in person["activities"]:
                if activity["purpose"] == "home":
                    distance = np.sqrt((activity["x"] - center.x)**2 + (activity["y"] - center.y)**2)

                    if distance < radius:
                        persons.append(dict(
                            id = person["id"],
                            x = activity["x"],
                            y = activity["y"]
                        ))
                    break

        return persons

class PopulationLayer(Resource):
    def get(self, attribute, metric):
        if not attribute in ("age", "income"):
            return { "error": "Unknown attribute: %s" % attribute }, 400

        if not metric in ("mean", "median", "q10", "q90", "min", "max", "gini"):
            return { "error": "Unknown metric: %s" % metric }, 400

        aggregator = metric if metric in ("mean", "median", "min", "max") else None
        if metric == "q10": aggregator = lambda x: x.quantile(0.1)
        if metric == "q90": aggregator = lambda x: x.quantile(0.9)
        if metric == "gini": aggregator = gini

        df_response = df_population.groupby("iris_id")[attribute].aggregate(aggregator).reset_index()
        df_response = df_response.rename(columns = { attribute: "value" })
        df_response = pd.merge(df_iris, df_response, on = "iris_id")

        response = json.loads(df_response.to_json())

        if attribute == "age":
            response.update(dict(minimumValue = 0, maximumValue = 100))
        elif attribute == "income":
            response.update(dict(minimumValue = 0, maximumValue = df_response["value"].max()))

        if metric == "gini":
            response.update(dict(minimumValue = 0, maximumValue = 1))

        return response

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
api.add_resource(RequestsLayer, '/requests')
api.add_resource(PersonsLayer, '/persons')
api.add_resource(ActivitiesLayer, '/activities/<string:person_id>')
api.add_resource(PopulationLayer, '/population/<string:attribute>/<string:metric>')
api.add_resource(SkimMatrixLayerStatus, "/skim/status/<string:identifier>")
api.add_resource(SkimMatrixLayerCalculate, "/skim/calculate/<string:identifier>/<string:attribute>/<string:metric>")
api.add_resource(SkimMatrixLayerData, "/skim/data/<string:identifier>")
api.add_resource(SkimMatrixLayerShape, "/skim/shape/<string:identifier>")

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
