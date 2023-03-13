from astral import LocationInfo

from astral.sun import azimuth, zenith
import pytz
from datetime import datetime
import pvlib

from solar_plant.inverter import Inverter
from solar_plant.cell_array import CellArray
from solar_plant.data_source import CustomData

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
            longitude=self.longitude)
        loc = LocationInfo(
            name='Solar Plant 1',
            region='Karachi, Pakistan',
            timezone='Asia/Karachi',
            latitude=self.latitude,
            longitude=self.longitude)

        self.data = CustomData()

        timezone = pytz.timezone("Asia/Karachi")
        utc = pytz.timezone("UTC")

        all_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']
        parameters = all_parameters['open_rack_glass_polymer']

        system = pvlib.pvsystem.PVSystem(
            name='Karachi Array',
            module=self.array_module,
            module_parameters={'pdc0': self.array1.cells[0].get("power_STC"),
                               'gamma_pdc': self.array1.parameters['gamma_r']},
            surface_tilt=self.array1.tilt_angle,
            surface_azimuth=self.array1.surface_azimuth,
            temperature_model_parameters=parameters,
            inverter=self.inverter_module,
            inverter_parameters={'pdc0': self.inverter.inverter_power_dc,
                                 'eta_inv_nom': self.inverter.inverter_efficiency},
            modules_per_string=100,
            strings_per_inverter=1)

        mc = pvlib.modelchain.ModelChain(
            system,
            location,
            aoi_model='physical',
            spectral_model='no_loss')

        for (index, row) in self.data():
            row_time = datetime.strptime(row['datetime'], '%Y%m%d%H%M').astimezone(timezone)
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
                row['wind_speed'], **parameters)

            dc_power_output = pvlib.pvsystem.pvwatts_dc(
                irradiance_df['poa_global'],
                cell_temperature,
                self.array1.power,
                self.array1.parameters['gamma_r']
            )

            ac_power_output = pvlib.inverter.pvwatts(
                dc_power_output,
                self.inverter.inverter_power_ac/self.inverter.inverter_efficiency,
                self.inverter.inverter_efficiency,
                eta_inv_ref=0.9637
            )

            # ModelChain
            # weather_data = pd.DataFrame(self.data.data, index=[index])
            # weather_data = weather_data[['albedo',
            # 'dni',
            # 'ghi',
            # 'dhi',
            # 'wind_speed',
            # 'temp_air']]

            print(dc_power_output[0], ac_power_output[0])



if __name__ == '__main__':
    power_plant = PowerPlant()
