import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
from textwrap import dedent
import os

from app import app

from paint.traffic import paintCarTrafficInZBS
from paint.metro import paintMetroUsageInZBS
from paint.covid import paintCovidCasesInZBS
from paint.bike import paintBikeTravelsEveryHour, paintBikeTravelsSankey

from utils import getRootPath

from preprocess.trafico import *

# Token for mapbox
token = 'pk.eyJ1IjoiY3RhcmF6b25hIiwiYSI6ImNrZDkxcW1sYjBwOWkycnM4NDRpbXViYnYifQ.jK8gChNK_dzVpKlrKKfJgA'

##############LOAD DATA
df = pd.read_csv(os.path.join(getRootPath(), 'data/metro/raw_data/metro_data_fin.csv'))
years = df['year'].unique()

# Data for the map
df2 = pd.read_csv(os.path.join(getRootPath(), 'data/metro/raw_data/mapas_metro.csv'))
data = "Ent_2019"

data_options = ['Ent_2014', 'Util_2014', 'Ent_2015', 'Util_2015', 'Ent_2016',
                'Util_2016', 'Ent_2017', 'Util_2017', 'Ent_2018', 'Util_2018',
                'Ent_2019', 'Util_2019']

years_map = []
volume_type = []
for i in data_options:
    years_map.append(i.split('_')[1])
    volume_type.append(i.split('_')[0])

np_years = np.unique(np.array(years_map))
np_volume_type = np.unique(np.array(volume_type))
labels_vol = ['Entradas', 'Utilizaciones']

dropdown_years_map = dcc.Dropdown(
    id='dropdown_years_map',
    options=[{'label': i, 'value': i} for i in np_years],
    value='2019',
    placeholder="Seleccione un año"
)
dropdown_tipo_map = dcc.Dropdown(
    id='dropdown_tipo_map',
    options=[{'label': labels_vol[0], 'value': np_volume_type[0]},
             {'label': labels_vol[1], 'value': np_volume_type[1]}],
    value=np_volume_type[0],
    placeholder="Seleccione Entrada/Utilizacion"
)

dropdown_lines = dcc.Dropdown(
    id='dropdown_lines',
    options=[{'label': i, 'value': i} for i in years],
    value=2019,
    placeholder='Select a year'
)

# Dropdown months biciMAD
months = ['01', '02', '03', '04', '05', '06']
dropdown_months_BICI = dcc.Dropdown(
    id='dropdown_months_bici',
    options=[{'label': i, 'value': i} for i in months],
    value='05',
    placeholder='Select a month'
)

# Plot of users every month depending on year
df_new = df.groupby(['year', 'month_number', 'month']).sum().reset_index()
df_new = df_new.sort_values(['year', 'month_number'], ascending=[True, True])
fig2 = px.line(df_new, x="month", y="users", color='year')
graphusers = dcc.Graph(figure=fig2)

# plot for the map

# Plot with Z-values
'''
months = ['january', 'february', 'march', 'april', 'may', 'june']

df_new3 = df.loc[df['month'].isin(months)]
df_new3 = df_new3.groupby(['year', 'month_number', 'month']).sum().reset_index()

std = df_new3.groupby(['month_number', 'month'])['users'].std().reset_index()
mean = df_new3.groupby(['month_number', 'month'])['users'].mean().reset_index()

df_2020 = df_new3[df_new3['year'] == 2020]
df_out = (df_2020.set_index(['month_number', 'month']) - mean.set_index(['month_number', 'month'])).reset_index()
df_out = (df_out.set_index(['month_number', 'month']) / std.set_index(['month_number', 'month'])).reset_index()

fiz_zscore = px.bar(df_out, x="month", y="users")
'''
# collapse info utilizaciones entradas

collapse_info = [
    dbc.Button(
        "INFO",
        id="collapse-button",
        className="mb-3",
        color="secondary",
        outline=True
    ),
    dbc.Collapse(
        dbc.Card(
            dbc.CardBody(
                html.P(
                    dcc.Markdown(dedent(
                        '''**Entradas** es el número de entradas por las barreras de peaje de los vestibulos de cada estación.
                        __Utilizaciones__ es el número de movimientos por el interior de una estación (entradas, salidas y transbordos)'''
                    )), className="card-text",
                ),
            )
        ),
        id="collapse",
    )
]

# LAYOUT
layout = html.Div((

    dbc.Row(
        dbc.Col(
            html.H1("City Observatory", style={'color': 'grey'})
        ), style={'margin-bottom': '10px'}
    ),
    dbc.Row(
        dbc.Col([

            dcc.Markdown('''
El reto “Aplana la curva” pretende dar respuesta al problema que supone recuperar la movilidad en la ciudad mientras convivimos con la pandemia. Este reto tiene dos objetivos: reducir la movilidad total respecto al flujo normal y aplanar las horas puntas con una distribución a lo largo de un intervalo de tiempo mayor. Para poder lograr estos retos los actores públicos y privados deben colaborar.

Esta es la primera entrega de una serie de *documentos interactivos digitales* que pretende apoyar la toma decisiones y creación de conocimiento compartido respecto a los retos de las ciudades. Este primer número está enfocado al reto de reducir la movilidad total. Este documento está construido con datos disponibles en el portal de datos de Metro de Madrid.

La reducción de flujos en el transporte tiene que ser entendido desde la heterogeneidad geográfica de estos flujos. Una primera visión global nos muestra cómo la reducción del flujo de personas en el Metro afecta más a unas paradas que otras. Esta representación es clave para poder relacionar factores urbanísticos y socio-económicos de las ciudades como mostraremos en números posteriores
''')
        ])
    ),
    html.Hr(),
    dbc.Row(
        dbc.Col(
            html.H5('Uso estaciones')
        )
    ),
    dbc.Row([
        dbc.Col(
            collapse_info,
            width=4),

        dbc.Col(dropdown_years_map),
        dbc.Col(dropdown_tipo_map),
    ], style={'margin-bottom': '5px'}
    ),

    dbc.Row([

        dbc.Col(
            dcc.Graph(id='mapgraph')

        )
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H5('Lineas Metro / mes')
        )

    ]),
    dbc.Row([

        dbc.Col(html.P(['Año' + ":", dropdown_lines]), width=2),

    ]),
    dbc.Row([

        dbc.Col(
            dcc.Graph(id="line-graph", style={"width": "100%", "display": "inline-block"}), width=9
        ),
        dbc.Col(
            dcc.Markdown('''
            La heterogeneidad del uso del transporte también se traduce en un uso desigual de cada línea de metro. Esto es relevante porque cada línea conecta puntos de la ciudad que tienen igualmente sus características socio-económicas. 
            Por ejemplo, puede haber líneas que no reducen tanto su flujo porque la gente que vive conectada por esa línea no puede cambiar su horario laboral o teletrabajar. 
            
            En próximos números investigaremos la actividad económica asociada a cada línea para ofrecer más detalles. Una información desagregada por líneas puede servir para diseñar acciones concretas para alcanzar los retos de “Aplana la curva”

            '''),
            width=3,
            style={'margin-top': '25px'}
        ),
    ]),
    html.Hr(),
    dbc.Row(
        dbc.Col(
            html.H5('Usuarios metro anual')
        )
    ),

    dbc.Row([
        dbc.Col(
            dcc.Markdown('''
            Finalmente, el flujo agregado comparado con años anteriores nos ofrece un indicador directo de la reducción total del flujo de personas. 
            
            El impacto del confinamiento y el COVID-19 en el uso del Metro es claro y desde Mayo se observa una recuperación con velocidad creciente. 
            Sin embargo la estacionalidad modula esta recuperación y hasta Septiembre no podremos observar la recuperación del transporte público con fines laborales. 
            La velocidad de cambio va a ser un parámetro clave para entender dinámicamente como la evolución epidemiológica y la medidas de distanciamiento van a afectar a los flujos en el transporte.


            '''),
            width=3,
            style={'margin-top': '35px'}
        ),
        dbc.Col(
            dcc.Graph(figure=fig2, style={"width": "100%", "display": "inline-block"}),
            width=9

        )
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H4('Uso biciMAD')
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.P(
                ['Para el año 2020 seleccione un mes' + ":", dropdown_months_BICI]
            )
            , width=3),
    ]),

    dbc.Row([

        dbc.Col(
            dcc.Graph(id='histogram-bike-graph')
        )
    ]),

    html.Hr(),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='sankey-bike-graph')
        )
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col(
            html.H4('Conclusiones'),
            width=2
        ),

    ]),

    dbc.Row([

        dbc.Col([
            dcc.Markdown('''
            * Este documento es una primera entrega de una serie de documentos interactivos que apoyen el reto “Aplana la curva” y generen conocimiento compartido
            
            * Los datos actuales tienen un nivel de agregación “grueso” y es necesario generar otros tipos de agregaciones para llegar a más conclusiones y tratar otros retos como el del aplanamiento de la hora punta
            
            * El uso de Metro no se ha recuperado del impacto del COVID-19 y del confinamiento y tendremos que esperar a Septiembre y posibles nuevas medidas o brotes para poder abordar los retos que suponen el uso del transporte para recuperar actividad laboral
            
            * La heterogeneidad geográfica del uso del transporte será clave para entender los factores sociales y económicos. La desagregación por líneas es el primer paso para establecer un mapeo a nivel de ciudad y tomar medidas concretas y efectivas
            
            * Este análisis será enriquecido con otras fuentes de datos de transporte ya que el análisis debe ser multimodal en cuanto a medios de transporte. Así mismo el uso de fuentes de Big Data para medir movilidad como los datos de móviles será clave para entender las relaciones entre movilidad mediante transporte público y privado
                      
            
            '''),
            html.P(['Para más información escribira ', html.A('r.fbenito@upm.es', href='mailto:r.fbenito@upm.es')])

        ])
    ], style={'margin-bottom': '30px'}),
    html.Hr(),

    dbc.Row([

        dbc.Col(
            html.Iframe(
                id="JotFormIFrame-202503869763361",
                title="Ciudadanía - Compromiso y manifiesto",
                # onload="window.parent.scrollTo(0,0)",
                # allowtransparency="true",
                # allowfullscreen="true",
                # allow="geolocation; microphone; camera",
                src="https://form.jotform.com/202572649501050",
                height=950,
                width= 700
                # frameborder="0",
                #style={#"width": "100%;",
                       #"height": "539px;",
                      # "border": "none;",
                #       "scrolling": "no"}
            ),
            style={'margin-bottom':'30px',
                   #'margin-left':'20px',
                   'border-widht':'1px'}
        )

    ])
),
    style={'margin-left': '10px', 'margin-right': '10px'})


@app.callback(
    Output('mapgraph', 'figure'),
    [Input('dropdown_tipo_map', 'value'),
     Input('dropdown_years_map', 'value')])
def map_figure(v_tipo, v_year):
    value = str(v_tipo) + '_' + str(v_year)
    df3 = df2[['name_Est', 'long', 'lat', value]]
    fig4 = px.scatter_mapbox(df3, lat="lat", lon="long", hover_name="name_Est", hover_data=["name_Est", value],
                             color_discrete_sequence=["blue"], zoom=10, height=500, size=value)
    fig4.update_layout(mapbox_style="light", mapbox_accesstoken=token)
    fig4.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig4


# plot months vs total users selecting year
@app.callback(
    Output("line-graph", "figure"), [Input('dropdown_lines', "value")])
def line_figure(year):
    df1 = df.loc[df['year'] == year]
    figure = px.line(df1, x="month", y="users", color='line', color_discrete_map={
        "1": "lightblue",
        "2": "red",
        "3": "yellow",
        "4": "brown",
        "5": "lightgreen",
        "6": "grey",
        "7": "orange",
        "8": "pink",
        "9": "purple",
        "10": "blue",
        "11": "green",
        "12": "olive",
        "R": "black"}
                     )
    figure.update_traces(mode="markers+lines", hovertemplate=None)

    return figure


# Callbacks para los collapse (INFO utilizacioens estaciones)
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("histogram-bike-graph", 'figure'),
    [Input('dropdown_months_bici', 'value')]
)
def hist_bike_figure(month):
    fig_hist = paintBikeTravelsEveryHour('2020', month)
    return fig_hist


@app.callback(
    Output('sankey-bike-graph', 'figure'),
    [Input('dropdown_months_bici', 'value')]
)
def sankey_bike_figure(month):
    fig_sankey = paintBikeTravelsSankey('2020', month)
    return fig_sankey
