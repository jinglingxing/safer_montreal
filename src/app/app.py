import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import dash_leaflet as dl
from typing import List, Tuple

from src.algorithm.a_star import AStar
from src.algorithm.model import Model
from src.features.preprocessing_graph import load_or_process_graph

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)
server = app.server

button = html.Div([
        dbc.Button("Reset", id="reset_val", className="me-2", n_clicks=0)
    ])

ps_button = html.Div([
        dbc.Button("Police Stations", id="ps_button_val", className="me-2", n_clicks=0)
    ])

fs_button = html.Div([
        dbc.Button("Fire Stations", id="fs_button_val", className="me-2", n_clicks=0)
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
                                   dl.LayerGroup(id="layer"),
                                   dl.LayerGroup(id="police_layer"),
                                   dl.LayerGroup(id="fire_layer"),
                                   dl.LayerGroup(id="path_layer")
                               ]
                               ), md=8),
                dbc.Col(
                    dbc.Row([
                        button, ps_button, fs_button
                    ]),
                    md=4)
            ],
            align="center",
        ),
        dcc.Store(id='departure'),
        dcc.Store(id='destination')
    ],
    fluid=True,
)


def plot_path(path: List[Tuple[float, float]]):
    polyline = dl.Polyline(positions=path)
    patterns = [
        dict(offset='100%', repeat='0', arrowHead=dict(pixelSize=15, polygon=False, pathOptions=dict(stroke=True)))]
    arrow = dl.PolylineDecorator(children=polyline, patterns=patterns)
    return arrow

icon_core = {
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "iconAnchor": [12, 41],
    "popupAnchor": [1, 20],
    "shadowSize": [41, 41]
}

icon_dep = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-gold.png',
    "shadowUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-black.png',
    **icon_core
}

icon_dest = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    "shadowUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-black.png',
    **icon_core
}

icon_ps = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    "shadowUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-black.png',
    **icon_core
}

icon_fs = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    "shadowUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-black.png',
    **icon_core
}

@app.callback(Output(component_id="layer", component_property='children'),
              [Input(component_id='departure', component_property='data'),
               Input(component_id='destination', component_property='data')])
def create_markers(departure, destination):
    res = [None, None]

    if departure is not None:
        res[0] = dl.Marker(position=departure,
                           icon=icon_dep,
                           children=dl.Tooltip("Departure: ({:.3f}, {:.3f})".format(*departure)))
    if destination is not None:
        res[1] = dl.Marker(position=destination,
                           icon=icon_dest,
                           children=dl.Tooltip("Destination: ({:.3f}, {:.3f})".format(*destination)))

    return res


@app.callback(Output(component_id="departure", component_property='data'),
              Output(component_id="destination", component_property='data'),
              [Input(component_id="map_id", component_property='click_lat_lng'),
               Input(component_id='departure', component_property='data'),
               Input(component_id='destination', component_property='data')])
def click_coord(click_lat_lng, departure, destination):
    if click_lat_lng is None:
        return None, None
    else:
        if departure is None:
            departure = click_lat_lng
        else:
            destination = click_lat_lng
    return departure, destination


@app.callback(Output(component_id='map_id', component_property='click_lat_lng'),
              [Input(component_id='reset_val', component_property='n_clicks')])
def reset_button(_):
    return None

graph = load_or_process_graph('model/preprocessed_map_graph.json')
model = Model('model/decision_tree_model.pkl',
              'model/best_nn.h5',
              'model/DT_MinMaxScaler.pkl',
              'model/NN_MinMaxScaler.pkl',
              'model/OneHotEncodingScaler.pkl')
a_star = AStar(graph, model)

@app.callback(Output(component_id='path_layer', component_property='children'),
              [Input(component_id='departure', component_property='data'),
               Input(component_id='destination', component_property='data')])
def display_path(departure, destination):
    if departure is None or destination is None:
        return plot_path([])
    return plot_path(a_star.get_path(departure, destination))

@app.callback(Output(component_id='police_layer', component_property='children'),
            [Input(component_id='ps_button_val', component_property='n_clicks')])
def police_stations(n):
    res = []
    if n % 2 != 0:
        res = [dl.Marker(position=ps,
                           icon=icon_ps,
                           children=dl.Tooltip("Police Station: ({:.3f}, {:.3f})".format(*ps)))
               for ps in graph.get_police_stations_coordinates()]
    return res

@app.callback(Output(component_id='fire_layer', component_property='children'),
            [Input(component_id='fs_button_val', component_property='n_clicks')])
def fire_stations(n):
    res = []
    if n % 2 != 0:
        res = [dl.Marker(position=fs,
                           icon=icon_fs,
                           children=dl.Tooltip("Fire Station: ({:.3f}, {:.3f})".format(*fs)))
               for fs in graph.get_fire_stations_coordinates()]
    return res


print("app is running")

if __name__ == "__main__":
    app.run_server(port='8053', debug=True, use_reloader=False)