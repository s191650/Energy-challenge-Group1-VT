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
    
    # Energy signature
    plt.scatter(meteo.iloc[:]['Temperature C'], Q_load[:, j])
    plt.xlabel("Temperature [C°]")
    plt.ylabel(r"Q$_{load}$ [kW]")
    plt.title(str(bg.index[j])+" energy signature")
    plt.grid()
    plt.xlim(left = -15,right = 40)
    plt.xticks(np.arange(-15,45,5))
    plt.ylim(bottom = 0, top = ceil(Q_load[:, j].max()/10)*10)
    plt.savefig(f"Energy-signature/{str(bg.index[j])}.png")
    plt.clf()
    
    # Load curve
    plt.plot(np.arange(8760), Q_load[:, j])
    plt.xlabel(r"$\tau$, time")
    plt.ylabel(r"Q$_{load}$ [kW]")
    plt.title(str(bg.index[j])+" load curve")
    plt.ylim(bottom = 0, top = ceil(Q_load[:, j].max()/10)*10)
    plt.xlim(left=0,right = 8760)
    plt.xticks([15*24,46*24,74*24,105*24,135*24,166*24,196*24,227*24,258*24,288*24,319*24,349*24],["Jan-15","Feb-15","Mar-15","Apr-15","May-15","Jun-15","Jul-15","Aug-15","Sep-15","Oct-15","Nov-15","Dec-15"],rotation = 45)
    plt.fill_between(np.arange(8760), Q_load[:, j], 0, color='#1f77b4', alpha=1)
    plt.savefig(f"Load-curve/{str(bg.index[j])}-load-curve.png")
    plt.clf()
    
    print(str(bg.index[j])+" printed")


