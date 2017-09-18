#TODO: Find registers to set installer information/ settings and user access rights
set_outback_time()

OutBack_Year        #Clock year (4 digit)
Outback_Month       #Clock Month (1 - 12)
OutBack_Day         #Clock Day (1 - 31)
OutBack_Hour        #Clock Hour (0 - 23)
Outback_Minute      #Clock Minute (0 - 59)
OutBack_Second      #Clock Second (0 - 59)

set_system_setpoints()

OB_Bulk_Charge_Enable_Disable = 0   #0=Not used 1=Start Bulk, 2=Stop Bulk, 3=Start EQ Charge, 4= Stop EQ Charge
OB_Inverter_AC_Drop_Use = 0         # 0=Not used 1=Use, 2=Drop
OB_Set_Inverter_Mode = 2            #1=Off, 2=Search, 3=On
OB_Grid_Tie_Mode  = 1              #1=Enable, 2=Disable
OB_Set_Inverter_Charger_Mode  = 2   #Auto set to 2 when grid tie mode is enabled  #1=Off, 2=Auto, 3=On
#TODO: look into registers to specify PV array wattage, Generator kW rating and type, Maximume inverter kW rating,

set_battery_setpoints():

FNconfig_Battery_Capacity = 120     #AH- set this value to the capacity of the battery bank
FNconfig_Charged_Volts    = 55.2    #V -dependent on the specifc battery bank used
FNconfig_Battery_Charged_Amps = 0.02*FNconfig_Battery_Capacity   #AUTOSET THIS REGISTER WHEN BATTERY CAP IS SET. Can vary between 1.5% and 2% of battery capacity depending on life and condition of bank
FNconfig_Charged_Time = 1       #minutes- time voltage and amps must be met to consider batteries charged
#TODO: Find register to set nominal voltage of battery bank
#If needed outback has the implimentation of scaling factors to adjust these nominal values

set_inverter_setpoints():

#AC Input
GSconfig_AC_Input_Select_Priority = 0   #0=Grid, 1=Gen
GSconfig_AC_Coupled = 0                     #0=No, 1=Yes (not implemented)

#Grid Input
GSconfig_Grid_Input_Mode = 2                #Grid Input Mode: 0=Generator, 1=Support, 2=Grid Tied, 3=UPS, 4=Backup, 5=Mini Grid, 6=Grid Zero
GSconfig_Grid_Tie_Enable = 1        #1=Yes, 0=No

#Generator Input
GSconfig_Gen_Input_Mode = 0             #Grid Input Mode: 0=Generator, 1=Support, 2=Grid Tied, 3=UPS, 4=Backup, 5=Mini Grid, 6=Grid Zero

#Battery/ Charging
GSconfig_Charger_Operating_Mode = 0         #0=All Inverter Charging Disabled, 1=Bulk and Float Charging Enabled
GSconfig_Sell_Volts = 48                        #V - Sell Voltage Target
GSconfig_ReBulk_Volts = 54.4                    #V- ReBulk Voltage Target

#AUX
#TODO

set_chargecontroller_setpoints():
#Charging set points (also set in inverter setpoints)
#Since the inverter sells power to maintain its own Float, Absorption, or Sell settings (all of which should be lower than those of the controller), this mode makes it easier for the inverter to sell power.
CCconfig_Absorb_Volts           #Absorb Voltage Target
CCconfig_Absorb_Time_Hours      #Absorb Time Hours
CCconfig_Absorb_End_Amps        #Amperage to end Absorbing
CCconfig_Rebulk_Volts           #Voltage to re-initiate Bulk charge
CCconfig_Float_Volts            #Float Voltage Target
CCconfig_Bulk_Current           #Max Output Current Limit

#MPPT
CCconfig_MPPT_Mode = 0          #0 = Auto; 1 = U-Pick

#TODO: Need the active registers (Registers in AllOutput.txt) to find rest of set points
CCconfig_Grid_Tie_Mode = 1      #0 = Grid Tie Mode disabled; 1 = Grid Tie Mode enabled
#TODO: Auxillary Output of CC

set_batterymonitor_setpoints():
#when parameters are met the SOC will be consider 100%
FNconfig_Battery_Capacity = 100         #Ah- Battery AH capacity
FNconfig_Charged_Volts = 55.2           #V-  Sets the minimum voltage the three-stage charger must reach during the Bulk or Absorption stages for the battery monitor to consider the batteries fully charged.
FNconfig_Charged_Time = 3               #min -Sets the duration the Charged Voltage and Charged Return Amps must be maintained before the charging cycle is considered finished.
FNconfig_Battery_Charged_Amps = 2.0     #A- Sets the limit to which the charging current must “trickle down” or decrease before the batteries are considered charged.

#TODO: Relay Mode to switch or turn other devices on or off

set_mate3_settings():
#TODO: Advacned gnerator start (AGS) Setup
#TODO: Data logging functionality (possible recording onto external memory device)
#TODO: Possible set up of HBX mode if trying to minimize grid usage
#Grid Use Time
#Will not work with HBX or Mini Grid modes, If the battery voltage falls below the inverter’s Low Battery Cut-Out voltage, the inverter will automatically connect to the AC input source regardless of the time-of-day setting)
#Only one Grid Use Time may be programmed on a weekend.  Three Grid Use Time periods may be programmed on weekdays.
#Min = 0-59, Hour = 0-23

#ONLY ALLOW USER ACCESS IF GRID TIED IS ENABLED
OutBack_Grid_Use_Interval_1_Mode = 1        #0=Disabled, 1=Enabled
OutBack_Grid_Use_Interval_1_Weekday_Start_Hour = 0
OutBack_Grid_Use_Interval_1_Weekday_Start_Minute = 0
OutBack_Grid_Use_Interval_1_Weekday_Stop_Hour = 13
OutBack_Grid_Use_Interval_1_Weekday_Stop_Minute = 0
OutBack_Grid_Use_Interval_1_Weekend_Start_Hour = 0
OutBack_Grid_Use_Interval_1_Weekend_Start_Minute = 0
OutBack_Grid_Use_Interval_1_Weekend_Stop_Hour = 0
OutBack_Grid_Use_Interval_1_Weekend_Stop_Minute = 0


#BE ABLE TO DISPLAY THIS DATA ON MAIN PAGE
record_sunspec_data():
#Sunspec registers for inverter
#DC (In)
I_DC_Power
#AC(Out)
I_AC_Power
I_AC_VAR
I_AC_VA
I_AC_Energy_WH

record_system_data():
#System
OutBack_Error
OutBack_Status
OutBack_System_Voltage              #12, 24, 26, 48 or 60 VDC
OutBack_Measured_System_Voltage     #Current system battery voltage computed by gateway

record_battery_data():
#Battery/ Charge Controller
CC_Watts
CC_Todays_Min_Battery_Volts
CC_Todays_Max_Battery_Volts
CC_Todays_kWH
CC_Todays_AH
CC_Lifetime_kWH_Hours
CC_Lifetime_kAmp_Hours
CC_Lifetime_Max_Watts
CC_Lifetime_Max_Battery_Volts
CC_Lifetime_Max_VOC

#FlexNet Battery Monitor
#MIGHT NOT BE ABLE TO ACCESS BELOW REGISTERS BECASUE THEY ARE USED IN LOCAL DATA LOGGING. MAY NEED TO USE REGISTER BELOW
FNconfig_Datalog_Minimum_SOC
FNconfig_Datalog_Input_AH
FNconfig_Datalog_Input_kWh
FNconfig_Datalog_Output_AH
FNconfig_Datalog_Output_kWh
FNconfig_Datalog_NET_AH
FNconfig_Datalog_NET_kWh


FN_Input_kW
FN_Output_kW
FN_Net_kW
FN_Days_Since_Charge_Parameters_Met
FN_State_Of_Charge

#THESE WOULD NOT BE TIME SERIES BUT INSTEAD MAYBE A TABLE WITH THE DAY AND THEN VALUE
FN_Todays_Minimum_SOC
FN_Todays_Maximum_SOC
FN_Todays_NET_Input_AH
FN_Todays_NET_Input_kWh
FN_Todays_NET_Output_AH
FN_Todays_NET_Output_kWh
FN_Todays_NET_Battery_AH
FN_Todays_NET_Battery_kWh
FN_Todays_Minimum_Battery_Voltage
FN_Todays_Minimum_Battery_Time
FN_Todays_Maximum_Battery_Voltage
FN_Todays_Maximum_Battery_Time
FN_Cycle_kWh_Charge_Efficiency
FN_Total_Days_At_100_Percent
FN_Lifetime_kAH_Removed


record_inverter_data():
#Inverter
GSconfig_Stacking_Mode
GS_Single_Inverter_Output_Current
GS_Single_Inverter_Charge_Current
GS_Single_Inverter_Buy_Current
GS_Single_Inverter_Sell_Current
GS_Single_Grid_Input_AC_Voltage
GS_Single_Gen_Input_AC_Voltage
GS_Single_Output_AC_Voltage
GS_Single_Inverter_Operating_mode
GS_Single_Error_Flags
GS_Single_Warning_Flags
GS_Single_Battery_Voltage

#HAVE TO TEST TO SEE HOW THESE REGISTER POPULATE AND THEN WILL DECIDE IF WE NEED TO SHOW
GS_Single_kWh_SF
GS_Single_AC1_Buy_kWh
GS_Single_AC2_Buy_kWh
GS_Single_AC1_Sell_kWh
GS_Single_AC2_Sell_kWh
GS_Single_Output_kWh
GS_Single_Charger_kWh
GS_Single_Output_kW
GS_Single_Buy_kW
GS_Single_Sell_kW
GS_Single_Charge_kW
GS_Single_Load_kW
GS_Single_AC_Couple_kW



