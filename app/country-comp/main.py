"""
Run in background with Python 3.5 or higher; uses Bokeh 0.12.10 installed.
Bokeh server defaults to running on port 5006:

    $ bokeh serve countries-plot

Run on alternate port if 5006 is in use:

    $ bokeh serve countries-plot --port 5007
"""

from os.path import dirname, join
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Select
from bokeh.io import curdoc
from plot_options import apply_plot_options

world = pd.read_csv(join(dirname(__file__), "data.csv"))

axis_map = {
    "GNP Per-Capita (USD)": "per_cap_gnp",
    "Life Expectancy (years)": "lifeexpectancy",
    "Surface Area (sq km)": "surfacearea",
    "Year of Independence": "indepyear"
}

# Create Input controls
ctry_selec = Select(title="Country",
                    options=sorted(set(world.country.values)), value='All')
regn_selec = Select(title="Region",
                    options=sorted(set(world.region.values)), value='All')
cont_selec = Select(title="Continent",
                    options=sorted(set(world.continent.values)), value='All')
govt_selec = Select(title="Form of Government",
                    options=sorted(set(world.govtform.values)), value='All')
x_axis = Select(title="X-Axis (choose quantity to plot)",
                options=sorted(axis_map.keys()), value='GNP Per-Capita (USD)')
y_axis = Select(title="Y-Axis (choose quantity to plot)",
                options=sorted(axis_map.keys()), value="Life Expectancy (years)")

cds = ColumnDataSource(data=dict(x=[], y=[], color=[], alpha=[], country=[],
                                 region=[], continent=[], govtform=[],
                                 surfacearea=[], indepyear=[], lifeexpectancy=[],
                                 per_cap_gnp=[]))

hover = HoverTool(
    tooltips=[
        ("Country", "@country"),
        ("Region", "@region"),
        ("Continent", "@continent"),
        ("Form of Gov't", "@govtform"),
        ("Surface Area", "@surfacearea{0.} km-sq"),
        ("Year of Independence", "@indepyear{0}"),
        ("Life Expectancy", "@lifeexpectancy{0.} years"),
        ("GNP Per-Capita", "@per_cap_gnp{0.} (USD)"),
    ])
tools = [hover, 'box_zoom,wheel_zoom,pan,reset']

f = figure(plot_width=500, plot_height=500, tools=tools)

f.circle(source=cds, x='x', y='y', color='color', line_color=None,
         fill_alpha='alpha', size=10)

apply_plot_options(f)

def select_countries():

    selec = world.copy()

    # default color is grey with very light alpha
    selec['color'] = 'grey' 
    selec['alpha'] = 0.25

    # selected points will be full-alpha purple
    selec_col = 'purple'; selec_alpha = 1.0

    if ctry_selec.value != 'All':
        ctry = selec.loc[ selec.country==ctry_selec.value ].copy()
    else:
        ctry = selec.loc[:].copy()
    ctry.reset_index(inplace=True)

    if regn_selec.value != 'All':
        regn = selec.loc[ selec.region==regn_selec.value ].copy()
    else:
        regn = selec.loc[:].copy()
    regn.reset_index(inplace=True)

    if cont_selec.value != 'All':
        cont = selec.loc[ selec.continent==cont_selec.value ].copy()
    else:
        cont = selec.loc[:].copy()
    cont.reset_index(inplace=True)

    if govt_selec.value != 'All':
        govt = selec.loc[ selec.govtform==govt_selec.value ].copy()
    else:
        govt = selec.loc[:].copy()
    govt.reset_index(inplace=True)

    m1 = ctry.merge(regn, how='inner', on='index')
    m2 = m1.merge(cont, how='inner', on='index')
    m3 = m2.merge(govt, how='inner', on='index')
    m3.rename(columns={'index': 'orig_index'}, inplace=True)

    selec_indices = m3['orig_index'].values
    selec.loc[selec.index.isin(selec_indices), 'color'] = selec_col
    selec.loc[selec.index.isin(selec_indices), 'alpha'] = selec_alpha

    # return without the "All" row at bottom
    return selec[:-1]


def update():
    df = select_countries()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    f.xaxis.axis_label = x_axis.value
    f.yaxis.axis_label = y_axis.value

    cds.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        alpha=df["alpha"],
        country=df["country"],
        region=df["region"],
        continent=df["continent"],
        govtform=df["govtform"],
        surfacearea=df["surfacearea"],
        indepyear=df["indepyear"],
        lifeexpectancy=df["lifeexpectancy"],
        per_cap_gnp=df["per_cap_gnp"],
    )

controls = [ctry_selec, regn_selec, cont_selec, govt_selec, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

desc = Div(text=open(join(dirname(__file__), "description.html")).read(),
            width=800)

sizing_mode = 'fixed'

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, f]
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Countries Comparison"
