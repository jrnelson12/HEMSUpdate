# Grid Energy Asset

from HEMS_data import HEMSData
data = HEMSData()
import math

def Grid(totalLoadPower, energyCost, netMetering):
    if totalLoadPower >= 0:
        totalCost = totalLoadPower*energyCost
    else:
        totalCost = totalLoadPower*netMetering*(-1)
    #Todo add demand charges
    return totalCost
