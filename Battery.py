# battery Energy Asset
# Hi!

from HEMS_data import HEMSData
data = HEMSData()
import math

def BatteryParameter(nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate):
    maxCapacityAsEnergy = (nominalCapacity * nominalVoltage)/1000
    minCapacityAsEnergy = maxCapacityAsEnergy * minCapacityAsFractoin
    chargeEfficiency = chargeEff
    dischargeEfficiency = dischargeEff
    maxRatedChargePower = maxCapacityAsEnergy * maxCRate
    maxRatedDischargePower = maxCapacityAsEnergy * maxCRate

    return maxCapacityAsEnergy, minCapacityAsEnergy, chargeEfficiency, dischargeEfficiency, maxRatedChargePower, maxRatedDischargePower


def BatteryGetMaximumChargePower(currentCapacity, timestepHourlyFraction, nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate):

    (maxCapacityAsEnergy, minCapacityAsEnergy, chargeEfficiency, dischargeEfficiency, maxRatedChargePower, maxRatedDischargePower) = BatteryParameter(nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate)

    #check if max power is bound by available room in battery
    currentCapacityAsEnergy = (currentCapacity * nominalVoltage)/1000
    maxChargeEnergy = maxCapacityAsEnergy - currentCapacityAsEnergy

    maxChargePower = maxChargeEnergy * ( 1.0 / timestepHourlyFraction )  #account for timestep size in converting to power
    maxChargePower = maxChargePower/(chargeEfficiency) #account for charge efficiency

    #check if power is bound by CRate limit
    if maxChargePower < maxRatedChargePower:
        maxChargePower = maxChargePower
    else:
        maxChargePower = maxRatedChargePower


    return(maxChargePower, maxChargeEnergy)

def BatteryGetMaximumDischargePower(currentCapacity, timestepHourlyFraction, nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate):

    (maxCapacityAsEnergy, minCapacityAsEnergy, chargeEfficiency, dischargeEfficiency, maxRatedChargePower, maxRatedDischargePower) = BatteryParameter(nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate)

    #check if max power is bound by available room in battery
    currentCapacityAsEnergy = (currentCapacity * nominalVoltage)/1000
    maxDischargeEnergy = currentCapacityAsEnergy - minCapacityAsEnergy

    maxDischargePower = maxDischargeEnergy * ( 1.0 / timestepHourlyFraction )  #account for timestep size in converting to power
    maxDischargePower = maxDischargePower * dischargeEfficiency #account for charge efficiency

    #check if power is bound by CRate limit
    if maxDischargePower < maxRatedChargePower:
        maxDischargePower = maxDischargePower
    else:
        maxDischargePower = maxRatedDischargePower

    return(maxDischargePower, maxDischargeEnergy)

def BatteryPower(power,currentCapacity, timestepHourlyFraction, nominalCapacity, nominalVoltage,minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate):
    #power has positive convention as output power
    #Calculating current capacity as energy, battery parameters, and charging/discharging constraints
    currentCapacityAsEnergy = (currentCapacity * nominalVoltage)/1000
    maxCapacityAsEnergy, minCapacityAsEnergy, chargeEfficiency, dischargeEfficiency, maxRatedChargePower, maxRatedDischargePower = BatteryParameter(nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate)
    maxChargePower, maxChargeEnergy = BatteryGetMaximumChargePower(currentCapacity, timestepHourlyFraction, nominalCapacity, nominalVoltage,minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate)
    maxDischargePower, maxDischargeEnerg = BatteryGetMaximumDischargePower(currentCapacity, timestepHourlyFraction, nominalCapacity, nominalVoltage, minCapacityAsFractoin, chargeEff, dischargeEff, maxCRate)

    #double-check to see if power is too high
    if( power > 0 ):  #discharging
        if maxDischargePower < power:
            dischargePower = power
        else:
            dischargePower =  maxDischargePower

        outputPower = dischargePower
        capacityAsEnergy = currentCapacityAsEnergy - dischargePower / dischargeEfficiency
    elif( power < 0 ):  #charging
        if maxChargePower < (-1.0 * power):
            chargePower = -1.0 * power
        else:
            chargePower = maxChargePower

        outputPower = -1.0 * chargePower
        capacityAsEnergy = currentCapacityAsEnergy + chargePower * chargeEfficiency

    else:  #no load applied
        chargePower = 0
        dischargePower = 0
        outputPower = 0
        capacityAsEnergy = currentCapacityAsEnergy


    capacityAsFraction = capacityAsEnergy / maxCapacityAsEnergy

    return outputPower, capacityAsEnergy, capacityAsFraction,

def BatteryCapacity(batteryPower, currentCapacity, batteryNominalVoltage, batteryNominalCapacity, chargeEff, dischargeEff,):   # Calculate battery capacity
    currentCapacityAsEnergy = (currentCapacity * batteryNominalVoltage)/1000

    if (batteryPower > 0):  # discharging
        capacityAsEnergy = currentCapacityAsEnergy - batteryPower/dischargeEff
        capacityAsAmpHour = currentCapacity - (batteryPower/batteryNominalVoltage)*1000/dischargeEff
    elif (batteryPower < 0):  # charging
        batteryPower = -1.0 * batteryPower
        capacityAsEnergy = currentCapacityAsEnergy + batteryPower*chargeEff
        capacityAsAmpHour = currentCapacity + (batteryPower / batteryNominalVoltage)*1000*chargeEff
    else:  # no load applied
        capacityAsEnergy = currentCapacityAsEnergy
        capacityAsAmpHour = currentCapacity

    maxCapacityAsEnergy = (batteryNominalCapacity * batteryNominalVoltage)/1000
    capacityAsFraction = capacityAsEnergy / maxCapacityAsEnergy

    return capacityAsEnergy, capacityAsFraction, capacityAsAmpHour
