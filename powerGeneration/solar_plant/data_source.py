from os.path import basename, dirname, join, abspath
from os import listdir
import pandas as pd
from datetime import datetime


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
        self.data["Year"] = self.data["Year"].astype(int)
        self.data["Month"] = self.data["Month"].astype(int)
        self.data["Day"] = self.data["Day"].astype(int)
        self.data["Hour"] = self.data["Hour"].astype(int)
        self.data["Minute"] = self.data["Minute"].astype(int)
        self.data["datetime"] = self.data.apply(lambda row:
            f"{row['Year'].astype(int)}{row['Month'].astype(int):02}{row['Day'].astype(int):02}{row['Hour'].astype(int):02}{row['Minute'].astype(int):02}", axis=1)
        self.data = self.data.rename(columns={
            'Surface Albedo': 'albedo',
            'DNI': 'dni',
            'GHI': 'ghi',
            'DHI': 'dhi',
            'Wind Speed': 'wind_speed',
            'Temperature': 'temp_air'
        })


    def __call__(self):
        for (index, row) in self.data.iterrows():
            yield index, row

if __name__ == '__main__':
    data_source = CustomData()
    print(data_source.data.columns)
