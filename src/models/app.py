import plotly.graph_objects as go
import dash
import json
from dash import dcc
import dash_leaflet as dl
from dash import html
from dash.dependencies import Output, Input


app = dash.Dash()
app.layout = html.Div([
    html.P("Coordinate (click on map):"),
    html.Div(id="coordinate-click-id"),
    dl.Map(id='map_id',
           style={'width': '1200px', 'height': '900px'},
           center=[45.5416889, -73.667256], zoom=11,
           children=[
               dl.TileLayer()
           ]
           ),
])


@app.callback(Output("coordinate-click-id", 'children'),
              [Input("map_id", 'click_lat_lng')])
def click_coord(e):
    if e is not None:
        return json.dumps(e)
    else:
        return "-"


if __name__ == '__main__':
    app.run_server(port='8052', debug=True, use_reloader=False)