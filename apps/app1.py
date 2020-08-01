import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go

from app import app
from apps import app1, app2

##############LOAD DATA
df = pd.read_csv('./data/metro_data_fin.csv')
years = df['year'].unique()

# Data for the map
df2 = pd.read_csv('./data/mapas_metro')
data = "Ent_2019"

data_options = ['Ent_2014', 'Util_2014', 'Ent_2015', 'Util_2015', 'Ent_2016',
                'Util_2016', 'Ent_2017', 'Util_2017', 'Ent_2018', 'Util_2018',
                'Ent_2019', 'Util_2019']

dropdown_map = dcc.Dropdown(
    id='dropdown_map',
    options=[{'label': i, 'value': i} for i in data_options],
    value='Util_2019',
)

# Token for mapbox
token = 'pk.eyJ1IjoiY3RhcmF6b25hIiwiYSI6ImNrZDkxcW1sYjBwOWkycnM4NDRpbXViYnYifQ.jK8gChNK_dzVpKlrKKfJgA'

dropdown = dcc.Dropdown(
    id='dropdown_',
    options=[{'label': i, 'value': i} for i in years],
    value=2019,
    placeholder='Select a year'
)
# Plot of users every month depending on year
df_new = df.groupby(['year', 'month_number', 'month']).sum().reset_index()
df_new = df_new.sort_values(['year', 'month_number'], ascending=[True, True])
fig2 = px.line(df_new, x="month", y="users", color='year')
graphusers = dcc.Graph(figure=fig2)

# plot for the map

#Plot with Z-values

months = ['january', 'february', 'march', 'april', 'may', 'june']

df_new3 = df.loc[df['month'].isin(months)]
df_new3 = df_new3.groupby(['year', 'month_number', 'month']).sum().reset_index()

std = df_new3.groupby(['month_number', 'month'])['users'].std().reset_index()
mean = df_new3.groupby(['month_number', 'month'])['users'].mean().reset_index()

df_2020 = df_new3[df_new3['year'] == 2020]
df_out = (df_2020.set_index(['month_number', 'month']) - mean.set_index(['month_number', 'month'])).reset_index()
df_out = (df_out.set_index(['month_number', 'month']) / std.set_index(['month_number', 'month'])).reset_index()

fig5 = px.bar(df_out, x="month", y="users")

#LAYOUT
layout = html.Div((

    dbc.Row(
        dbc.Col(
            html.H1("City Observatory", style={'color': 'grey'})
        ), style={'margin-bottom': '10px'}
    ),

    dbc.Row(
        dbc.Col(
            html.H5('Uso estaciones')
        )
    ),
    dbc.Row([

        dbc.Col(html.P(['Año y Entrada/Utilización' + ":", dropdown_map]), width=2),
        dbc.Col([

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
                            "<b>Entradas</b> es el número de entradas por las barreras de peaje de los vestibulos de cada estación. "
                            "Utilizaciones> es el número de movimientos por el interior de una estación (entradas, salidas y transbordos",
                            className="card-text",
                        ),

                    )
                ),
                id="collapse",
            )],
            width=4)
    ], style={'margin-bottom': '5px'}),
    dbc.Row([

        dbc.Col(
            dcc.Graph(id='mapgraph')

        )
    ]),
    html.Hr(),
    dbc.Row(
        dbc.Col(
            html.H5('Lineas Metro / mes')
        )
    ),
    dbc.Row([

        dbc.Col(html.P(['Año' + ":", dropdown]), width=2),
        dbc.Col(
            dcc.Graph(id="line-graph", style={"width": "100%", "display": "inline-block"})
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
            dcc.Graph(figure=fig2, style={"width": "100%", "display": "inline-block"})

        )
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H5('z-score'),
            width= 2
        ),
        dbc.Col([

            dbc.Button(
                "Z-SCORE INFO",
                id="collapse-button-z",
                className="mb-3",
                color="secondary",
                outline=True
            ),
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        html.P(
                            "Desviación sobre la línea base (mismo mes durante 5 años) ",
                            className="card-text",
                        ),

                    )
                ),
                id="collapse-z",
            )],
            width=4)
    ]),
    dbc.Row([

        dbc.Col(
            dcc.Graph(figure=fig5, style={"width": "100%", "display": "inline-block"})

        )
    ])
),
    style={'margin-left': '10px', 'margin-right': '10px'})


@app.callback(
    Output('mapgraph', 'figure'),
    [Input('dropdown_map', 'value')])
def map_figure(value):
    df3 = df2[['name_Est', 'long', 'lat', value]]
    fig4 = px.scatter_mapbox(df3, lat="lat", lon="long", hover_name="name_Est", hover_data=["name_Est", value],
                             color_discrete_sequence=["blue"], zoom=10, height=500, size=value)
    fig4.update_layout(mapbox_style="light", mapbox_accesstoken=token)
    fig4.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig4


# '''plot months vs total users selecting year'''
@app.callback(
    Output("line-graph", "figure"), [Input('dropdown_', "value")])
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
    return figure

#Callbacks para los collapse (INFO utilizacioens estaciones)
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#Collapse callback z-score
@app.callback(
    Output("collapse-z", "is_open"),
    [Input("collapse-button-z", "n_clicks")],
    [State("collapse-z", "is_open")],
)
def toggle_collapse_z(n, is_open):
    if n:
        return not is_open
    return is_open
