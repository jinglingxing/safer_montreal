from jupyter_dash import JupyterDash

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
# import settings

from dash.dependencies import Output, Input

MAP_ID = "map-id"
COORDINATE_CLICK_ID = "coordinate-click-id"

# app = dash.Dash(__name__, external_scripts=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app = JupyterDash(__name__, external_scripts=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Create layout.
app.layout = html.Div([
    html.H1("Example: Gettings coordinates from click"),
    dl.Map(id=MAP_ID, style={'width': '1000px', 'height': '500px'}, center=[32.7, -96.8], zoom=5, children=[
        dl.TileLayer()
        ]),

    html.P("Coordinate (click on map):"),
    html.Div(id=COORDINATE_CLICK_ID)

])

@app.callback(Output(COORDINATE_CLICK_ID, 'children'),
              [Input(MAP_ID, 'click_lat_lng')])
def click_coord(e):
    if e is not None:
        return json.dumps(e)
    else:
        return "-"

if __name__ == '__main__':

    app.run_server(port=8080, debug=True, mode='inline')