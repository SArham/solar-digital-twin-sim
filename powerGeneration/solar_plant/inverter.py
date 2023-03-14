from os.path import join
import pandas as pd
import numpy as np

import pvlib
from solar_plant.data_source import OUT_PATH


class Inverter:
    name = "Sunny Tripower CORE1 33-US"
    reference = "https://sunwatts.com/content/specs/SMA%20Sunny%20Tripower%20Core1%20Datasheet.pdf"
    # Inverter Parameters
    inverter_efficiency = 0.975
    inverter_power_dc = 35000  # Watts
    inverter_power_ac = inverter_efficiency * inverter_power_dc  # Watts

    Vac = 305  # Volts
    Pso = 2  # Watts
    Vdco = 330  # Rated input current Volts
    Pnt = 2  # Watts
    Vdcmax = 1000  # Volts
    Idcmax = 120  # Amps
    Mppt_low = 150  # Min MPPT Volts
    Mppt_high = 1000  # Max MPPT Volts

    C0 = 0
    C1 = 0
    C2 = 0
    C3 = 0

    power_in = []
    power_out = []
    time = []

    def __init__(self):
        self.base_parameters = {
            'pdc0': self.inverter_power_dc,
            'eta_inv_nom': self.inverter_efficiency}

        self.parameters = pd.DataFrame(
            {'Vac': self.Vac,
             'Pso': self.Pso,
             'Paco': self.inverter_power_ac,
             'Pdco': self.inverter_power_dc,
             'Vdco': self.Vdco,
             'C0': self.C0,
             'C1': self.C1,
             'C2': self.C2,
             'C3': self.C3,
             'Pnt': self.Pnt,
             'Vdcmax': self.Vdcmax,
             'Idcmax': self.Idcmax,
             'Mppt_low': self.Mppt_low,
             'Mppt_high': self.Mppt_high}, index=[0])

    def get_module(self):
        trans_param = self.parameters.transpose()
        inv = pvlib.pvsystem.retrieve_sam('cecinverter')
        inverter = inv.copy()
        inverter['New Inverter'] = pd.Series(np.float64)
        inverter['New Inverter'] = trans_param
        return inverter

    def add_power(self, dc_pow, ac_pow, time):
        self.power_in.append(dc_pow)
        self.power_out.append(ac_pow)
        self.time.append(pd.Timestamp(time))

    def create_csv(self):
        data_dict = {}
        data_dict["timestamp"] = self.time
        data_dict[f"dc_power"] = self.power_in
        data_dict[f"ac_power"] = self.power_out

        data = pd.DataFrame(data_dict)
        saving_path = join(OUT_PATH, "inverter.csv")
        data.to_csv(saving_path, index=False)

    def __call__(self, *args, **kwargs):
        pass