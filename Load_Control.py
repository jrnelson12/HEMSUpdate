# Load Energy Asset

from HEMS_data import HEMSData

data = HEMSData()
import math


def Load(load, maxCurtail, curtail, loadBank):
    if curtail > maxCurtail:
        curtail = maxCurtail
    else:
        curtail = curtail
    totalLoadPower = load - load*curtail
    loadBank = loadBank + load*curtail

    return totalLoadPower, loadBank, curtail
