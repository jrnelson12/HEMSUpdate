# Solar PV Energy Asset

from HEMS_data import HEMSData
data = HEMSData()
import math
import SolarFunctions

#Solar Gemometry


def SolarPV(dayOfYear, localTime, timeZone, longitude, latitude, slope, globalHorizontalRadiation, clearnessIndex, DNI,
            timeStepHourlyFraction, DFI, groundReflectance, capacity):
    #assume fixed tilt for now
    declination = SolarFunctions.CalculateSolarDeclination(dayOfYear)
    solarTime = SolarFunctions.CalculateSolarTime(localTime, timeZone, longitude, dayOfYear)
    hourAngle = SolarFunctions.CalculateHourAngle(solarTime)
    zenith = SolarFunctions.CalculateZenithAngle(latitude,declination,hourAngle)
    altitude = SolarFunctions.CalculateSolarAltitude(zenith)
    azimuth = SolarFunctions.CalculateSolarAzimuth(latitude,declination,altitude,hourAngle)
    sunsetHourAngle = SolarFunctions.CalculateSunsetHourAngle(latitude, declination)
    #calculate incident angle
    if (altitude > 0 ): #sun is up
        incidentAngle = SolarFunctions.CalculateIncidentAngle(latitude, declination, hourAngle, slope, azimuth)
    else:   #sun is down
        incidentAngle= 90.0

    #calculate incident radiation
    if (globalHorizontalRadiation > 0 ): #sun is shining
        tiltRatio = SolarFunctions.CalculateTiltRatio(incidentAngle,zenith)
        panelSlope = math.radians(slope)

        #beam component
        beamComponent = DNI*tiltRatio
        #sometimes tilt ratio can be high and cause the above to skew results, so modify beam if that is the case
        extraterrestrialNormalRadiation = SolarFunctions.CalculateExtraterrestrialNormalRadiation(dayOfYear)
        clearnessIndex = SolarFunctions.CalculateClearnessIndex(globalHorizontalRadiation, extraterrestrialNormalRadiation)
        if ( beamComponent > ( clearnessIndex * extraterrestrialNormalRadiation ) ):
            beamComponent = ( clearnessIndex * extraterrestrialNormalRadiation )

        #diffuse component
        exteraterrestrialHorizontalRadiation = SolarFunctions.CalculateExtraterrestrialHorizontalRadiationOverTimestep(latitude,
                                                        dayOfYear,solarTime,sunsetHourAngle,declination,timeStepHourlyFraction)
        if ( exteraterrestrialHorizontalRadiation > 0 ):
            anisotropyIndex = DNI / exteraterrestrialHorizontalRadiation
        else:
            anisotropyIndex = .5 #a reasonable number just so that the computation runs

        horizontalBrighteningFactor = math.sqrt( DNI / globalHorizontalRadiation )

        diffuseComponent = DFI * anisotropyIndex * tiltRatio + DFI * (1.0 - anisotropyIndex)\
                                                           * ( ( 1.0 + math.cos( slope ) ) / 2.0 ) * ( 1.0 +
                                                            horizontalBrighteningFactor * math.pow( math.sin( slope / 2.0 ), 3.0 ) )

        #reflective component
        reflectiveComponent = globalHorizontalRadiation* groundReflectance * ( ( 1.0 - math.cos( slope ) ) / 2.0 )

        incidentRadiation = beamComponent + diffuseComponent + reflectiveComponent

    else: #sun is not shining
        incidentRadiation = 0.0

    #TODO -- add temperature effects

    #calculate array power output
    powerOutputDC = incidentRadiation * capacity / 1000.0 #divide by 1000 because incident radiation in W / m2 and capacity in kW
    return powerOutputDC


#Summary Data

#def SummaryStatisticsPowerSummary(poweroutputDC):
#    if poweroutputDC > 0:
#        totalCapacity = this->m_capacity;
#        totalProduction = powerSummary.total * m_timestepHourlyFraction;
#        meanPowerOutput = powerSummary.mean;
#        meanDailyEnergy = m_meanPowerOutput * 24.0;
#       maxPowerOutput = powerSummary.max;
#        minPowerOutput = powerSummary.min;
#        operatingTime = powerSummary.operatingTime;
#        capacityFactor = m_meanPowerOutput / m_capacity * 100.0;
#    else:
#        totalCapacity = 0
#        totalProduction = 0
#        meanPowerOutput = 0
#        meanDailyEnergy = 0
#        maxPowerOutput = 0
#        minPowerOutput = 0
#        operatingTime = 0
#        capacityFactor = 0
