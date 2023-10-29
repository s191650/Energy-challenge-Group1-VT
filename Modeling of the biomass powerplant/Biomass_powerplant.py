# -*- coding: utf-8 -*-
from CoolProp.CoolProp import PropsSI
import numpy as np

"Données"

fluid = 'Water'

P = np.zeros(9, dtype=float)
T = np.zeros(9, dtype=float)
s = np.zeros(9, dtype=float)
h = np.zeros(9, dtype=float)
x = np.zeros(9, dtype=float)

m_dot_vap = 3.6 #[kg/s]
Q_dot_th = 6.5e6 # [W]
 
eta_t_is = 0.84
eta_p_is = 0.88
eta_alt = 0.96

T[1] = 420 + 273.15 # [K]
P[1] = 42e5 # [Pa]
P[2] = 200e3 # [Pa]
P[4] = 10e3 # [Pa]

"Résolution"
"Hypothèse : tous les échangeurs sont isobares"


"1-2. Turbine HP"
"Etat 1 : on connait la température et la pression donc on peut calculer l'enthalpie et l'entropie"
(h[1],s[1]) = PropsSI(('H','S'),'P',P[1],'T',T[1],fluid)

"Efficacité isentropique d'une turbine"

h_2s = PropsSI('H','P',P[2],'S',s[1],fluid)
h[2] = h[1]-eta_t_is*(h[1]-h_2s)

(s[2],T[2],x[2]) = PropsSI(('S','T','Q'),'P',P[2],'H',h[2],fluid)

W_dot_t_HP = m_dot_vap*(h[1]-h[2])

"2-3. Réseau de chaleur"
P[3] = P[2]
x[3] = 0 # "! hypothèse car pas d'information sur les conditions du fluide en sortie d'échangeur"
 
(h[3],s[3],T[3]) = PropsSI(('H','S','T'),'P',P[3],'Q',x[3],fluid)

y = Q_dot_th/(m_dot_vap*(h[2]-h[3]))
" y est la fraction de vapeur soutirée"
"Une partie de la vapeur va céder sa chaleur dans l'échangeur qui alimente le réseau de chaleur."
"Une fois sortie de cet échangeur, on peut suposer que l'eau est à l'état de liquide saturé et elle ne peut donc pas être détendue dans la seconde turbine."


"2-4. Turbine BP"
"La seconde partie de la vapeur peut être détendue dans une turbine basse pression pour extraire un maximum de travail"


h_4s = PropsSI('H','P',P[4],'S',s[2],fluid)
h[4] = h[2] - eta_t_is*(h[2]-h_4s)

(s[4],T[4],x[4]) = PropsSI(('S','T','Q'),'P',P[4],'H',h[4],fluid)

W_dot_t_BP = (1-y)*m_dot_vap*(h[2]-h[4])


"4-5. Condenseur"
P[5] = P[4]
x[5] = 0 # "! hypothèse car pas d'information sur les conditions du fluide en sortie de condenseur"
 
(h[5],s[5],T[5]) = PropsSI(('H','S','T'),'P',P[5],'Q',x[5],fluid)


"5-6. Pompe BP"
P[6] = P[3]

h_6s = PropsSI('H','P',P[6],'S',s[5],fluid)
h[6] = eta_p_is*(h_6s-h[5]) + h[5]

(s[6],T[6]) = PropsSI(('S','T'),'P',P[6],'H',h[6],fluid)

W_dot_p_BP = m_dot_vap*(1-y)*(h[6]-h[5])


"3/6-7. Mélange"
"Conservation de l'énergie lors du mélange"
h[7] = y*h[3] + (1-y)*h[6]

"! NB: les mélange se font toujours à pression constante"
P[7] = P[3]

(s[7],T[7]) = PropsSI(('S','T'),'P',P[7],'H',h[7],fluid)



"7-8. Pompe HP"
P[8] = P[1]

h_8s = PropsSI('H','P',P[8],'S',s[7],fluid)
h[8] = eta_p_is*(h_8s-h[7]) + h[7]

(s[8],T[8]) = PropsSI(('S','T'),'P',P[8],'H',h[8],fluid)

W_dot_p_HP = m_dot_vap*(h[8]-h[7])


"8-1. Générateur de vapeur"
Q_dot_gen = m_dot_vap*(h[1]-h[8])

"Performances du cycle"
W_dot_el = eta_alt*(W_dot_t_BP + W_dot_t_HP) - W_dot_p_BP - W_dot_p_HP
 
eta_el = W_dot_el/Q_dot_gen
eta_th = Q_dot_th/Q_dot_gen
eta_cogen = eta_th + eta_el

print("a. La fraction de vapeur soutirée :",round(y,4))
print("b. La puissance nette générée par l'unité de cogénération :",round(W_dot_el,2),"W")
print("c. La puissance fournie par le générateur de vapeur :",round(Q_dot_gen,2),"W")
print("d. Le rendement de l'unité de cogénération :",round(eta_cogen,4))