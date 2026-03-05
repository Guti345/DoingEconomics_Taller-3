import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pingouin as pg
from lets_plot import *
from requests import head

# ===================================================
# 0) CONFIGURACIÓN GENERAL DEL PROYECTO (PATHS)
# ===================================================
# Define la raíz del proyecto y construye rutas para:
# - Raw data (datos crudos)
# - Clean data (si aplica)
# - Outputs (gráficos y tablas)
root = Path("C:/Users/anton/OneDrive/Documentos/GitHub/DoingEconomics_Taller-3")

Raw_data = root / "Data" / "Raw"
Clean_data = root / "Data" / "Clean"
output_g = root / "Outputs" / "Graphs"
output_t = root / "Outputs" / "Tables"

print("Project root:", root)
print("Data directory:", Raw_data)
print("Output directory:", output_g)

# ===================================================
# 1) CONFIGURACIÓN DE ESTILO Y VISUALIZACIÓN
# ===================================================
# Configura lets-plot y aplica un estilo de gráficos (aeturrell/core_python)
LetsPlot.setup_html(no_js=True)

plt.style.use(
    "https://raw.githubusercontent.com/aeturrell/core_python/main/plot_style.txt"
)

# ===================================================
# PARTE 1.1 — ANALIZANDO ANOMALÍAS DE TEMPERATURA
# (Pregunta 1.1.1–1.1.3 del PDF)
# ===================================================

# ---------------------------------------------------
# 1.1) Cargar el dataset de anomalías de temperatura (NH)
# ---------------------------------------------------
# Lee el CSV de NASA (Northern Hemisphere means) y define "Year" como índice
main_db = Raw_data / "NH_Temp_means.csv"

df = pd.read_csv(
    main_db,
    skiprows=1,
    na_values="***",
)

print(df.head())

df = df.set_index("Year")

# ---------------------------------------------------
# 1.2) Gráficos de línea (mes, estación, anual)
# ---------------------------------------------------

# 1.1.3(i) Gráfico mensual: Octubre (Oct)
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

# 1.1.3(ii) Gráfico estacional: DJF, MAM, JJA, SON
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

# 1.1.3(iii) Gráfico anual: J-D
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

# ===================================================
# PARTE 1.2 — VARIACIÓN DE LA TEMPERATURA EN EL TIEMPO
# (Preguntas 1.2.1–1.2.5 del PDF)
# ===================================================

#######################################
# 1.2.1) Tablas de frecuencia (1951–1980 vs 1981–2010)
#######################################

# Selecciona la anomalía anual (J-D) y elimina valores perdidos
anom = df["J-D"].dropna()

# Separa dos periodos para comparar distribuciones
anom_1951_1980 = anom.loc[1951:1980]
anom_1981_2010 = anom.loc[1981:2010]

# Define bins para construir frecuencias (se usan bins separados y también uno combinado)
bins1 = np.arange(anom_1951_1980.min()-0.01, anom_1951_1980.max()+0.01, 0.05)
bins2 = np.arange(anom_1981_2010.min()-0.01, anom_1981_2010.max()+0.01, 0.05)
bins = np.unique(np.concatenate([bins1, bins2]))

# Frecuencias usando bins por periodo (mismo enfoque que en el taller)
freq_1951_1980 = pd.cut(anom_1951_1980, bins=bins1).value_counts().sort_index()
freq_1981_2010 = pd.cut(anom_1981_2010, bins=bins2).value_counts().sort_index()

# Frecuencias usando bins combinados (para comparar con bins consistentes si se requiere)
freq_1951_1980f = pd.cut(anom_1951_1980, bins=bins).value_counts().sort_index()
freq_1981_2010f = pd.cut(anom_1981_2010, bins=bins).value_counts().sort_index()

# Construye tablas finales (formato Range/Frequency)
tabla_1951_1980 = freq_1951_1980.reset_index()
tabla_1951_1980.columns = ["Range of temperature anomaly (T)", "Frequency"]

tabla_1981_2010 = freq_1981_2010.reset_index()
tabla_1981_2010.columns = ["Range of temperature anomaly (T)", "Frequency"]

print("Tabla de frecuencias 1951–1980")
print(tabla_1951_1980)

print("\nTabla de frecuencias 1981–2010")
print(tabla_1981_2010)

# Exporta tablas a Excel
tabla_1951_1980.to_excel(output_t / "tabla_1951_1980.xlsx", index=False)
tabla_1981_2010.to_excel(output_t / "tabla_1981_2010.xlsx", index=False)

#######################################
# 1.2.2) Histogramas comparativos (1951–1980 vs 1981–2010)
#######################################

# Crea dos histogramas (lado a lado) para comparar distribuciones
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

output_file = output_g / "Histograma_Comparacion_Anomalias.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"Gráfico guardado en: {output_file}")

plt.show()

#######################################
# 1.2.3) Deciles (D3 y D7) para 1951–1980
#######################################

# Calcula deciles 3 (30%) y 7 (70%) en el periodo base 1951–1980
d3 = np.quantile(anom_1951_1980, 0.3)
d7 = np.quantile(anom_1951_1980, 0.7)

# Organiza los deciles en tabla y exporta
tabla_deciles = pd.DataFrame({
    "Decile": ["D3", "D7"],
    "Quantile": [0.3, 0.7],
    "Temperature anomaly (°C)": [d3, d7]
})

print(tabla_deciles)
tabla_deciles.to_excel(output_t / "Tabla_Deciles_1951_1980.xlsx", index=False)

#######################################
# 1.2.4) Porcentaje de años “calientes” en 1981–2010 usando D7
#######################################

# Re-selecciona anomalías 1981–2010 (para asegurar consistencia)
anom_1981_2010 = anom.loc[1981:2010]

# Cuenta observaciones por encima del decil 7 (clasificadas como “calientes”)
hot_years = (anom_1981_2010 > d7).sum()

# Total de observaciones del periodo
total_years = len(anom_1981_2010)

# Porcentaje de “calientes”
hot_percentage = (hot_years / total_years) * 100

print("Años calientes:", hot_years)
print("Total de años:", total_years)
print(f"Porcentaje de anomalías calientes: {hot_percentage:.2f}%")

# Tabla resumen y exportación
tabla_resultado = pd.DataFrame({
    "Category": ["Hot anomalies (> D7)"],
    "Number of years": [hot_years],
    "Percentage (%)": [round(hot_percentage, 2)]
})

print(tabla_resultado)
tabla_resultado.to_excel(output_t / "Tabla_Resultado_Hot_Anomalies.xlsx", index=False)

#######################################
# 1.2.5) Media y varianza por estación en tres periodos (1921–1950, 1951–1980, 1981–2010)
#######################################

# Define columnas estacionales
stations = ["DJF", "MAM", "JJA", "SON"]

# Divide el dataset en tres periodos
p1 = df.loc[1921:1950, stations]
p2 = df.loc[1951:1980, stations]
p3 = df.loc[1981:2010, stations]

# Calcula medias por estación y periodo
mean_1921_1950 = p1.mean()
mean_1951_1980 = p2.mean()
mean_1981_2010 = p3.mean()

# Calcula varianzas por estación y periodo
var_1921_1950 = p1.var()
var_1951_1980 = p2.var()
var_1981_2010 = p3.var()

# Construye una tabla consolidada (medias y varianzas) y exporta
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

# ===================================================
# PARTE 1.3 — CO₂ Y SU RELACIÓN CON LA TEMPERATURA
# (Preguntas 1.3.3–1.3.4 del PDF)
# ===================================================

# -------------------------------------------
# 1.3.3) Gráfico de CO2 (Interpolated y Trend) desde enero de 1960
# -------------------------------------------

main_db1 = Raw_data / "doing-economics-datafile-working-in-excel-project-1.xlsx"

df_1 = pd.read_excel(
    main_db1,
    sheet_name="Sheet1"
)

print(df_1.head())

# Crea una columna Date para manejar serie temporal mensual
df_1["Date"] = pd.to_datetime(dict(year=df_1["Year"], month=df_1["Month"], day=1))

# Filtra datos a partir de 1960-01
df_1960 = df_1[df_1["Date"] >= "1960-01-01"]

# Grafica CO2 interpolated y trend
fig, ax = plt.subplots(figsize=(10,6))

ax.plot(df_1960["Date"], df_1960["Interpolated"], label="CO₂ (Interpolated)", linewidth=2)
ax.plot(df_1960["Date"], df_1960["Trend"], label="CO₂ Trend", linestyle="--", linewidth=2)

ax.set_xlabel("Time (Year)")
ax.set_ylabel("CO₂ concentration (ppm)")
ax.set_title("Atmospheric CO₂ Levels (1960–Present)")

ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Guarda el gráfico de CO2
fig.savefig(output_g / "Grafico_CO2_1960_Present.png", dpi=300, bbox_inches="tight")

# -------------------------------------------
# 1.3.4) Unir CO2 (Trend) con anomalías de temperatura (mes elegido: enero)
# -------------------------------------------

# Selecciona CO2 Trend para enero (Month == 1) y renombra la columna
co2_jan = df_1[df_1["Month"] == 1][["Year", "Trend"]]
co2_jan = co2_jan.rename(columns={"Trend": "CO2_trend"})

# Selecciona anomalías de temperatura para enero y renombra
temp_jan = df[["Jan"]].reset_index()
temp_jan = temp_jan.rename(columns={"Jan": "Temp_anomaly"})

# Une ambas bases por año
merged = pd.merge(temp_jan, co2_jan, on="Year", how="inner")

# Diagrama de dispersión: CO2 vs anomalía de temperatura
fig, ax = plt.subplots(figsize=(8,6))

ax.scatter(
    merged["Temp_anomaly"],
    merged["CO2_trend"],
    alpha=0.7
)

ax.set_xlabel("Temperature anomaly (°C)")
ax.set_ylabel(r"CO$_2$ concentration (ppm)")
ax.set_title(r"Relationship between CO$_2$ levels and temperature anomalies")

ax.grid(alpha=0.3)

plt.tight_layout()

# Guarda el scatter
fig.savefig(output_g / "Scatter_CO2_Temp.png", dpi=300)

plt.show()

# Correlación de Pearson entre anomalía (enero) y CO2 trend (enero)
pearson_corr = merged["Temp_anomaly"].corr(merged["CO2_trend"])
print("Pearson correlation:", round(pearson_corr, 3))

# Guarda correlación en tabla Excel
table_corr = pd.DataFrame({
    "Correlation": [round(pearson_corr, 3)]
})

table_corr.to_excel(output_t / "Tabla_Correlacion_CO2_Temp.xlsx", index=False)