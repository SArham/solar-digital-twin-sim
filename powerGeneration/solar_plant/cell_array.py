from os.path import join
from random import uniform
from collections import defaultdict

import pandas as pd
import numpy as np
import pvlib

from solar_plant.cell import Cell
from solar_plant.data_source import OUT_PATH


class CellArray:
    cells = []
    tilt_angle = 20  # degrees
    surface_azimuth = 180  # the panels are facing south
    max_fluctuation_per = 0.07
    min_fluctuation_per = 0.02

    power = 0

    def __init__(self, cell_no=100):
        for cell_index in range(0, cell_no):
            cell = Cell(cell_index)
            cell_power = cell.get("power_STC")
            self.power += cell_power
            self.cells.append(cell)

        # Defining an Inverter and a Module Object
        self.base_module_parameters = {
            'pdc0': self.power,
            'gamma_pdc': self.cells[0].get("gamma_pdc")}

        self.parameters = pd.DataFrame(
            {'Technology': 'Mono-c-Si',
           'Bifacial': 0,
           'STC': self.cells[0].get("power_STC"),
           'PTC': self.cells[0].get("power_NOCT"),
           'A_c': self.cells[0].get("module_area"),
           'Length': self.cells[0].get("module_length"),
           'Width': self.cells[0].get("module_width"),
           'N_s': self.cells[0].get("number_of_cells"),
           'I_sc_ref': self.cells[0].get("I_sc_ref"),
           'V_oc_ref': self.cells[0].get("V_oc_ref"),
           'I_mp_ref': self.cells[0].get("I_mp_ref"),
           'V_mp_ref': self.cells[0].get("V_mp_ref"),
           'alpha_sc': self.cells[0].get("alpha_sc"),
           'beta_oc': self.cells[0].get("beta_oc"),
           'T_NOCT': self.cells[0].get("T_NOCT"),
           'BIPV': False,
           'gamma_r': self.cells[0].get("gamma_pdc")}, index=[0])

    def add_power_and_temp(self, dc_power, time, temp):
        self.__add_power(dc_power, time)
        self.__add_temperature(temp)

    def __add_power(self, dc_power, time):
        no_of_panels = len(self.cells)
        average_power = dc_power / no_of_panels
        max_fluctuation = average_power * self.max_fluctuation_per
        min_fluctuation = average_power * self.min_fluctuation_per
        for index in range(0, no_of_panels, 2):
            delta = uniform(min_fluctuation, max_fluctuation)
            self.cells[index].set_power(round(average_power + delta, 2), pd.Timestamp(time))
            self.cells[index+1].set_power(round(average_power - delta, 2), pd.Timestamp(time))

    def __add_temperature(self, temp):
        no_of_panels = len(self.cells)
        max_fluctuation = temp * self.max_fluctuation_per
        min_fluctuation = temp * self.min_fluctuation_per
        for index in range(0, no_of_panels, 2):
            delta = uniform(min_fluctuation, max_fluctuation)
            self.cells[index].set_temp(round(temp + delta, 2))
            self.cells[index + 1].set_temp(round(temp - delta, 2))

    def get_module(self):
        transposed_params = self.parameters.transpose()
        modules = pvlib.pvsystem.retrieve_sam('cecmod')
        module = modules.copy()
        module['New Module'] = pd.Series(np.float64)
        module['New Module'] = transposed_params
        return module

    def create_csv(self):
        data_dict = defaultdict(list)
        data_dict["timestamp"] = self.cells[0].time
        for index, cell in enumerate(self.cells):
            data_dict[f"cell_{cell.cell_no}_power"] = cell.power
            data_dict[f"cell_{cell.cell_no}_temp"] = cell.temp
        data = pd.DataFrame(data_dict)
        saving_path = join(OUT_PATH, "cell_array.csv")
        data.to_csv(saving_path, index=False)

    def __call__(self, *args, **kwargs):
        pass