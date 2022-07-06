import dash
import json
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, dcc, html
import dash_leaflet as dl
from typing import List, Tuple
import re

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)

button = html.Div([
        dbc.Button("Submit", id="submit_val", className="me-2", n_clicks=0),
        dbc.Button("Reset", id="reset_val", className="me-2", n_clicks=0)
    ])

app.layout = dbc.Container(
    [
        html.H1("Safer Montreal"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dl.Map(id='map_id',
                               style={'width': '1200px', 'height': '900px'},
                               center=[45.5416889, -73.667256], zoom=11,
                               children=[
                                   dl.TileLayer(),
                                   dl.LayerGroup(id="layer")
                               ]
                               ), md=8),
                dbc.Col(
                    dbc.Row([
                        button
                    ]),
                    md=4)
            ],
            align="center",
        ),
    ],
    fluid=True,
)


# def plot_path(path: List[Tuple[float,float]]):
#     pass

 
dep_value = None
dest_value = None


def assign_dep_dest(click_lat_lng):
    global dep_value
    global dest_value
    if dep_value is None:
        dep_value = click_lat_lng
    else:
        dest_value = click_lat_lng


def reset_dep_dest():
    global dep_value, dest_value
    dep_value = None
    dest_value = None


def create_markers():
    res = [None, None]

    if dep_value is not None:
        res[0] = dl.Marker(position=dep_value,
                      children=dl.Tooltip("Departure: ({:.3f}, {:.3f})".format(*dep_value)))
    if dest_value is not None:
        res[1] = dl.Marker(position=dest_value,
                      children=dl.Tooltip("Destination: ({:.3f}, {:.3f})".format(*dest_value)))

    return res


@app.callback(Output(component_id="layer", component_property='children'),
              [Input(component_id="map_id", component_property='click_lat_lng')])
def click_coord(click_lat_lng):
    if click_lat_lng is None:
        reset_dep_dest()
    else:
        assign_dep_dest(click_lat_lng)
    return create_markers()


@app.callback(Output(component_id='map_id', component_property='click_lat_lng'),
              [Input(component_id='reset_val', component_property='n_clicks')])
def reset_button(_):
    return None


if __name__ == "__main__":
    app.run_server(port='8053', debug=True, use_reloader=False)