import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import pandas as pd

df = pd.read_csv('init.csv')

caliber_types = df['Caliber'].unique()

layout = html.Div(children=[
    html.H1(children='Ammo Analyzer'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),    

    dcc.Link('Go to Ammo', href='/ammo'),
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        id='ammo-select',
        options=[{'label': i, 'value': i} for i in caliber_types],
        value=['MTL', 'SF'],
        multi=True
    ),

    dcc.Graph(
        id='ammo-selector',
        figure={
            'data': [{
                'x': df["Bullet Name"],'y': df["Caliber"], 'type':'bar',

            }],
            'layout': {
                'title': 'Dash Data Visualization'
            }
            
        },
        style={"display": "flex", "flex-direction": "column"},
    ),

])

