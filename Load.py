# Load Energy Asset

from HEMS_data import HEMSData
data = HEMSData()
import math

def ControllableLoad(controllableLoadPower, curtail):
    powerCurtail = controllableLoadPower * curtail
    powerNet = controllableLoadPower - powerCurtail

    return powerNet, powerCurtail

def Load(controllableLoadPower, curtail, uncontrollableLoadPower):
    powerNet, powerCurtail = ControllableLoad(controllableLoadPower, curtail)
    totalLoadPower = uncontrollableLoadPower + powerNet

    return totalLoadPower

