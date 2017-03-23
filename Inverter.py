# Inverter Energy Asset

from HEMS_data import HEMSData
data = HEMSData()
import math

def Inverter(powerOutputDC, inverterEff, pvCapacity, invertCapacity):
    #check if inverter is size aduquatly
    if pvCapacity < invertCapacity:
        print ('Inverter is oversized')
    elif pvCapacity >= 1.55*invertCapacity:
        print ('Inverter is undersized')
    else:
        powerOutputAC = powerOutputDC*inverterEff

    return powerOutputAC