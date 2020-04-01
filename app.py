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
    3000000        
]

scale = [
    "#00f2a8",
    "#00de9a",
    "#00cb8c",
    "#007c56",
    "#00553b",
    "#00412d",
    "#001a12",
    "#000705",
]


#
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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
 
app.title = 'IncomeMapping in the USA'

colors = {
    'background': 'lightgray',
    'text': '#7FDBFF'
}

markdown_text = '''
#### Some references
[Dash Core Components](https://dash.plot.ly/dash-core-components)  
[Dash HTML Components](https://dash.plot.ly/dash-html-components)  
[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/l/components)  
'''
DEFAULT_OPACITY = 0.8

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="Mean income in the USA"),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the maximum mean income:",
                                ),
                                dcc.Slider(
                                    id="income_slider",
                                    marks={
                                        bin_: {
                                            "label": str(bin_),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for bin_ in bins
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap of income by city"
                                    ),        
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=dict(
                                        data=[
                                            dict(
                                                lat=data_map["Lat"],
                                                lon=data_map["Lon"],
                                                text=data_map["Mean"],
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
#                 html.Div(
#                     id="graph-container",
#                     children=[
#                         html.P(id="chart-selector", children="Select chart:"),
#                         dcc.Dropdown(
#                             options=[
#                                 {
#                                     "label": "Box plot of mean income by State",
#                                     "value": "boxplot",
#                                 },
#                                 {
#                                     "label": "Bar plot of mean income by State",
#                                     "value": "barplot",
#                                 }
#                             ],
#                             value="barplot",
#                             id="chart-dropdown",
#                         ),
#                         dcc.Graph(
#                             id="selected-data",
#                             figure=dict(
#                                 data=[dict(x=0, y=0)],
#                                 layout=dict(
#                                     paper_bgcolor="#F4F4F8",
#                                     plot_bgcolor="#F4F4F8",
#                                     autofill=True,
#                                     margin=dict(t=75, r=50, b=100, l=50),
#                                 ),
#                             ),
#                         ),
#                     ],
#                 ),
# =============================================================================
            ],
        ),
    ],
)
                        
#def filter_dataframe(income_slider):
#    print(income_slider)
#    dff= data_map.loc[data_map['Mean'] <= income_slider[1]]
#    return dff
# 
#@app.callback(
#     Output('county-choropleth','data'),
#     [Input('income_slider','value')]
#     )
#def update_dataframe(income_slider):
#     data_map=filter_dataframe(income_slider)
#     return data_map                        



@app.callback(
    Output("county-choropleth", "figure"),
    [Input("income_slider", "value")],
    [State("county-choropleth", "figure")],
)
def display_map(income, figure):
    cm = dict(zip(bins, scale))

    data = [
        dict(
            lat=data_map["Lat"],
            lon=data_map["Lon"],
            text= dict(
                    data_map['City'],
                    data_map['Mean']
                    ),
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=5, color="white", opacity=0),
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

#    base_url = "https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/"
#    for bin in bins:
#        geo_layer = dict(
#            sourcetype="geojson",
#            source=base_url + str(income) + "/" + bin + ".geojson",
#            type="fill",
#            color=cm[bin],
#            opacity=DEFAULT_OPACITY,
#            # CHANGE THIS
#            fill=dict(outlinecolor="#afafaf"),
#        )
#        layout["mapbox"]["layers"].append(geo_layer)

    fig = dict(data=data, layout=layout)
    return fig


#
#@app.callback(
#    Output("selected-data", "figure"),
#    [
#        Input("county-choropleth", "selectedData"),
#        Input("chart-dropdown", "value"),
#        Input("years-slider", "value"),
#    ],
#)
#def display_selected_data(selectedData, chart_dropdown, state):
#    if selectedData is None:
#        return dict(
#            data=[dict(x=0, y=0)],
#            layout=dict(
#                title="Click-drag on the map to select counties",
#                paper_bgcolor="#1f2630",
#                plot_bgcolor="#1f2630",
#                font=dict(color="#2cfec1"),
#                margin=dict(t=75, r=50, b=100, l=75),
#            ),
#        )
#    pts = selectedData["points"]
#    fips = [str(pt["text"].split("<br>")[-1]) for pt in pts]
#    for i in range(len(fips)):
#        if len(fips[i]) == 4:
#            fips[i] = "0" + fips[i]
#    dff = data[data["County"].isin(fips)]
#    dff = dff.sort_values("Mean")
#
#    if chart_dropdown != "death_rate_all_time":
#        title = "Absolute deaths per county, <b>1999-2016</b>"
#        AGGREGATE_BY = "Deaths"
#        if "show_absolute_deaths_single_year" == chart_dropdown:
#            dff = dff[dff.Year == year]
#            title = "Absolute deaths per county, <b>{0}</b>".format(year)
#        elif "show_death_rate_single_year" == chart_dropdown:
#            dff = dff[dff.Year == year]
#            title = "Age-adjusted death rate per county, <b>{0}</b>".format(year)
#            AGGREGATE_BY = "Age Adjusted Rate"
#
#        dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors="coerce")
#        deaths_or_rate_by_fips = dff.groupby("County")[AGGREGATE_BY].sum()
#        deaths_or_rate_by_fips = deaths_or_rate_by_fips.sort_values()
#        # Only look at non-zero rows:
#        deaths_or_rate_by_fips = deaths_or_rate_by_fips[deaths_or_rate_by_fips > 0]
#        fig = deaths_or_rate_by_fips.iplot(
#            kind="bar", y=AGGREGATE_BY, title=title, asFigure=True
#        )
#
#        fig_layout = fig["layout"]
#        fig_data = fig["data"]
#
#        fig_data[0]["text"] = deaths_or_rate_by_fips.values.tolist()
#        fig_data[0]["marker"]["color"] = "#2cfec1"
#        fig_data[0]["marker"]["opacity"] = 1
#        fig_data[0]["marker"]["line"]["width"] = 0
#        fig_data[0]["textposition"] = "outside"
#        fig_layout["paper_bgcolor"] = "#1f2630"
#        fig_layout["plot_bgcolor"] = "#1f2630"
#        fig_layout["font"]["color"] = "#2cfec1"
#        fig_layout["title"]["font"]["color"] = "#2cfec1"
#        fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
#        fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
#        fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
#        fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
#        fig_layout["margin"]["t"] = 75
#        fig_layout["margin"]["r"] = 50
#        fig_layout["margin"]["b"] = 100
#        fig_layout["margin"]["l"] = 50
#
#        return fig
#
#    fig = dff.iplot(
#        kind="area",
#        x="Year",
#        y="Age Adjusted Rate",
#        text="County",
#        categories="County",
#        colors=[
#            "#1b9e77",
#            "#d95f02",
#            "#7570b3",
#            "#e7298a",
#            "#66a61e",
#            "#e6ab02",
#            "#a6761d",
#            "#666666",
#            "#1b9e77",
#        ],
#        vline=[year],
#        asFigure=True,
#    )
#
#    for i, trace in enumerate(fig["data"]):
#        trace["mode"] = "lines+markers"
#        trace["marker"]["size"] = 4
#        trace["marker"]["line"]["width"] = 1
#        trace["type"] = "scatter"
#        for prop in trace:
#            fig["data"][i][prop] = trace[prop]
#
#    # Only show first 500 lines
#    fig["data"] = fig["data"][0:500]
#
#    fig_layout = fig["layout"]
#
#    # See plot.ly/python/reference
#    fig_layout["yaxis"]["title"] = "Age-adjusted death rate per county per year"
#    fig_layout["xaxis"]["title"] = ""
#    fig_layout["yaxis"]["fixedrange"] = True
#    fig_layout["xaxis"]["fixedrange"] = False
#    fig_layout["hovermode"] = "closest"
#    fig_layout["title"] = "<b>{0}</b> counties selected".format(len(fips))
#    fig_layout["legend"] = dict(orientation="v")
#    fig_layout["autosize"] = True
#    fig_layout["paper_bgcolor"] = "#1f2630"
#    fig_layout["plot_bgcolor"] = "#1f2630"
#    fig_layout["font"]["color"] = "#2cfec1"
#    fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
#    fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
#    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
#    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
#
#    if len(fips) > 500:
#        fig["layout"][
#            "title"
#        ] = "Age-adjusted death rate per county per year <br>(only 1st 500 shown)"
#
#    return fig



if __name__ == "__main__":
    app.run_server(debug=True)