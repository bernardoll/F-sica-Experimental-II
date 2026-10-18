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

ajuste = odr_fit(f, tempo, temperatura, [2.0, 0.0], weight_y=s_temperatura, weight_x=None)

# Resultado
a_otimo, T_0_otimo = ajuste.beta
erro_a, erro_T_0 = ajuste.sd_beta

print("Resultado do Ajuste:")
print(f"a (slope)   = {a_otimo:.8f} ± {erro_a:.8f}")
print(f"T_0 (interc) = {T_0_otimo:.8f} ± {erro_T_0:.8f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0.05)

# plotagem do erro - CORRIGIDO AQUI
ax1.errorbar(tempo, temperatura, yerr=s_temperatura, fmt='o', ms=5, label='Dados com barras de erro')

# plotagem da curva
tempo_curva = np.linspace(tempo.min(), tempo.max(), 500)
temperatura_curva = f(tempo_curva, [a_otimo, T_0_otimo])
ax1.plot(tempo_curva, temperatura_curva, label=fr'Ajuste ODR ($a = \ \frac{{Vit}}{{C}} \ = \ ${a_otimo:.2f})') # Adicionado label=
ax1.set_xlabel('Tempo (s)')
ax1.set_ylabel('Temperatura (°C)')
ax1.legend()
ax1.grid(True)

ax2.errorbar(tempo, ajuste.eps, yerr=s_temperatura, fmt='o', color='blue')
ax2.axhline(0, color='black', linestyle='--')
ax2.set_xlabel('Tempo (s)')
ax2.set_ylabel('Resíduos')
ax2.grid(True)

plt.show()