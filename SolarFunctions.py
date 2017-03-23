# Solar Geometry and Resource

from HEMS_data import HEMSData
data = HEMSData()
import math


def CalculateDiffuseRatio_Erbs(clearnessIndex ):
    #diffuseRatio -- the ratio of diffuse radiation to global radiation

    if ( clearnessIndex < 0.0 ): #this should never happen
        diffuseRatio = 1.0
    elif ( clearnessIndex <= 0.22 ):
        diffuseRatio = 1.0 - 0.09 * clearnessIndex
    elif ( clearnessIndex <= 0.80 ):
        diffuseRatio = 0.9511 - 0.1604 * clearnessIndex + 4.388 * pow(clearnessIndex,2) \
                       - 16.638 * pow(clearnessIndex,3) + 12.336 * pow(clearnessIndex,4)
    else:
        diffuseRatio = 0.165

    return(diffuseRatio)


#Calculates solar time.
#@param localTime - local time or civil time [fractional] from 0 to 24.
#@param timezone - timezone of the location from GMT [hours].
#@param longitude - longitude of the location [decimal].
#@param dayOfYear - day of year [fractional] starting at 0 for Jan 1.
#@return solar time [fractional] from 0 to 24.

def CalculateSolarTime(localTime, timezone, longitude, dayOfYear ):

    solarTime = localTime + (longitude / 15.0) - timezone

    #calculate the equation of time
    solarLocale = (2 * math.pi) * (dayOfYear - 1.0) / 365.0 #radians
    solarTime = solarTime + (3.82 * (0.000075 + 0.001868 * math.cos(solarLocale) - 0.032077 * math.sin(solarLocale)
                        - 0.014615 * math.cos(2.0 * solarLocale) - 0.04089 * math.sin(2.0 * solarLocale)))

    #ensure the solar time is between zero and 24 hours
    while (solarTime < 0.0):
        solarTime = solarTime + 24.0
    while (solarTime > 24.0):
        solarTime = solarTime - 24.0

    return (solarTime)


#Calculates the hour angle. The hour angle equals zero at solar noon.
#@param solarTime - solar time [fractional] from 0 to 24.
#@return hour angle [radians].

def CalculateHourAngle(solarTime):
    hourAngle = ( math.pi / 180.0 ) * ( solarTime - 12.0 ) * 15.0
    return( hourAngle )


#Calculates the angle at which the sun sets.
#Eq. 1.6.1 from Duffie and Beckman, 2nd ed.
#@param latitude - location latitude [radians].
#@param solarDeclination - solar declination [radians].
#@return sunset hour angle [radians].


def CalculateSunsetHourAngle(latitude, solarDeclination ):


    cosOfSunsetHourAngle = -1.0 * math.tan(latitude) * math.tan(solarDeclination)

    #handle for special cases
    if (cosOfSunsetHourAngle >= 1.0):
        sunsetHourAngle = 0.0 #set to zero if sun doesn't come up (polar regions in winter)
    elif ( cosOfSunsetHourAngle <= -1.0 ):
        sunsetHourAngle = math.pi #sun is up all day (polar regions in summer)
    else:
        sunsetHourAngle = math.acos(cosOfSunsetHourAngle) #all regions

    return (sunsetHourAngle)


#Calculates the solar declination, the latitude at which the sun's rays are
#perpendicular to the earth's surface at solar noon. Eq. 1.6.1 from Duffie and Beckman, 2nd ed.
#@param dayOfYear - day of year [fractional] starting at 0 for Jan 1.
#@return solar declination [radians].

def CalculateSolarDeclination(dayOfYear):
    declination = 23.45 * math.sin( math.radians( 360.0 * ( 284.0 + dayOfYear ) / 365.0 ) )
    declination = math.radians(declination)
    return(declination)

# * Calculates the solar azimuth in degrees West of South. The equation is modified
# * from that listed on "en.wikipedia.org/wiki/Solar_azimuth_angle" because the
# * Eq. given on Wikipedia has a convention in degrees East of North instead of West of South.
# * @param latitude - latitude of the location [radians].
# * @param solarDeclination - solar declination [radians].
# * @param solarAltitude - solar altitude [radians].
# * @param hourAngle - hour angle [radians].
# * @return solar azimuth.

def CalculateSolarAzimuth(latitude, solarDeclination, solarAltitude, hourAngle):
    sinOfAzimuth = (math.sin(hourAngle) * math.cos(solarDeclination)) / math.cos(solarAltitude)

    # now find out the quadrant, and calculate the final value to be between -180 and +180
    if (sinOfAzimuth >= 1.0): #sun preparing to come up in the East
        solarAzimuth = math.pi / 2.0 #90 degrees
    elif ( sinOfAzimuth <= -1.0 ): #sun has set in the West
        solarAzimuth = -math.pi / 2.0 #-90 degrees
    else: #between - 180 and +180...but we need to find out which quadrant
        principalValueOfTheta = math.asin(sinOfAzimuth) #between - 90 and +90
        cosOfAzimuth = (math.cos(hourAngle) * math.cos(solarDeclination) * math.sin(latitude) - math.sin(solarDeclination)
                        * math.cos(latitude)) / math.cos(solarAltitude)

        if (cosOfAzimuth < 0.0): #between 90 and 270
            if ( sinOfAzimuth > 0.0): #between 0 and +180
                solarAzimuth = math.pi - principalValueOfTheta #180 -[0, 90]...between +90 and +180
            else:   #between -180 and 0
                solarAzimuth = -math.pi - principalValueOfTheta #-180 -[-90, 0]...between -180 and -90
        else:   #between -90 and 90
            solarAzimuth = principalValueOfTheta  #between -90 and +90

    return (solarAzimuth)

# * Calculates the solar altitude from the zenith angle.
# * @param zenithAngle - zenith angle [radians].
# * @return solar altitude [radians].

def CalculateSolarAltitude(zenithAngle):
    SolarAltitude = max(math.pi/2.0 - zenithAngle, 0.0)
    return(SolarAltitude)

# * Calculates the zenith angle, the angle of deviation between the normal of a
# * flat surface on the earth to the sun's beam component.
# * @param latitude - location latitude [radians].
# * @param solarDeclination - solar declination [radians].
# * @param hourAngle - hour angle [radians].
# * @return zenith angle [radians].

def CalculateZenithAngle(latitude,solarDeclination,hourAngle ):
    cosThetaZ = math.sin( solarDeclination ) * math.sin( latitude )\
                + math.cos( solarDeclination ) * math.cos( latitude ) * math.cos( hourAngle )
    ThetaZ = math.cos(cosThetaZ)
    return(ThetaZ)

# * Calculates incident angle, the angle of deviation between the normal of a
# * tilted surface to the sun's beam component.
# * @param latitude - location latitude [radians].
# * @param solarDeclination - solar declination [radians].
# * @param hourAngle - hour angle [radians].
# * @param slope - slope of incident surface [radians].
# * @param azimuth - azimuth of incident surface [radians].
# * @return incident angle [radians].

def CalculateIncidentAngle(latitude, solarDeclination, hourAngle, slope, azimuth ):
    cosTheta = math.sin(solarDeclination) * math.sin(latitude) * math.cos(slope) \
           - math.sin(solarDeclination) * math.cos(latitude) * math.sin(slope) * math.cos(azimuth) \
           + math.cos(solarDeclination) * math.cos(latitude) * math.cos(slope) * math.cos(hourAngle) \
           + math.cos(solarDeclination) * math.sin(latitude) * math.sin(slope) * math.cos(azimuth) * math.cos(hourAngle) \
           + math.cos(solarDeclination) * math.sin(slope) * math.sin(azimuth) * math.sin(hourAngle)
    cosTheta = math.acos(cosTheta)
    return (cosTheta)

# * Calculates the tilt ratio, a relationship between the incident angle of the
# * tilted surface and the zenith angle.
# * @param incidentAngle - angle of deviation of a sloped surface [radians].
# * @param zenithAngle - zenith angle [radians].
# * @return diffuse ratio.

def CalculateTiltRatio(incidentAngle,zenithAngle ):
    Rb = math.cos(incidentAngle) / math.cos(zenithAngle)
    if (Rb < 0.0):
        Rb = 0.0 # nonegativevalues
    elif (Rb > 5.0):
        Rb = 5.0 #no unrealistic high values
    return (Rb)


#return W/m2
def CalculateExtraterrestrialNormalRadiation(DayOfYear):
    ExtraterrestrialNormalRadiation =  1.367 * ( 1.0 + 0.033 * math.cos(math.radians(360.0*DayOfYear/365.0)))*1000.0
    return(ExtraterrestrialNormalRadiation)


def CalculateExtraterrestrialHorizontalRadiationOverTimestep(latitude,dayOfYear,solarTime,sunsetHourAngle,solarDeclination,timestepHourlyFraction ):
    G_ext_n = CalculateExtraterrestrialNormalRadiation(dayOfYear)
    hourAngle1 = CalculateHourAngle(solarTime - timestepHourlyFraction / 2.0)
    hourAngle2 = CalculateHourAngle(solarTime + timestepHourlyFraction / 2.0)

    #don't compute before sunrise or after sunset
    if (sunsetHourAngle != math.pi / 2.0):
        if (hourAngle1 < 0.0):
            hourAngle1 = max(hourAngle1, -sunsetHourAngle)
        else:
            hourAngle1 = min(hourAngle1, sunsetHourAngle)
        if (hourAngle2 < 0.0):
            hourAngle2 = max(hourAngle2, -sunsetHourAngle)
        else:
            hourAngle2 = min(hourAngle2, sunsetHourAngle)

    #units of kW / m2 using timestepHourlyFraction,
    G_ext_h = ( 12.0 / math.pi ) * G_ext_n * ( math.cos( latitude ) * math.cos( solarDeclination )
                                          * ( math.sin( hourAngle2 ) - math.sin( hourAngle1 ) )
                                          + ( hourAngle2 - hourAngle1 ) * math.sin( latitude )
                                          * math.sin( solarDeclination ) ) / timestepHourlyFraction
    G_ext_h = max(G_ext_h, 0.0)
    return (G_ext_h)

def CalculateClearnessIndex(GHI, ExtraterrestrialNormalRadiation):
    kT = GHI/ExtraterrestrialNormalRadiation
    return (kT)
