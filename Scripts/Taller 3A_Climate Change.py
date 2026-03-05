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

anom = df["J-D"].dropna()

anom_1951_1980 = anom.loc[1951:1980]
anom_1981_2010 = anom.loc[1981:2010]

bins1 = np.arange(anom_1951_1980.min()-0.01, anom_1951_1980.max()+0.01, 0.05)
bins2 = np.arange(anom_1981_2010.min()-0.01, anom_1981_2010.max()+0.01, 0.05)
bins = np.unique(np.concatenate([bins1, bins2]))

freq_1951_1980 = pd.cut(anom_1951_1980, bins=bins1).value_counts().sort_index()
freq_1981_2010 = pd.cut(anom_1981_2010, bins=bins2).value_counts().sort_index()

freq_1951_1980f = pd.cut(anom_1951_1980, bins=bins).value_counts().sort_index()
freq_1981_2010f = pd.cut(anom_1981_2010, bins=bins).value_counts().sort_index()

tabla_1951_1980 = freq_1951_1980.reset_index()
tabla_1951_1980.columns = ["Range of temperature anomaly (T)", "Frequency"]

tabla_1981_2010 = freq_1981_2010.reset_index()
tabla_1981_2010.columns = ["Range of temperature anomaly (T)", "Frequency"]

print("Tabla de frecuencias 1951–1980")
print(tabla_1951_1980)

print("\nTabla de frecuencias 1981–2010")
print(tabla_1981_2010)

tabla_1951_1980.to_excel(output_t / "tabla_1951_1980.xlsx", index=False)
tabla_1981_2010.to_excel(output_t / "tabla_1981_2010.xlsx", index=False)

# -----------------------------
# Crear figura con dos histogramas
# -----------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

# Histograma 1951–1980
ax[0].hist(anom_1951_1980, bins=bins, color="tab:blue", alpha=0.8, edgecolor="black")
ax[0].axvline(0, color="black", linewidth=1.5, label="Promedio 1951–1980")
ax[0].set_title("Temperature anomalies (1951–1980)")
ax[0].set_xlabel("Temperature anomaly (°C)")
ax[0].set_ylabel("Frequency")
ax[0].legend()
ax[0].grid(alpha=0.3)

# Histograma 1981–2010
ax[1].hist(anom_1981_2010, bins=bins, color="tab:orange", alpha=0.8, edgecolor="black")
ax[1].axvline(0, color="black", linewidth=1.5, label="Promedio 1951–1980")
ax[1].set_title("Temperature anomalies (1981–2010)")
ax[1].set_xlabel("Temperature anomaly (°C)")
ax[1].legend()
ax[1].grid(alpha=0.3)

plt.suptitle("Distribution of Northern Hemisphere temperature anomalies", fontsize=14)

plt.tight_layout()

# Guardar gráfico
output_file = output_g / "Histograma_Comparacion_Anomalias.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print(f"Gráfico guardado en: {output_file}")

plt.show()

# Calcular deciles
d3 = np.quantile(anom_1951_1980, 0.3)
d7 = np.quantile(anom_1951_1980, 0.7)

# Crear tabla
tabla_deciles = pd.DataFrame({
    "Decile": ["D3", "D7"],
    "Quantile": [0.3, 0.7],
    "Temperature anomaly (°C)": [d3, d7]
})

print(tabla_deciles)
tabla_deciles.to_excel(output_t / "Tabla_Deciles_1951_1980.xlsx", index=False)

# -----------------------------
# Clasificar anomalías 1981–2010
# -----------------------------

# anomalías del periodo
anom_1981_2010 = anom.loc[1981:2010]

# contar años "calientes"
hot_years = (anom_1981_2010 > d7).sum()

# total de observaciones
total_years = len(anom_1981_2010)

# porcentaje
hot_percentage = (hot_years / total_years) * 100

print("Años calientes:", hot_years)
print("Total de años:", total_years)
print(f"Porcentaje de anomalías calientes: {hot_percentage:.2f}%")

tabla_resultado = pd.DataFrame({
    "Category": ["Hot anomalies (> D7)"],
    "Number of years": [hot_years],
    "Percentage (%)": [round(hot_percentage, 2)]
})

print(tabla_resultado)
tabla_resultado.to_excel(output_t / "Tabla_Resultado_Hot_Anomalies.xlsx", index=False)

# -----------------------------
# Estaciones a analizar
# -----------------------------
stations = ["DJF", "MAM", "JJA", "SON"]

# -----------------------------
# Definir periodos
# -----------------------------
p1 = df.loc[1921:1950, stations]
p2 = df.loc[1951:1980, stations]
p3 = df.loc[1981:2010, stations]

# -----------------------------
# Calcular medias
# -----------------------------
mean_1921_1950 = p1.mean()
mean_1951_1980 = p2.mean()
mean_1981_2010 = p3.mean()

# -----------------------------
# Calcular varianzas
# -----------------------------
var_1921_1950 = p1.var()
var_1951_1980 = p2.var()
var_1981_2010 = p3.var()

# -----------------------------
# Organizar resultados en tabla
# -----------------------------
tabla_estaciones = pd.DataFrame({
    "Mean 1921–1950": mean_1921_1950,
    "Variance 1921–1950": var_1921_1950,
    "Mean 1951–1980": mean_1951_1980,
    "Variance 1951–1980": var_1951_1980,
    "Mean 1981–2010": mean_1981_2010,
    "Variance 1981–2010": var_1981_2010
})

print(tabla_estaciones)
tabla_estaciones = tabla_estaciones.round(3)
tabla_estaciones.to_excel(output_t / "Tabla_Estaciones.xlsx", index=True)