import pandas as pd
import numpy as np
from solar_plant.cell import Cell

import pvlib

class CellArray:
    cells = []
    tilt_angle = 20  # degrees
    surface_azimuth = 180  # the panels are facing south

    power = 0

    def __init__(self, cell_no=100):
        for _ in range(0, cell_no):
            cell = Cell()
            cell_power = cell.get("power_STC")
            self.power += cell_power if cell_power is not None else 0
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

    def get_module(self):
        transposed_params = self.parameters.transpose()
        modules = pvlib.pvsystem.retrieve_sam('cecmod')
        module = modules.copy()
        module['New Module'] = pd.Series(np.float64)
        module['New Module'] = transposed_params
        return module

    def __call__(self, *args, **kwargs):
        pass