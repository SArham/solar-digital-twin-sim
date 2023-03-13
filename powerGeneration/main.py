import numpy as np
import pandas as pd

from astral import LocationInfo
from astral.sun import sun
import pytz
import pvlib

from solar_plant.inverter import Inverter
from solar_plant.cell_array import CellArray
from solar_plant.data_source import CustomData


class PowerPlant:
    # Coordinates of the Location
    latitude = 24.953534
    longitude = 67.051792

    def __init__(self):
        self.inverter = Inverter()
        self.array1 = CellArray()

        self.array_module = self.array1.get_module()
        self.inverter_module = self.inverter.get_module()


        # Defining a location for PVLIB
        location = pvlib.location.Location(latitude=self.latitude, longitude=self.longitude)
        loc = LocationInfo(name='Main Location',
                           region='Karachi, Pakistan',
                           timezone='Asia/Karachi',
                           latitude=self.latitude,  # 55.865408,
                           longitude=self.longitude)  # -3.199696

        self.data = CustomData()

        timezone = pytz.timezone("PKT")
        UTC = pytz.timezone("UTC")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    power_plant = PowerPlant()
