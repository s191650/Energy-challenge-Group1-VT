from math import*
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

building_index = ["B22_c","B40_c","B41_c","B42_c","B44_c","B45_c"]


for building in range(len(building_index)):
    Q = pd.read_table(f"Q_dot_csv/Q_dot_{str(building_index[building])}.csv",delimiter = ";")
    # Energy signature
    plt.scatter(Q.iloc[:]["T"], Q.iloc[:]["P"])
    plt.grid()
    plt.xlabel("Temperature [C°]")
    plt.ylabel(r"Q$_{load}$ [kW]")
    plt.xticks(np.arange(-15,45,5))
    plt.title(str(building_index[building])+" energy signature")
    plt.savefig(f"Energy-signature/{str(building_index[building])}.png")
    plt.clf()
    print(f"{str(building_index[building])} plotted")

    # Load curve
    plt.plot(np.arange(len(Q)), Q.iloc[:]["P"])
    plt.grid()
    plt.xlabel(r"$\tau$, time")
    plt.ylabel(r"Q$_{load}$ [kW]")
    plt.title(str(building_index[building])+" load curve")
    plt.fill_between(np.arange(len(Q)), Q.iloc[:]["P"], 0, color='#1f77b4', alpha=1)
    plt.savefig(f"Load-curve/{str(building_index[building])}-load-curve.png")
    plt.clf()