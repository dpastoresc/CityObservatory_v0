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

from utils import getRootPath

from preprocess.trafico import *


# Token for mapbox
token = 'pk.eyJ1IjoiY3RhcmF6b25hIiwiYSI6ImNrZDkxcW1sYjBwOWkycnM4NDRpbXViYnYifQ.jK8gChNK_dzVpKlrKKfJgA'

#FILE que guarda los graphs de SALUD/epidemiologicos que no van en el principal (temporal mientras tanto, posibilidad de nueva pestaña)




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
    dbc.Row([
        dbc.Col(
            html.H4('Intensidad de tráfico por Zonas Básicas de Salud')
        )
    ]),

    dbc.Row([

        dbc.Col(
            dcc.Graph(figure=paintCarTrafficInZBS('intensidad'))
        )
    ]),
    html.Hr(),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H4('Casos COVID por Zonas Básicas de Salud')
        )
    ]),

    dbc.Row([

        dbc.Col(
            dcc.Graph(figure=paintCovidCasesInZBS('casos_confirmados_ultimos_14dias'))
        )
    ]),
    html.Hr(),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H4('Intensidad de metro por Zonas Básicas de Salud')
        )
    ]),

    dbc.Row([

        dbc.Col(
            dcc.Graph(figure=paintMetroUsageInZBS("Ent_2019"))
        )
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H4('Conclusiones'),
            width=2
        ),

    ]),

),
    style={'margin-left': '10px', 'margin-right': '10px'})




