import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pyo
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

"""
Dash app
"""
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    dbc.Row(
        [dbc.Col(html.H3("TESTING"))],
    ),
    dbc.Row(
        [dbc.Col(dcc.Dropdown("First col"),
                 style={'text-align': 'center'}),
         dbc.Col(dcc.Dropdown('second col'),
                 width=2,
                 style={'text-align': 'center'}),
         dbc.Col(dcc.Dropdown('third col'),
                 width=2,
                 style={'text-align': 'center'})
         ],
    )
]
)

# Add the server clause:
if __name__ == '__main__':
    app.run_server()
