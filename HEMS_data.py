class HEMSData():
    def __init__(self, *args, **kwargs):
        self.input = HEMSDataInput()
        self.output = HEMSDataOutput()

class HEMSDataInput():
    def __init__(self, *args, **kwargs):

        #Environmental Data
        self.AmbientTemp = []  # Ambient Temperature in [K]
        self.GlobalHorizontalRadiation = []      # Global Horizontal Radiation [W/m2]
        self.DNI = []   #Direct Normal Irradiance [W/m2]
        self.DFI = []   #Diffuse Horizontal Irradiance [W/m2]
        self.LocalTime = []   # Hour of the day 1 through 24
        self.DayOfYear = []  # Day of the year
        self.ClearnessIndex = []  # Clearness Index
        self.TimeStepHourlyFraction = 1
        self.GroundReflectance = 0 # Ground Reflectance

        # Site Specific Data
        self.Elevation = 331  # Building elevation in [m]
        self.Latitude = 33  # Latitude of the building location
        self.Longitude = -112  # Longitude of the building location
        self.TimeZone = -7  # Time zone away from GMT (negative for west poistive for east)
        self.EnergySystemType = 'solarPV & & inverter && battery'   #Type of energy system to be controlled possible loads,
        # solarPV && inverter, solarPV && inverter && battery
        self.StartTOU = 12  #Hour of day that TOU starts
        self.StopTOU = 20   #Hour of day that TOU stops


        #Energy Asset

        #Solar PV
        self.PVcapacity = 5 #kW size of PV array
        self.PVArea = 100 #m2 Area of PV array
        self.PVperformance = 0.9 #Performance or efficiency of PV array
        self.PVOrientation = 180 #PV array Azimuth angle (South Ref = 180)
        self.PVSlope = 33 #PV array Tilt andle (Perpendicular to ground = 0)

        #Inverter
        self.Inverterefficeincy = 0.9 #DC to AC conversion efficeincy
        self.Invertercapacity = 5 #kW size of Inverter

        #Grid
        self.GridEnergyCost = [] #$/kWh energy price for current hour
        #self.GridDemandCharge = 9 #$/kW demand charge for month
        self.GridNetMeter = 0.3 #$/kWh price paid for sending energy to grid

        #Battery
        self.BatteryPower = 5 #kW power has positive convention as output -- power output (+) or power to charge (-)
        self.BatteryChargeEff = 0.9 #Charging Efficeicny (Must take into account efficiecny of AC/DC and charge controller)
        self.BatteryDischargeEff = 0.85 #Discharging Efficeicny (Must take into account efficiecny of AC/DC and charge controller)
        self.BatteryRTEff = 0.8 #Round Trip Efficeincy
        self.BatteryNominalCapacity = 150 #AmpHours of Battery Bank
        self.BatteryCurrentCapacity = 150 #AmpHours Assume Battery Bank is fully charge at beginging of simulation
        self.BatteryVoltageNominal = 48    #Volts Nominal Voltage of battery
        self.BatteryVoltageCharge = 50  # Volts Average voltage when charging the battery
        self.BatteryVoltageDischarge = 48 #Volts Average voltage when discharging the battery
        self.BatteryMinCapacityAsFraction = 0.2 #Minimume State of Charge Allowed in Battery
        self.BatteryMaxCRate = 5 #C Maximume charge or discharge rate

        #Load
        self.LoadUncontrollablePower = [] #kW Power requested by loads that are uncontrollable
        self.LoadControllablePower = []  #kW Power requested by loads that are controllable
        self.LoadCurtailPercent = 0    #Percent of load to be curtailed and met at a later time step


class HEMSDataOutput():
    def __init__(self, *args, **kwargs):

        #SolarPV
        self.PVPowerOut = 0; #kW

        #Inverter
        self.IPowerIn = 0; #kW
        self.IPowerOut = 0; #kW

        #Grid
        self.GridPowerNet = 0; #Net energy comsumed or produced by building (- produce + consume)
        self.GridPower = 0; #kW Power used from grid
        self.GridEnergy = 0; #kWh Energy used from grid

        #Battery
        self.BatteryCapacityAsEnergy = 0;
        self.BatterySOC = 0; #Present SOC of battery
        self.BatteryPower = 0;  #kW (Power used to charge or discharged from battery)
        self.BatteryPowerAllowable = 0; #Allowable power to be used for charging


        #Load
        self.LoadControllablePowerActual = 0;  # kW Power used by loads that are controllable
        self.LoadPercentCurtail = 0  # Percent of controllable load that is curtailed


