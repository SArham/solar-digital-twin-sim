import pandas as pd
import numpy as np

import pvlib


class Inverter:
    # Inverter Parameters
    inverter_efficiency = 0.968  # 96.8%
    inverter_power_dc = 26000  # Watts
    # inverter_power_ac = 6000
    inverter_power_ac = inverter_efficiency * inverter_power_dc  # Watts
    # inverter_power_dc = 6900 # Watts

    Vac = 230  # Volts
    Pso = 2  # Watts
    Vdco = 330  # Rated input current Volts
    Pnt = 2  # Watts
    Vdcmax = 600  # Volts
    Idcmax = 11  # Amps
    Mppt_low = 90  # Min MPPT Volts
    Mppt_high = 520  # Max MPPT Volts

    C0 = 0
    C1 = 0
    C2 = 0
    C3 = 0

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

    def __call__(self, *args, **kwargs):
        pass