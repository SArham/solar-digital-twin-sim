from astral import LocationInfo

from astral.sun import azimuth, zenith
import pytz
from datetime import datetime
import pvlib
import pandas as pd

from solar_plant.inverter import Inverter
from solar_plant.cell_array import CellArray
from solar_plant.data_source import CustomData
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

class PowerPlant:
    # Coordinates of the Location
    latitude = 24.953534
    longitude = 67.051792

    def __init__(self):
        self.inverter = Inverter()
        self.array1 = CellArray()

        self.array_module = self.array1.get_module()
        self.inverter_module = self.inverter.get_module()

        # Defining a location for pvlib and astral
        location = pvlib.location.Location(
            latitude=self.latitude,
            longitude=self.longitude,
            tz='Asia/Karachi')
        loc = LocationInfo(
            name='Solar Plant 1',
            region='Karachi, Pakistan',
            timezone='Asia/Karachi',
            latitude=self.latitude,
            longitude=self.longitude)

        self.data = CustomData()

        timezone = pytz.timezone("Asia/Karachi")

        all_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']
        parameters = all_parameters['open_rack_glass_polymer']

        dc_output = []
        ac_output = []
        azim = []
        zen = []
        cell_temp = []
        irradiance_list = []
        timestamps = []
        for (index, row) in tqdm(self.data()):
            t = datetime.strptime(row['datetime'], '%Y%m%d%H%M')
            row_time = t.astimezone(timezone)
            row_azimuth = azimuth(loc.observer, row_time)
            row_zenith = zenith(loc.observer, row_time)

            irradiance_df = pvlib.irradiance.get_total_irradiance(
                surface_tilt=self.array1.tilt_angle,
                surface_azimuth=self.array1.surface_azimuth,
                dni=row['dni'],
                ghi=row['ghi'],
                dhi=row['dhi'],
                solar_zenith=row_zenith,
                solar_azimuth=row_azimuth,
                model='isotropic')

            cell_temperature = pvlib.temperature.sapm_cell(
                irradiance_df['poa_global'],
                row['temp_air'],
                row['wind_speed'],
                **parameters)

            dc_power_output = pvlib.pvsystem.pvwatts_dc(
                irradiance_df['poa_global'],
                cell_temperature,
                self.array1.power,
                self.array1.parameters['gamma_r'])

            ac_power_output = pvlib.inverter.pvwatts(
                dc_power_output,
                self.inverter.inverter_power_ac/self.inverter.inverter_efficiency,
                self.inverter.inverter_efficiency,
                eta_inv_ref=0.9637)

            self.array1.add_power_and_temp(dc_power_output[0], t, cell_temperature)
            self.inverter.add_power(dc_power_output[0], ac_power_output[0], t)

            irradiance_list.append(irradiance_df["poa_global"])
            cell_temp.append(cell_temperature)
            dc_output.append(dc_power_output[0])
            ac_output.append(ac_power_output[0])
            azim.append(row_azimuth)
            zen.append(row_zenith)
            timestamps.append(pd.Timestamp(row_time))

        self.data.data["irradiance"] = irradiance_list
        self.data.data["cell_temp"] = cell_temp
        self.data.data["solar_zenith"] = zen
        self.data.data["solar_azimuth"] = azim
        self.data.data["dc_output"] = dc_output
        self.data.data["ac_output"] = ac_output
        self.data.create_csv()
        self.array1.create_csv()
        self.inverter.create_csv()


if __name__ == '__main__':
    power_plant = PowerPlant()
