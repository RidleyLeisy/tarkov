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
pricing_dimensions = ['Pen Power by Price','Flesh Damage by Price']

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
    
    html.Div([
        html.H3('Tarkov Ammo Updates'),
        dbc.Row([
            dbc.Col([html.H5('Priciest Ammo'),
            html.H6(df[['Bullet Name','Current Price']].max()['Bullet Name']),
    
            ],id="pricey_num"),

            dbc.Col([html.H5('Cheapest Ammo'),
            html.H6(df[['Bullet Name','Current Price']].min()['Bullet Name']),
    
            ],id="chaep_num"),
            
            dbc.Col([html.H5('Higheset Weekly Price Increase'),
            html.H6(df[['Bullet Name','1 week Price Diff']].max()['Bullet Name']),
    
            ],id="weekly_in_num"),
            
            dbc.Col([html.H5('Lowest Weekly Price Increase'),
            html.H6(df[['Bullet Name','1 week Price Diff']].min()['Bullet Name']),
    
            ],id="weekly_de_num"),

            ]),
        ]),

    
    
    # filters for ammo graph
    # ammo graph
   
    html.Div([
       html.Div([
           html.P("Filter by dimension:",className="dimen_label"),
                dcc.Dropdown(
                id='ammo-dimension',
                options=[{'label': i, 'value': i} for i in dimensions],
                multi=True,
                value=['Flesh Damage','Penetration Power'],
                className="row container"
                        ),  
            html.P("Filter by Ammo Type:",className="ammo_label"),
                dcc.Dropdown(
                id='ammo-type',
                options=[{'label': i, 'value': i} for i in caliber_types],
                multi=True,
                value=['12/70 slugs'],
                className="row container"
                            )
        ]),
            ],className="twelve columns"),       
    

    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                id='ammo-selector-graph', 
                figure= {'layout':{'clickmode': 'event+select'}},
                clickData= {'points': [{'label': '12/70 FTX Custom LIte Slug'}]},
                
                        )
                    ],width=9,align='start'),
        dbc.Col([
            dbc.Row(
                    [html.P("Current Price"), html.H6(id="currentPrice")],
                    id="cPrice",
                    
                        ),
            dbc.Row(
                    [ html.P("Past 24 Hours"), html.H6(id="past24")],
                    id="24Price",
                   
                        ),
            dbc.Row(
                    [html.P("Past 7 Days"), html.H6(id="past7d")],
                    id="7d",
                    ),
                    
                ],align='center'),
            ])
            ]),
            
    
    # penetration by price
    html.Div([
       html.Div([
           html.P("Filter by dimension:",className="dimen_by_price"),
                dcc.Dropdown(
                id='ammo-dimension-p',
                options=[{'label': i, 'value': i} for i in pricing_dimensions],
                multi=False,
                value='Armor Damage (%)',
                className="row container"
                        ),  
            html.P("Filter by Ammo Type:",className="ammo_label_p"),
                dcc.Dropdown(
                id='ammo-type-p',
                options=[{'label': i, 'value': i} for i in caliber_types],
                multi=True,
                value=['12/70 slugs'],
                className="row container"
                            )
        ]),
        dbc.Col([
    
            dcc.Graph(
                id='ammo-price-graph', 
                figure= {'layout':{'clickmode': 'event+select'}},
                clickData= {'points': [{'label': '12/70 FTX Custom LIte Slug'}]},
                
                        )
                    ],width=9,align='start'),
            ],className="twelve columns"),
                

)




# Main graph callback
@app.callback(
    dash.dependencies.Output('ammo-selector-graph','figure'),
    [dash.dependencies.Input('ammo-type','value'),
    dash.dependencies.Input('ammo-dimension','value')]
)
def update_ammo_test(ammo_type, ammo_dimen):
    
    dic = {'data':[]}
    length = len(ammo_dimen)
    count = 0
    
    for dim in ammo_dimen:
        inside_dic = {}
        if count < length:
            dff = df.loc[df['Caliber'].isin(ammo_type)].sort_values(by=dim)
            inside_dic.update({'x': dff['Bullet Name'].values})
            inside_dic.update({'y': dff[dim].values})
            inside_dic.update({'type':'bar'})
            inside_dic.update({'name':dim})
            count+=1
        else:
            break
        dic['data'].append(inside_dic)
    return dic


# Return same ammo as first graph for pricing graph
@app.callback(
    dash.dependencies.Output('ammo-type-p','value'),
    [dash.dependencies.Input('ammo-type','value')]
)
def update_ammo_p(ammo_type):
    return ammo_type


# Price Graph
@app.callback(
    dash.dependencies.Output('ammo-price-graph','figure'),
    [dash.dependencies.Input('ammo-type-p','value'),
    dash.dependencies.Input('ammo-dimension-p','value')]
)
def create_price_graph(ammo_type_p,ammo_dimen):
    dff = df.loc[df['Caliber'].isin(ammo_type_p)].sort_values(by=ammo_dimen)
    
    data = {'data': [dict(
                x = dff[ammo_dimen],
                y = dff["Bullet Name"],
                type='bar',
                orientation='h',)]}
    return data


# 24 Price
@app.callback(
    Output('past24', 'children'),
    [Input('ammo-selector-graph', 'clickData')])
def display_click_data_24(clickData):
   
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['24 hour Price Diff']
    
    return dff.to_json(orient='records')

# Week Price
@app.callback(
    Output('past7d', 'children'),
    [Input('ammo-selector-graph', 'clickData')])
def display_click_data_7d(clickData):
    
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['1 week Price Diff']

    return dff.to_json(orient='records')

# Current Price
@app.callback(
    Output('currentPrice', 'children'),
    [Input('ammo-selector-graph', 'clickData')])
def display_click_data_c(clickData):
    
    bullet_name = clickData['points'][0]['label']
    dff = df.loc[df['Bullet Name'] == bullet_name]['Current Price']

    return dff.to_json(orient='records')

# Most expensive ammo
@app.callback(
    Output('pricey_num', 'value'),
)
def most_exp_ammo():
    data = df[['Bullet Name','Current Price']].max()['Bullet Name']
    return data