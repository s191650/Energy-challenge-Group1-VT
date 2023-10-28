from math import*
import pandas as pd
import matplotlib.pylab as plt

meteo = pd.read_table("Data/meteo.csv",delimiter = ";")
meteo["HOUR"] = pd.to_numeric(meteo["HOUR"])
meteo_index = ["YEAR","MO","DY","HOUR","T"]

building_index = ["B22_c","B40_c","B41_c","B42_c","B44_c","B45_c"]


for building in range(len(building_index)):
    bg = pd.read_table(f'Data/{building_index[building]}.csv',delimiter =';')
    bg["P"] = pd.to_numeric(bg["P"])
    bg["HOUR"] = pd.to_numeric(bg["HOUR"])

    Q = pd.DataFrame(columns = ["YEAR","MO","DY","HOUR","P","T"])
    
    buffer = 0  # Compte le nombre de mesure prise sur une heure
    index = 0   # Variable gardant l'index de la première heure pile
    P = 0       # Somme de toutes les puissances mesurées sur une heure
    hour_passed = 0 
    meteo_index = 0 # index correspondant au fichier meteo
    for i in range(len(bg)):
        hour = bg.iloc[index]["HOUR"]
        if (hour == bg.iloc[i]["HOUR"]) :
            P = P + int(bg.iloc[i]["P"])
            buffer = buffer + 1
        else :
            if(buffer == 0):
                Q_var = pd.DataFrame({"YEAR" : [bg.iloc[i-1]["YEAR"]],
                                    "MO" : [bg.iloc[i-1]["MO"]],
                                    "DY" : [bg.iloc[i-1]["DY"]],
                                    "HOUR" : [hour],
                                    "P" : [P],
                                    "T" : [nan]})
            else :
                Q_var = pd.DataFrame({"YEAR" : [bg.iloc[i-1]["YEAR"]],
                                    "MO" : [bg.iloc[i-1]["MO"]],
                                    "DY" : [bg.iloc[i-1]["DY"]],
                                    "HOUR" : [hour],
                                    "P" : [P/buffer],
                                    "T" : [nan]})
            
            if(bg.iloc[i-1]["MO"] == meteo.iloc[meteo_index]["MO"] and                  # Verifie que le température correspond a la bonne valeur du mois/jour/heure
            bg.iloc[i-1]["DY"] == meteo.iloc[meteo_index]["DY"] and
                bg.iloc[i-1]["HOUR"] == meteo.iloc[meteo_index]["HOUR"] ):
                
                Q_var["T"] = meteo.iloc[meteo_index]["T"]
                meteo_index = meteo_index + 1
            else :
                while not (bg.iloc[i-1]["MO"] == meteo.iloc[meteo_index]["MO"] and      # Si pas la bonne valeur du mois/jour/heure on incremente meteo_index pour retrouver la bonne valeur
                bg.iloc[i-1]["DY"] == meteo.iloc[meteo_index]["DY"] and
                bg.iloc[i-1]["HOUR"] == meteo.iloc[meteo_index]["HOUR"]) :
                    
                    meteo_index = meteo_index + 1
                Q_var["T"] = meteo.iloc[meteo_index]["T"]
                meteo_index = meteo_index + 1

            Q = pd.concat([Q,Q_var])
            P = 0
            hour_passed = hour_passed + 1
            buffer = 0
            index = i
            i = i-1
            print(
                building_index[building],
                Q.iloc[hour_passed-1]["YEAR"],
                Q.iloc[hour_passed-1]["MO"],
                Q.iloc[hour_passed-1]["DY"],
                Q.iloc[hour_passed-1]["HOUR"],
                Q.iloc[hour_passed-1]["P"],
                Q.iloc[hour_passed-1]["T"])
    Q.to_csv(f"Q_dot_csv/Q_dot_{str(building_index[building])}.csv", index=False, sep = ";")