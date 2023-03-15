from os.path import dirname, join, abspath

import pandas as pd


OUT_PATH = join(abspath(dirname(__file__)), "output")


class CustomData:
    names = ["2924399_24.69_67.10_2017.csv"] # , "2924399_24.69_67.10_2018.csv", "2924399_24.69_67.10_2019.csv"
    base_path = join(abspath(dirname(__file__)), "weather_data")
    path = join(abspath(dirname(__file__)), "weather_data", names[0])

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

        # self.data = pd.read_csv(self.path)
        self.data = self.join_dataframes()
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

        # self.data = self.data.head(100)

    def join_dataframes(self):
        dataframes = []
        for name in self.names:
            path = join(self.base_path, name)
            data = pd.read_csv(path)
            dataframes.append(data)
        combined_df = pd.concat(dataframes)
        combined_df.reset_index(drop=True)
        return combined_df

    def __call__(self):
        for (index, row) in self.data.iterrows():
            yield index, row

    def create_csv(self):
        saving_path = join(OUT_PATH, "overview_output.csv")
        self.data.to_csv(saving_path, index=False)


if __name__ == '__main__':
    data_source = CustomData()
    print(data_source.data.columns)
