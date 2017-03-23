# hour = Outback_Hour
# pvPower = CC_Array_Current * CC_Array_Voltage
# inverterPowerOutSS = I_AC_Power
# inverterPowerOutOB = GS_Single_AC_Output_Voltage * (GS_Single_Inverter_Charge_Current + GS_Single_Inverter_Output_Current
#                                                     + GS_Single_Inverter_Sell_Current)
# loadPowerOB = GS_Single_AC_Output_Voltage * GS_Single_Inverter_Output_Current
# # here is the dispatch logic...
# # - no solar, use grid to meet load
# # - charge battery with solar
# # - send excess to meet load
# # - discharge battery during TOU period battery to avoid high grid price...assume 12-8PM
#
# if (hour < startTOU or hour > stopTOU):  # outside TOU, don't use battery
#     batteryVoltage_OB = CC_Batt_Voltage
#
#     if (batteryVoltage_OB <= batteryRebulkVoltage_OB):  # battery is at or less than the voltage to re-initiate bulk charging
#         if pvPower <= 0:  # no solar just use grid to meet load
#             batteryPower = 0
#             powerOutputDC = 0
#             powerOutputAC = 0
#             PVPower = 0
#             totalLoadPower = Load.Load(controllableLoadPower, curtail, uncontrollableLoadPower)
#             EnergyNet = totalLoadPower
#         elif (PVPower > batteryPower):  # more solar than can put into battery
#             batteryPower = (-1.0 * batteryPower)  # switch sign so we know it is charging
#             powerOutputDC = powerOutputDC - batteryPower  # send remaining to load
#             powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity, invertCapacity)
#             totalLoadPower = Load.Load(controllableLoadPower, curtail, uncontrollableLoadPower)
#             EnergyNet = totalLoadPower - powerOutputAC
#         else:  # battery requires all solar power, no solar pushed to loads
#             batteryPower = (-1.0 * powerOutputDC)
#             powerOutputDC = 0  # send remaining to load
#             powerOutputAC = 0
#             totalLoadPower = Load.Load(controllableLoadPower, curtail, uncontrollableLoadPower)
#             EnergyNet = totalLoadPower
#     else:  # no room to charge battery, just push solar to AC
#         batteryPower = 0  # still need to do, else numbers don't update
#         powerOutputDC = SolarPV.SolarPV(dayOfYear, localTime, timeZone, longitude, latitude, slope,
#                                         globalHorizontalRadiation,
#                                         clearnessIndex, DNI, timeStepHourlyFraction, DFI, groundReflectance, pvCapacity)
#         PVPower = powerOutputDC
#         powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity, invertCapacity)
#         totalLoadPower = Load.Load(controllableLoadPower, curtail, uncontrollableLoadPower)
#         EnergyNet = totalLoadPower - powerOutputAC
#
# else:  # inside TOU, use battery if possible
#     powerOutputDC = SolarPV.SolarPV(dayOfYear, localTime, timeZone, longitude, latitude, slope,
#                                     globalHorizontalRadiation,
#                                     clearnessIndex, DNI, timeStepHourlyFraction, DFI, groundReflectance, pvCapacity)
#     PVPower = powerOutputDC
#     powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity, invertCapacity)
#     totalLoadPower = Load.Load(controllableLoadPower, curtail, uncontrollableLoadPower)
#     EnergyNet = totalLoadPower - powerOutputAC  # send remaining to grid
#     batteryPower, maxChargeEnergy = Battery.BatteryGetMaximumChargePower(currentCapacity, timeStepHourlyFraction,
#                                                                          nominalCapacity, nominalVoltage,
#                                                                          minCapacityAsFractoin,
#                                                                          chargeEff, dischargeEff, maxCRate)
#     if (EnergyNet < 0):  # use excess power to charge battery
#         excessDC = -1 * (EnergyNet / inverterEff)  # change back to DC and sign from negative to positive
#         if batteryPower > 0:
#             if excessDC > batteryPower:  # more solar than can put into battery
#                 batteryPower = (-1.0 * batteryPower)  # switch sign so we know it is charging
#                 powerOutputDC = excessDC - batteryPower  # send remaining to grid
#                 powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity, invertCapacity)
#                 EnergyNet = -1 * (powerOutputAC)  # send remaining to grid
#
#             else:  # battery requires all solar power, no excess solar pushed to grid
#                 batteryPower = (-1.0 * excessDC)  # switch sign so we know it is charging
#                 powerOutputDC = excessDC
#                 powerOutputAC = 0
#                 EnergyNet = 0
#         else:  # no room to charge battery, just push solar to AC
#             batteryPower = 0  # still need to do, else numbers don't update
#             powerOutputDC = excessDC
#             powerOutputAC = Inverter.Inverter(excessDC, inverterEff, pvCapacity, invertCapacity)
#             EnergyNet = -1 * (powerOutputAC)  # send remaining to grid
#     else:  # try use battery to meet load
#         deficitAC = totalLoadPower - powerOutputAC  # how much AC load battery has to supply
#         deficitDC = deficitAC / inverterEff  # account for DC to AC efficiency
#         batteryPower, maxDischargeEnerg = Battery.BatteryGetMaximumDischargePower(currentCapacity,
#                                                                                   timeStepHourlyFraction,
#                                                                                   nominalCapacity, nominalVoltage,
#                                                                                   minCapacityAsFractoin,
#                                                                                   chargeEff, dischargeEff, maxCRate)
#         if (batteryPower > 0):
#             if (deficitDC > batteryPower):  # need more power than battery can deliver
#                 batteryPower = (batteryPower)  # positive sign means discharging
#                 powerOutputDC = powerOutputDC + batteryPower  # account for extra battery power going into inverter
#                 powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity,
#                                                   invertCapacity)  # solar output + battery output
#                 EnergyNet = totalLoadPower - powerOutputAC
#
#             else:  # battery can meet deficit DC that solar PV cannot
#                 batteryPower = (deficitDC)
#                 powerOutputDC = powerOutputDC + batteryPower  # account for extra battery power going into inverter
#                 powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity,
#                                                   invertCapacity)  # solar output + battery output
#                 EnergyNet = totalLoadPower - powerOutputAC
#
#
#         else:  # no energy in battery to use
#             batteryPower = 0  # still need to do, else numbers don't update
#             powerOutputDC = powerOutputDC + batteryPower  # account for extra battery power going into inverter
#             powerOutputAC = Inverter.Inverter(powerOutputDC, inverterEff, pvCapacity,
#                                               invertCapacity)  # solar output + battery output
#             EnergyNet = totalLoadPower - powerOutputAC
#
# batteryCurrentCapacity, batterySOC, capacityAsAmpHour = Battery.BatteryCapacity(batteryPower, currentCapacity,
#                                                                                 nominalVoltage, nominalCapacity,
#                                                                                 chargeEff, dischargeEff)
#
# return powerOutputDC, powerOutputAC, batteryPower, EnergyNet, batteryCurrentCapacity, batterySOC, capacityAsAmpHour, PVPower