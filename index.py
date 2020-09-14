##################MULTI PAGE APP DASH ################
# Prueba de una aplicacion con diferentes paginas - implementando un menu
# Manage the different apps on different urls with the callbacks
# Entry point for running the app
# This file links up all the individual pages (it is possible to add a navigation bar that is common to the rest of files)
# Tb se puede modificar el index_string de la App que permite fijar un menu, footer, etc

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import app1, app2

app.layout = html.Div([
    html.Div([
        dbc.Navbar(
            dbc.Container([
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand("Madrid City Observatory", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/home",
                ),
                # Genera el menu con el componente de bootstrap
                dbc.Nav(
                    [
                        dbc.NavLink("City Observatory", active=True, href="/home", style={'color': 'grey'}),
                        dbc.NavLink("About", href="#", style={'color': 'grey'}),
                        dbc.NavLink(
                            html.A('Contact', href='mailto:david.pastor@upm.es'
                                   , style={'color': 'grey'}),

                        ),

                    ]
                )
            ],
                className='floating menu row', style={'max-width': '2000px'}
            ),
            color="dark",
            dark=True,
            className="mb-4",
        ),
    ], style={'padding-right': '-15px', 'padding-left': '-15px'}
    ),

    html.Hr(),

    html.Div([

        dcc.Location(id='url', refresh=False),

        html.Div(id='page-content'),
    ], className='container-fluid'
    )
]

)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return app1.layout
    if pathname == '/home':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout

    else:
        return '404'


# START THE SERVER
#server = app.server
#if __name__ == '__main__':
#    app.run_server(debug=True)
