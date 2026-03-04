import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pingouin as pg
from lets_plot import *
from requests import head

# ---------------------------------------------------
# 0. Definir estructura del proyecto (SIN os.chdir)
# ---------------------------------------------------

# Este archivo .py está dentro del proyecto
root = Path("C:/Users/anton/OneDrive/Documentos/GitHub/DoingEconomics_Taller-3")


Raw_data = root / "Data" / "Raw"
Clean_data = root / "Data" / "Clean"
output_g = root / "Outputs" / "Graphs"
output_t = root / "Outputs" / "Tables"

print("Project root:", root)
print("Data directory:", Raw_data)
print("Output directory:", output_g)

# ---------------------------------------------------
# 1. Configuración de gráficos
# ---------------------------------------------------

LetsPlot.setup_html(no_js=True)

plt.style.use(
    "https://raw.githubusercontent.com/aeturrell/core_python/main/plot_style.txt"
)

# ---------------------------------------------------
# 2. Cargar base de datos
# ---------------------------------------------------

main_db = Raw_data / "NH_Temp_means.csv"

df = pd.read_csv(
    main_db,
    skiprows=1,
    na_values="***",
)

print(df.head())

# Setear el año como índice
df = df.set_index("Year")

# ---------------------------------------------------
# 3. Graficar evolución
# ---------------------------------------------------

# 3.1 Gráfico de evolución de temperatura media anual (J-D) y octubre (Oct)
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df.index, df["Oct"], label="October", linestyle="--", color="tab:blue")
ax.axhline(0, linewidth=1.5, alpha=0.8, label="Promedio de 1951 a 1980", linestyle="--", color="tab:grey")

ax.set_xlim(df.index.min(), df.index.max())
ax.set_xlabel("Year")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_title(f"Northern Hemisphere temperature anomalies: October mean (1880–{df.index.max()})")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()

output_file = output_g / "Grafico_1_EvolucionOct.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"Gráfico guardado en: {output_file}")
plt.show()


# 3.2 Gráfico de evolución de temperatura media por estación (DJF, MAM, JJA, SON)
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df.index, df["DJF"], label="Winter (DJF)", alpha=0.8, linewidth=2)
ax.plot(df.index, df["MAM"], label="Spring (MAM)", alpha=0.8, linewidth=2)
ax.plot(df.index, df["JJA"], label="Summer (JJA)", alpha=0.8, linewidth=2)
ax.plot(df.index, df["SON"], label="Autumn (SON)", alpha=0.8, linewidth=2)
ax.axhline(0, linewidth=1.5, alpha=0.8, label="Promedio de 1951 a 1980", linestyle="--", color="tab:grey")

ax.set_xlim(df.index.min(), df.index.max())
ax.set_xlabel("Year")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_title(f"Northern Hemisphere temperature anomalies by season (1880–{df.index.max()})")
ax.legend(ncol=2)
ax.grid(alpha=0.3)

plt.tight_layout()

output_file = output_g / "Grafico_2_Seasonal.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"Gráfico guardado en: {output_file}")
plt.show()


# 3.3 Gráfico de evolución de temperatura media anual (J-D)
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df.index, df["J-D"], label="Mean annual (J-D)", color="tab:orange")
ax.axhline(0, linewidth=1.5, alpha=0.8, label="Promedio de 1951 a 1980", linestyle="--", color="tab:grey")


ax.set_xlim(df.index.min(), df.index.max())
ax.set_xlabel("Year")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_title(f"Northern Hemisphere temperature anomalies: annual mean (J-D) (1880–{df.index.max()})")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()

output_file = output_g / "Grafico_3_PromedioAnual.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"Gráfico guardado en: {output_file}")
plt.show()

#######################################
# 4. Tablas de Frecuencia e Histogramas
#######################################

df["Period"] = pd.cut(
    df.index,
    bins=[1950, 1980, 2010],
    labels=["1951—1980", "1981—2010"],
    ordered=True,
)

print(df.head())