import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2

####ABOUT AUTHORS

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
import plotly.express as px
import pandas as pd

layout = html.Div(
    [




        html.Div([
            html.H5('About', className='col-md-12'),

        ], className='row'),

    ]
)
