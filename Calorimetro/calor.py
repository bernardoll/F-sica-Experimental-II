import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from odrpack import odr_fit

def f(t, p):
    a, T_0 = p[0], p[1]
    return a * t + T_0

file = pd.read_excel("Calorimetro/Dados_calorimetro.xlsx")

# Dados brutos
temperatura = np.array(file["temp. (C)"].tolist())
tempo = np.array(file["tempo (s)"].tolist())

# Incertezas
s_temperatura = np.array(file["s_temp. (C)"].tolist())

print(temperatura)

temperatura = temperatura[2:]
np.delete(tempo, [0, 1])
np.delete(s_temperatura, [0, 1])

print(temperatura)