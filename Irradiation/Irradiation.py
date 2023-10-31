import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import*
import csv

Data = pd.read_csv('Irradiation/Weather_Data_Solcast.csv',delimiter = ";")
month = Data['MO']
day = Data['DY']
hour = Data['HR']
azimuth = Data['azimuth']
azimuth_star = [0, 90, 180, 270] # N, E, S, W
S_h = Data['dni']   # Direct Normal Irradiance
G_h = Data['gti']   # Global Tilt Irradiance
gamma = [0, 90, 180, 270] # N, E, S, W
phi = 50.577306 # Latitude VT [°]
L = 5.578983    # Longitude VT [°]
i = 90 # Tilt angle with the horizontal [°]
I = pd.DataFrame(columns=["I_north","I_east","I_south","I_west"])
for d in range(4):
    G_i_gamma = np.zeros(len(hour))
    for j in range(len(hour)):
        # 1) Sun position
        delta = 23.45 * sin(360/365*(day[j]-81)*pi/180)     # (2) Degree between normal of the earth and sun

        legal_time = hour[j]
    
        # Heure d'hiver : 302e j -> 85e j et heure d'ete : 86e j -> 301e j
        if day[j] >= 86 and day[j] < 302: 
            t_ms = legal_time - L/15 - 1-1      # Mean solar time in summer
            if(t_ms<0):
                t_ms = 24+t_ms
        else:
            t_ms = legal_time - L/15 - 1        # Mean solar time in winter
            if(t_ms<0):
                t_ms = 24+t_ms

        beta = 360/365*day[j]
        ET = -0.00002 + 0.4197*cos(beta*pi/180)-7.3509*sin(beta*pi/180)-3.2265*cos(2*beta*pi/180)-9.3912*sin(2*beta*pi/180)-0.0903*cos(3*beta*pi/180)-0.3361*sin(3*beta*pi/180)
        
        t = ET/60 + t_ms    # True solar time
        
        omega = (t - 12)*15     # Image of the apparent solar time t (Angle)

        h = asin(cos(delta*pi/180)*cos(omega*pi/180)*cos(phi*pi/180) + sin(delta*pi/180)*sin(phi*pi/180))/(pi/180)      # (4)

        # 2) Ratios
    
        R_S = sin(i*pi/180)*cos(azimuth[j]*pi/180 - gamma[d]*pi/180)/tan(h*pi/180) + cos(i*pi/180)

        if(G_h[j]== 0):
            R_G = 0
        else:   
            R_G = (R_S - (1 + cos(i*pi/180))/2) * (S_h[j]/G_h[j]) + (1+cos(i*pi/180))/2 + (1-cos(i*pi/180))/2*azimuth_star[d]       # (7)
        
        G_i_gamma[j] = round(R_G*G_h[j],2)
        #G_i_gamma[j] = abs(round(R_S*S_h[j],2))
        
    if d == 0:
        csv_filename = "I_north"
        I[csv_filename] = G_i_gamma.tolist()
    elif d == 1:
        csv_filename = "I_east"
        I[csv_filename] = G_i_gamma.tolist()
    elif d == 2:
        csv_filename = "I_south"
        I[csv_filename] = G_i_gamma.tolist()
    elif d == 3:
        csv_filename = "I_west"
        I[csv_filename] = G_i_gamma.tolist()

I.to_csv("Irradiation/Irradiation.csv", index=False, sep = ";")
