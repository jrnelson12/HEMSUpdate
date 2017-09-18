from HEMS_data import HEMSData
data = HEMSData()
import math
import Dispatch
import Dispatch_Load
import Input_data
class HEMS():
    def __init__(self, *args, **kwargs):
        self.data = HEMSData()
def main():
    #Read in data day, hour, dfi, dni, ghi, ambtemp, KT, gridPrice, controllableLoad, uncontrollableLoad
    data.input.DayOfYear, data.input.LocalTime, data.input.DFI, data.input.DNI, data.input.GlobalHorizontalRadiation, data.input.AmbientTemp, \
    data.input.ClearnessIndex, data.input.GridEnergyCost, data.input.LoadControllablePower, data.input.LoadUncontrollablePower\
        = Input_data.inputs_data(data.input.DayOfYear, data.input.LocalTime, data.input.DFI, data.input.DNI, data.input.GlobalHorizontalRadiation, data.input.AmbientTemp,
                                 data.input.ClearnessIndex, data.input.GridEnergyCost, data.input.LoadControllablePower, data.input.LoadUncontrollablePower)
    print(data.input.DNI)
    #Lists to store outputs
    PVPowerOut =[]
    IPowerOut =[]
    IPowerIn = []
    BatteryPower =[]
    GridPowerNet =[]
    BatteryCurrentCapacity =[]
    BatterySOC =[]
    LoadBank = []
    Curtail = []

    #List to store inputs
    Day = []
    Hour = []
    DNI = []
    Load = []
    for hour in range(len(data.input.LocalTime)):
        #Simulate dispatch
        data.input.loadBank = float(data.input.loadBank)
        data.output.IPowerIn, data.output.IPowerOut, data.output.BatteryPower, data.output.GridPowerNet,\
        data.output.BatteryCapacityAsEnergy, data.output.BatterySOC, data.input.BatteryCurrentCapacity, data.output.PVPowerOut, data.input.loadBank, data.output.curtail = Dispatch_Load.Dispatch(data.input.EnergySystemType,
                                data.input.LoadControllablePower[hour], data.input.MaxCurtail,
                                data.input.LoadUncontrollablePower[hour], data.input.loadBank, data.input.DayOfYear[hour], data.input.LocalTime[hour],
                                data.input.TimeZone, data.input.Longitude, data.input.Latitude, data.input.PVSlope,
                                data.input.GlobalHorizontalRadiation[hour], data.input.ClearnessIndex[hour], data.input.DNI[hour],
                                data.input.TimeStepHourlyFraction, data.input.DFI[hour], data.input.GroundReflectance,
                                data.input.Inverterefficeincy, data.input.PVcapacity, data.input.Invertercapacity,
                                data.input.StartTOU, data.input.StopTOU, data.input.BatteryCurrentCapacity,
                                data.input.BatteryNominalCapacity, data.input.BatteryMinCapacityAsFraction,
                                data.input.BatteryChargeEff, data.input.BatteryDischargeEff, data.input.BatteryMaxCRate, data.input.BatteryVoltageNominal)


        print (data.input.DNI[hour], data.output.PVPowerOut, data.output.IPowerOut, data.output.BatteryPower, data.output.GridPowerNet,
                   data.output.BatteryCapacityAsEnergy, data.output.BatterySOC, data.input.BatteryCurrentCapacity, data.input.loadBank)

        # Changing from float to string
        #Outputs
        data.output.IPowerIn = str(data.output.IPowerIn)
        data.output.IPowerOut = str(data.output.IPowerOut)
        data.output.BatteryPower = str(data.output.BatteryPower)
        data.output.GridPowerNet = str(data.output.GridPowerNet)
        data.output.BatteryCapacityAsEnergy = str(data.output.BatteryCapacityAsEnergy)
        data.output.BatterySOC = str(data.output.BatterySOC)
        data.output.PVPowerOut = str(data.output.PVPowerOut)
        data.output.curtail = str(data.output.curtail)

        #Inputs
        data.input.DayOfYear[hour] = str(data.input.DayOfYear[hour])
        data.input.LocalTime[hour] = str(data.input.LocalTime[hour])
        data.input.DNI[hour] = str(data.input.DNI[hour])
        data.input.LoadUncontrollablePower[hour] = str(data.input.LoadUncontrollablePower[hour])
        data.input.loadBank = str(data.input.loadBank)

        # Recording each timestep in list
        Day.append(data.input.DayOfYear[hour])
        Hour.append(data.input.LocalTime[hour])
        DNI.append(data.input.DNI[hour])
        Load.append(data.input.LoadUncontrollablePower[hour])
        LoadBank.append(data.input.loadBank)
        PVPowerOut.append(data.output.PVPowerOut)
        IPowerIn.append(data.output.IPowerIn)
        IPowerOut.append(data.output.IPowerOut)
        BatteryPower.append(data.output.BatteryPower)
        GridPowerNet.append(data.output.GridPowerNet)
        BatteryCurrentCapacity.append(data.output.BatteryCapacityAsEnergy)
        BatterySOC.append(data.output.BatterySOC)
        Curtail.append(data.output.curtail)

    # Writing to csv file
    f = open('HEMSOutputLoadSolarBatteryTest.csv', 'w')
    for z in range(len(data.input.LocalTime)):
        f.write(Day[z] + ',')
        f.write(Hour[z] + ',')
        f.write(DNI[z] + ',')
        f.write(Load[z] + ',')
        f.write(LoadBank[z] + ',')
        f.write(PVPowerOut[z] + ',')
        f.write(IPowerIn[z] + ',')
        f.write(IPowerOut[z] + ',')
        f.write(BatteryPower[z] + ',')
        f.write(GridPowerNet[z] + ',')
        f.write(BatteryCurrentCapacity[z] + ',')
        f.write(BatterySOC[z] + ',')
        f.write(Curtail[z])
        f.write('\n')
    f.close()
if __name__ == '__main__':
    main()