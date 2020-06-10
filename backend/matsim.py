import gzip
import xml.sax

class PopulationReader(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.population = []

        self.person = None
        self.process_activities = False

    def startElement(self, name, attributes):
        if name == "person":
            self.person = { "id": attributes["id"], "activities": [] }
            self.process_activities = False

        elif name == "plan":
            self.process_activities = attributes["selected"] == "yes"

        elif name == "activity":
            self.person["activities"].append({
                "purpose": attributes["type"],
                "x": float(attributes["x"]),
                "y": float(attributes["y"])
            })

    def endElement(self, name):
        if name == "person":
            self.population.append(self.person)
            self.person = None

def read_population(path):
    with gzip.open(path) as f:
        reader = PopulationReader()
        xml.sax.parse(f, reader)
        return reader.population
