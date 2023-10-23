from math import*
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

meteo = pd.read_table('Meteo.csv',delimiter =";")
bg = pd.read_table('Building_geometry.csv',delimiter =";")
bg = bg.set_index(['Building Geometry'])

size_row = meteo.shape[0]
size_col = bg.shape[0]

K = np.zeros((size_row,size_col))
Q_load = np.zeros((size_row,size_col))
delta_T = np.zeros(size_row)

for j in range(size_col):
    for i in range(size_row):  
        K[i][j] =  bg.iloc[j]['Exterior wall surface']*bg.iloc[j]['U wall'] 
        + bg.iloc[j]['North-oriented Window area']*bg.iloc[j]['U window']
        + bg.iloc[j]['South-oriented Window area']*bg.iloc[j]['U window']
        + bg.iloc[j]['West-oriented Window area']*bg.iloc[j]['U window']
        + bg.iloc[j]['East-oriented Window area']*bg.iloc[j]['U window']
        + bg.iloc[j]['Zone surface m^2']*bg.iloc[j]['U floor'] 
        + bg.iloc[j]['Zone surface m^2']*bg.iloc[j]['U ceiling'] 
        + meteo.iloc[i]['U_wind (m/s)']
        delta_T[i] = 15-meteo.iloc[i]['Temperature C']
        Q_load[i][j] = K[i][j]*delta_T[i]/1000
        if Q_load[i][j] < 0:
            Q_load[i][j] = 0
        
    plt.scatter(meteo.iloc[:]['Temperature C'], Q_load[:, j])
    plt.xlabel("Temperature [C°]")
    plt.ylabel(r"Q$_{load}$ [kW]")
    plt.title(str(bg.index[j])+" energy signature")
    plt.grid()
    plt.xlim(left = -15,right = 40)
    plt.xticks(np.arange(-15,45,5))
    plt.ylim(bottom = 0, top = ceil(Q_load[:, j].max()/10)*10)
    plt.savefig(f"{str(bg.index[j])}.png")
    plt.clf()
    print(str(bg.index[j])+" printed")


