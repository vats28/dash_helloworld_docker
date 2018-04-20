import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import flask
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Tesla', 'value': 'tsla'},
            {'label': 'Apple', 'value': 'aapl'},
            {'label': 'Coke', 'value': 'coke'}
        ],
        value='tsla'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = web.DataReader(str(selected_dropdown_value),
                        data_source='morningstar',
                        start=dt(2015, 1, 1),
                        end=dt(2018, 1, 1)).reset_index()
    return {
        'data': [{
            'x': df.Date,
            'y': df.Close,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }

app.css.append_css({
    'external_url': (
	'https://cdn.rawgit.com/plotly/dash-app-stylesheets/96e31642502632e86727652cf0ed65160a57497f/dash-hello-world.css'
    )
})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


if __name__ == '__main__':
    app.run_server()
