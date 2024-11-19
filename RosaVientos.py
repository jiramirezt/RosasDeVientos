import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import cm

from windrose import WindroseAxes, plot_windrose

# Importar archivo desde excel
data = pd.read_excel(r'Datos_Rosa.xlsx')

ws = data['Vel'].to_numpy()
wd = data['Dir'].to_numpy()

# Grafica general
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, bins=np.arange(0, 10, 2) ,normed=True, opening=0.8, edgecolor="white")
ax.set_legend(title=r"$m \cdot s^{-1}$")
# Modificar el eje y de las figuras
y_ticks = range(0, 35, 5)
ax.set_rgrids(y_ticks, y_ticks)
plt.savefig("RosaVientos.png", dpi=300, bbox_inches="tight")


# Grafica mensual
wind_data = data.rename(columns={'Fecha': 'Fecha',
                                 'Vel': 'ws',
                                 'Dir':'wd',
                                 'Mes':'Mes'})

def plot_windrose_subplots(data, *, direction, var, color=None, **kwargs):
    """wrapper function to create subplots per axis"""
    ax = plt.gca()
    ax = WindroseAxes.from_ax(ax=ax)
    plot_windrose(direction_or_df=data[direction], var=data[var], ax=ax, **kwargs)


# Crear el subplot vacio para cada uno de los valores
g = sns.FacetGrid(
    data=wind_data,
    # Se crea un subplot por cada uno de los meses 
    col="Mes",
    # place a maximum of 3 plots per row
    col_wrap=3,
    subplot_kws={"projection": "windrose"},
    sharex=False,
    sharey=False,
    despine=False,
    height=3.5,
)

g.map_dataframe(
    plot_windrose_subplots,
    direction="wd",
    var="ws",
    normed=True,
    # Ajusrar el rango de velocidades que se ilustrara en la leyenda
    bins=(0.1, 2, 4, 6, 8),
    calm_limit=0.1,
    kind="bar",
)

# Hacer que se tenga el mismo eje y con fines comparativos entre los subplots
y_ticks = range(0, 35, 5)
for ax in g.axes:
    ax.set_legend(
        title=r"$m \cdot s^{-1}$", bbox_to_anchor=(1.15, -0.1), loc="lower right"
    )
    ax.set_rgrids(y_ticks, y_ticks)

# Ajustar el espacio entre los subplots 
plt.subplots_adjust(wspace=-0.07)
plt.savefig("RosaVientosMensual.png", dpi=300, bbox_inches="tight")