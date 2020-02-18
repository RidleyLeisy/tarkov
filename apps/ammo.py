import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import pandas as pd
import dash_bootstrap_components as dbc

from app import app



df = pd.read_csv('init.csv')

caliber_types = df['Caliber'].unique()
dimensions = ['Flesh Damage','Penetration Power','Armor Damage (%)','Accuracy (%)','Recoil (%)','Fragmentation Chance (%)']

layout = (dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Ammo", href="/ammo")),
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Gun", href="/gun")),
        ],
        brand="NavbarSimple",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    html.H1(children='Ammo Analyzer',style={'text-align':'center'}),
    
    html.Div(children=[
        html.Label('Multi-Select Dropdown'),
    
    # filters for ammo graph
    html.Div([
        html.Div([  
            dcc.Dropdown(
            id='ammo-dimension',
            options=[{'label': i, 'value': i} for i in dimensions],
            multi=False,
            value='Armor Damage (%)'
        ),  
            dcc.Dropdown(
            id='ammo-type',
            options=[{'label': i, 'value': i} for i in caliber_types],
            multi=True,
            value=['12/70 slugs']
        ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ]),
    # ammo graph
    html.Div([
        dcc.Graph(
            id='ammo-selector', 
            figure= {'layout':{'clickmode': 'event+select'}},
            clickData= {'points': [{'bullet_name': '12/70 FTX Custom LIte Slug'}]},
            config={'autosizable': True},
                )], 
            style={'width': '70%', 'margin': '0 auto'},
            
    ),

    html.Div([
        dcc.Markdown(d("""
            **Click Data**

            Click on points in the graph.
        """)),
        html.Pre(id='click-data', style = {
                                            'pre': {
                                                'border': 'thin lightgrey solid',
                                                'overflowX': 'scroll'
                                            }
                                        }),
    ], className='three columns'),



    dcc.Graph(
        id='ammo-pen',
        figure={

        }
    )
]))

@app.callback(
    dash.dependencies.Output('ammo-selector','figure'),
    [dash.dependencies.Input('ammo-type','value'),
    dash.dependencies.Input('ammo-dimension','value')]
)
def update_ammo(ammo_type, ammo_dimen):
    dff = df.loc[df['Caliber'].isin(ammo_type)].sort_values(by=ammo_dimen)
    return {'data': [dict(
                x = dff[ammo_dimen],
                y = dff["Bullet Name"],
                type='bar',
                orientation='h',

    )]}



@app.callback(
    Output('click-data', 'children'),
    [Input('ammo-selector', 'clickData')])
def display_click_data(clickData):
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['Current Price']

    return dff.to_json(orient='records')