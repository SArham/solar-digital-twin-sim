from os.path import basename, dirname, join, abspath
from os import listdir
import pandas as pd


class CustomData:
    path = join(abspath(dirname(__file__)), "weather_data", "2924399_24.69_67.10_2017.csv")

    properties = ["DHI",
                  "DNI",
                  "GHI",
                  "Solar Zenith Angle",
                  "Temperature",
                  "Cloud Type"]
    cloud_types = ["Clear",
                   "Probably Clear",
                   "Fog",
                   "Water",
                   "Super-Cooled Water",
                   "Mixed",
                   "Opaque Ice",
                   "Cirrus",
                   "Overlapping",
                   "Overshooting",
                   "Unknown",
                   "Dust",
                   "Smoke"]

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", self.path)
        # Load CSV file into a dataframe
        self.data = pd.read_csv(self.path)

    def __call__(self, *args, **kwargs):
        return self.data

if __name__ == '__main__':
    data_source = CustomData()
