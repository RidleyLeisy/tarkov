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
    html.H1(children='Ammo Analyzer',style={'text-align':'center','backgroundColor':'#F9F9F9'}),
    
    html.Div(children=[
    
    # filters for ammo graph

    # ammo graph
    html.Div([
        
       html.Div([html.P("Filter by dimension:",className="dimen_label"),
            dcc.Dropdown(
            id='ammo-dimension',
            options=[{'label': i, 'value': i} for i in dimensions],
            multi=False,
            value='Armor Damage (%)',
            className="dcc_control"
        ),  
            html.P("Filter by Ammo Type:",className="ammo_label"),
            dcc.Dropdown(
            id='ammo-type',
            options=[{'label': i, 'value': i} for i in caliber_types],
            multi=True,
            value=['12/70 slugs'],
            className="dcc_control"
        )],className="mini_container"),

        html.Div([
            dcc.Graph(
            id='ammo-selector', 
            figure= {'layout':{'clickmode': 'event+select'}},
            clickData= {'points': [{'label': '12/70 FTX Custom LIte Slug'}]},
            config={'autosizable': True},
                )], 
            )],
            className="pretty_container ten columns"

            
    ),

        html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.P("Current Price"), html.H6(id="currentPrice")],
                        id="cPrice",
                        className="one column",
                    ),
                    html.Div(
                        [ html.P("Past 24 Hours"), html.H6(id="past24")],
                        id="24Price",
                        className="two column",
                    ),
                    html.Div(
                        [html.P("Past 7 Days"), html.H6(id="past7d")],
                        id="7d",
                        className="three column",
                    ),
                ],
                id="info-container",
                className="column container-display",
            ),
        ]),

    # html.Div([
    #     dcc.Markdown(d("""
    #         **Click Data**

    #         Click on points in the graph.
    #     """)),
    #     html.Pre(id='click-data', style = {
    #                                         'pre': {
    #                                             'border': 'thin lightgrey solid',
    #                                             'overflowX': 'scroll'
    #                                         }
    #                                     }),
    # ], className='three columns'),

],style={'backgroundColor':'#F9F9F9'}))


@app.callback(
    dash.dependencies.Output('ammo-selector','figure'),
    [dash.dependencies.Input('ammo-type','value'),
    dash.dependencies.Input('ammo-dimension','value')]
)
def update_ammo(ammo_type, ammo_dimen):
    dff = df.loc[df['Caliber'].isin(ammo_type)].sort_values(by=ammo_dimen)
    return {'data': [dict(
                x = dff["Bullet Name"],
                y = dff[ammo_dimen],
                type='bar',

    )]}


# Current Price
@app.callback(
    Output('past24', 'children'),
    [Input('ammo-selector', 'clickData')])
def display_click_data_24(clickData):
   
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['24 hour Price Diff']

    return dff.to_json(orient='records')

# 24 Hour Price
@app.callback(
    Output('past7d', 'children'),
    [Input('ammo-selector', 'clickData')])
def display_click_data_7d(clickData):
    
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['1 week Price Diff']

    return dff.to_json(orient='records')


@app.callback(
    Output('currentPrice', 'children'),
    [Input('ammo-selector', 'clickData')])
def display_click_data_c(clickData):
    
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['Current Price']

    return dff.to_json(orient='records')