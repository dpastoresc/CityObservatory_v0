# Define the dash instance
# Para usar bootstrap/archivos de estilo CSS etc se añade aqui

import dash
import dash_bootstrap_components as dbc
import os

# bootstrap theme
# https://bootswatch.com/lux/
# external_stylesheets = [dbc.themes.LUX]


external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server

app.title = 'City Observatory'
server.secret_key = os.environ.get('secret_key', 'secret')

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
