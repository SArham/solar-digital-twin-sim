
class Cell:
    options = {
        "power_STC": 600,        # Watts
        "power_NOCT": 454,       # Watts
        "module_length": 2.172,  # meters
        "module_width": 1.303,   # meters
        "module_depth": 0.040,   # meters
        "module_weight": 35.3,   # kg
        "number_of_cells": 120,  # units
        "I_sc_ref": 18.42,       # Amps
        "V_oc_ref": 41.7,        # Volts
        "I_mp_ref": 17.34,       # Amps
        "V_mp_ref": 34.6,        # Volts
        "T_coef_I_sc": 0.04,     # % / C
        "T_coef_V_oc": -0.25,    # % / C
        "T_NOCT": 43,            # degrees
        "T_coef_P_max": -0.0037  # % / C
    }
    power = []
    temp = []
    time = []

    def __init__(self, cell_no, **kwargs):
        self.cell_no = cell_no
        self.options.update(kwargs)
        self.options["module_area"] = self.options["module_length"] * self.options["module_width"]
        self.options["alpha_sc"] = self.options["T_coef_I_sc"] * self.options["I_sc_ref"]   # A / deg C
        self.options["beta_oc"] = self.options["T_coef_V_oc"] * self.options["V_oc_ref"]  # V / deg C
        self.options["gamma_pdc"] = self.options["T_coef_P_max"] * self.options["power_STC"] / 272.15  # % / deg C

    def get(self, key):
        return self.options[key]

    def set_power(self, power, time):
        self.power.append(power)
        self.time.append(time)

    def set_temp(self, temp):
        self.temp.append(temp)

    def __call__(self):
        pass
