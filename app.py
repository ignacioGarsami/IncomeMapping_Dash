import utils
import os
import dash
import dash_bootstrap_components as dbc # import the library
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State
import json
import pandas as pd
import numpy as np




data_map = utils.data_handler()

os.remove("kaggle_income.csv.zip")

states = data_map['State_Name'].unique()
counties = data_map['County'].unique()
incomes = data_map['Mean'].unique()


bins = [
    0,
    25000,
    50000,
    100000,
    150000,
    200000,
    250000,       
]

data_map['Scale'] = "#ff0000"

data_map.loc[data_map['Mean'] > 25000, 'Scale'] = "#00de9a"
data_map.loc[data_map['Mean'] > 50000, 'Scale'] = "#00cb8c"
data_map.loc[data_map['Mean'] > 100000, 'Scale'] = "#007c56"
data_map.loc[data_map['Mean'] > 150000, 'Scale'] = "#00553b"
data_map.loc[data_map['Mean'] > 200000, 'Scale'] = "#00412d"
data_map.loc[data_map['Mean'] > 250000, 'Scale'] = "#001a12"


scale = [
    "#ff0000",
    "#00de9a",
    "#00cb8c",
    "#007c56",
    "#00553b",
    "#00412d",
    "#001a12",
]

#def generate_table(dataframe, max_rows=10):
#    return html.Table(
#        # Header
#        [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#        # Body
#        [html.Tr(
#            [html.Td(row[col]) for col in row.index.values]
#        ) for index, row in dataframe.head(max_rows).iterrows()]
#    )
#

#load the app with the Bootstrap css theme
#external_stylesheets = [dbc.themes.BOOTSTRAP]
external_stylesheets = [dbc.themes.LUX]
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
 
app.title = 'IncomeMapping in the USA'

#colors = {
#    'background': 'lightgray',
#    'text': '#7FDBFF'
#}

markdown_text = '''
#### Some references
[Dash Core Components](https://dash.plot.ly/dash-core-components)  
[Dash HTML Components](https://dash.plot.ly/dash-html-components)  
[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/l/components)  
'''
DEFAULT_OPACITY = 0.8

mapbox_access_token = "pk.eyJ1IjoiaWduYWNpb2dhcmMiLCJhIjoiY2s4aDdqNWVvMDF5aTNncG40bTEyMmwxdSJ9.khtjUesTo8hGuFb3x-1n9w"
mapbox_style = "mapbox://styles/ignaciogarc/ck8h7mfze13fi1ioi6zw69s5b"

# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            style={'textAlign': 'center'},
            children=[
                html.H4(children="Mean income in the USA"),
            ],
        ),
        dcc.Tabs([
                dcc.Tab(label = 'Data visualization', children = [      
                  html.Div(
                    id="app-container",
                    children=[
                        html.Div(
                            id="left-column",
                            children=[
                                html.Div(
                                    id="slider-container",
                                    children=[
                                        html.H5(
                                            id="slider-text",
                                            children="Select state to visualize:",
                                        ),
                                        dcc.Dropdown(
                                            style = {'width':'33%', 'padding': 2 },
                                            id="state-select",
                                            options=[{"label": i, "value": i} for i in states],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="heatmap-container",
                                    style={'textAlign': 'center'},
                                    children=[
                                        html.H5(
                                            "Heatmap of income by city"
                                            ),        
                                        dcc.Graph(
                                            id="county-choropleth",
                                            figure=dict(
                                                data=[
                                                    dict(
                                                        lat=data_map["Lat"],
                                                        lon=data_map["Lon"],    
                                                        hovertext = [["State: {} <br>County: {} <br>City: {} <br>Mean income: {}".format(i,j,v,w)]
                                                            for i,j,v,w in zip(data_map['State_Name'], data_map['County'], data_map['City'], data_map['Mean'])],
                                                        hoverinfo="text",
                                                        marker=dict(size= 6, color= data_map['Scale'], opacity=7),
                                                        type="scattermapbox",
                                                    )
                                                ],
                                                layout=dict(
                                                    mapbox=dict(
                                                        layers=[],
                                                        accesstoken=mapbox_access_token,
                                                        style=mapbox_style,
                                                        center=dict(
                                                            lat=38.72490, lon=-95.61446
                                                        ),
                                                        pitch=0,
                                                        zoom=3.5,
                                                    ),
                                                    autosize=True,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
        # =============================================================================
                         html.Div(
                             id="graph-container",
                             children=[
                                 html.H5(id="chart-selector", style = {'padding' : 2},  children="Select chart to visualize:"),
                                 dcc.Dropdown(
                                     style = {'width':'60%', 'padding': 2},
                                     options=[
                                         {
                                             "label": "Income mean by city in the selected State (Aggregated by ZIP Codes)",
                                             "value": "barplot",
                                         },
                                         {
                                             "label": "Income std deviation by city in the selected State (Aggregated by ZIP Codes)",
                                             "value": "barplot_std",
                                         },
                                        {
                                             "label": "Income median by city in the selected State (Aggregated by ZIP Codes)",
                                             "value": "barplot_med",
                                         }
                                     ],
                                     value="barplot",
                                     id="chart-dropdown",
                                 ),
                                 dcc.Graph(
                                     id="selected-data",
                                     figure=dict(
                                         data=[dict(x=0, y=0)],
                                         layout=dict(
                                             paper_bgcolor="#F4F4F8",
                                             plot_bgcolor="#F4F4F8",
                                             autofill=True,
                                             margin=dict(t=75, r=50, b=100, l=50),
                                         ),
                                     ),
                                 ),
                             ],
                         ),
        # =============================================================================
                    ],
                ),       
                ]),
                dcc.Tab(label = 'Raw data', children = [
                        #Here its supossed to be the raw table to explore the data
                ])
        ])

    ],
)
                                        

                        

@app.callback(
    Output("county-choropleth", "figure"),
    [Input("state-select", "value")],
    [State("county-choropleth", "figure")],
)
def display_map(value, figure):
    cm = dict(zip(bins, scale))
    if value is None:
        dff = data_map
    else:
        dff = data_map[data_map["State_Name"] == value]
    
    data = [
        dict(
            lat=dff["Lat"],
            lon=dff["Lon"],
            hovertext = [["State: {} <br>County: {} <br>City: {} <br>Mean income: {}".format(i,j,v,w)]
                                for i,j,v,w in zip(dff['State_Name'], dff['County'], dff['City'], dff['Mean'])],
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=6, color=dff['Scale'], opacity=7),
        )
    ]

    annotations = [
        dict(
            showarrow=False,
            align="right",
            text="<b>Mean income by city</b>",
            font=dict(color="#2cfec1"),
            bgcolor="#1f2630",
            x=0.95,
            y=0.95,
        )
    ]

    for i, bin in enumerate(reversed(bins)):
        color = cm[bin]
        annotations.append(
            dict(
                arrowcolor=color,
                text=bin,
                x=0.95,
                y=0.85 - (i / 20),
                ax=-60,
                ay=0,
                arrowwidth=5,
                arrowhead=0,
                bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
            )
        )

    if "layout" in figure:
        lat = figure["layout"]["mapbox"]["center"]["lat"]
        lon = figure["layout"]["mapbox"]["center"]["lon"]
        zoom = figure["layout"]["mapbox"]["zoom"]
    else:
        lat = (38.72490,)
        lon = (-95.61446,)
        zoom = 3.5

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(lat=lat, lon=lon),
            zoom=zoom,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=annotations,
        dragmode="lasso",
    )

    fig = dict(data=data, layout=layout)
    return fig



@app.callback(
    Output("selected-data", "figure"),
    [
        Input("chart-dropdown", "value"),
        Input("state-select", "value"),
    ],
)
def display_selected_data(chart_dropdown, state):

    dff = data_map[data_map["State_Name"] == state]
    dff = dff.sort_values("Mean")

    
    if chart_dropdown == 'barplot':
    
        fig = go.Figure([go.Bar(x=dff['City'], y=dff['Mean'])])
    
    elif chart_dropdown == 'barplot_std':
        
        fig = go.Figure([go.Bar(x=dff['City'], y=dff['Stdev'])])
    
    else:
        
        fig = go.Figure([go.Bar(x=dff['City'], y=dff['Median'])])

    fig_layout = fig["layout"]
    fig_data = fig["data"]

    fig_data[0]["text"] = dff.values.tolist()
    fig_data[0]["marker"]["color"] = "#2cfec1"
    fig_data[0]["marker"]["opacity"] = 1
    fig_data[0]["marker"]["line"]["width"] = 0
    fig_data[0]["textposition"] = "outside"
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#2cfec1"
    fig_layout["title"]["font"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["margin"]["t"] = 75
    fig_layout["margin"]["r"] = 50
    fig_layout["margin"]["b"] = 100
    fig_layout["margin"]["l"] = 50

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)