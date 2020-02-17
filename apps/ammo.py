import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from app import app


df = pd.read_csv('init.csv')


layout = html.Div(children=[
    html.H1(children='Ammo Analyzer'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),    
    dcc.Link('Go to Gun', href='/gun'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [{
                'x': df["Name"], 
                'y': df["Caliber"],
            }],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])



