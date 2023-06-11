# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 11:28:57 2023

@author: Yannis
"""
import datetime
from rocketpy import Environment, SolidMotor, Rocket, Flight, HybridMotor
import numpy as np
from matplotlib import pyplot as plt

#%% ENVIRONMENT
print('')
print('ENVIRONMENT')
#tomorrow's date
tomorrow = datetime.date.today() + datetime.timedelta(days=1) 


Env = Environment(railLength=12, 
                  latitude=39.388692, 
                  longitude=-8.287814, 
                  elevation=130)

Env.setDate((tomorrow.year, tomorrow.month, tomorrow.day, 12))  # Hour given in UTC time
Env.setAtmosphericModel(type="Forecast", file="GFS")
# Env.info()
print('')
print('done')
#%% MOTOR
print('')
print('MOTOR')
HALCYON_motor = HybridMotor(
    thrustSource=('Hycion_5.eng'),
    burnOut=3.9,                                                #           y
    grainNumber=1,                                              #           y
    grainSeparation=0/1000,                                     #[m]        y
    grainDensity=920,                                           #[kg/m^3]   y
    grainOuterRadius=43/1000,                                   #[m]        y
    grainInitialInnerRadius=22.5/1000,                          #[m]        y
    grainInitialHeight=310/1000,                                #[m]        y
    nozzleRadius=0.0141,                                        #[m]        y
    throatRadius=0.00677,                                       #[m]        y
    # oxidizer
    oxidizerTankRadius = 70/1000,                               #[m]        y
    oxidizerTankHeight = 320/1000,                              #[m]        y
    oxidizerInitialPressure = 39.4769,                          #[atm]      y
    oxidizerDensity = 960,                                      #[kg/m^3]   y
    oxidizerMolarMass = 44.013,                                 #N2O        y
    oxidizerInitialVolume = 4.3/0.96/100000,                    #           y
    distanceGrainToTank = 600/1000,                             #           y
    injectorArea = 1e-4,                                        #[m^2?]     y
    interpolationMethod = 'linear'                              # -         y
)

# HALCYON_motor.info()
print('')
print('done')
#%% ROCKET
print('')
print('ROCKET')
HALCYON = Rocket(
    motor=HALCYON_motor,
    radius=152.4 / 2000,                                        #[kg/m^2]   y
    mass= 33.8,                                                 #[kg]
    inertiaI= 6.86,                                             #[kg*m^2]
    inertiaZ= 0.069,                                            #[kg*m^2]
    distanceRocketNozzle=-1.579,                                 #[m] 
    distanceRocketPropellant=-0.964,                             #[m] 
    powerOffDrag="powerOffDragCurve.csv",                       # -
    powerOnDrag="powerOnDragCurve.csv"                          # -
)

HALCYON.setRailButtons([-0.259, -1.352])

print('')
print('done')
#%% NOSECONE
print('')
print('NOSECONE')
NoseCone = HALCYON.addNose(length=0.46,                         #[m]
                           kind="vonKarman",                    # -         y
                           distanceToCM=1.452)                    # -         
print('')
print('done')
#%% FINS
print('')
print('FINS')
FinSet = HALCYON.addTrapezoidalFins(4,
                                    span=(0.125+0.148)/2,                  #[m]           
                                    rootChord=0.247,             #[m]
                                    tipChord=0.05,             #[m]
                                    distanceToCM=-1.387)        #[m]

print('')
print('done')
#%% TAIL
print('')
print('TAIL')
Tail = HALCYON.addTail(
    topRadius=152.4/2000, 
    bottomRadius=0.0496, 
    length=0.254, 
    distanceToCM=-1.381
)

print('')
print('done')
#%% PARACHUTE
print('')
print('PARACHUTE')
def drogueTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False
    #return True if y[5] < 0 and y[2] < 200 + 100 else False

def mainTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+136 due to surface elevation).
    return True if y[5] < 0 and y[2] < 450 + 100 else False


Main = HALCYON.addParachute(
    "Main",
    CdS=9.621,
    trigger=mainTrigger,
    samplingRate=100,
    lag=5,
    noise=(0, 8.3, 0.5),
)

Drogue = HALCYON.addParachute(
    "Drogue",
    CdS=0.875,
    trigger=drogueTrigger,
    samplingRate=100,
    lag=1,
    noise=(0, 8.3, 0.5),
)
print('')
print('done')
#%% SIMULATION
print('')
print('SIMULATION')
TestFlight = Flight(rocket=HALCYON, 
                    environment=Env, 
                    inclination=85, 
                    heading=160)
print('')
print('done')
#%%

TestFlight.plot3dTrajectory()
# TestFlight.allInfo()
#%%
TestFlight.plotStabilityAndControlData()





