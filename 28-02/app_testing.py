import dash
import dash_core_components as dcc
import dash_html_components as html
import dill
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

report = dill.load(open("temp2", "rb"))

#add styling for the plots

app.layout = html.Div([

        html.H1(children='Results',
                style={
                    'textAlign': 'center'
                }
                ),

        html.Div(children='''
        Results of the optimisation process

        The dataset that was given as an input has been processed and multiple clustering algorithms have been applied.

        The smaller the error of he performance measure the better.
        ''', style={
            'textAlign': 'center'
        }),

    html.Div([
        dcc.Graph(
                figure=report.ranks
        )],
        style={'float': 'right',
               "width" : 700}),

    html.Div([
        dcc.Dropdown(
        id = "dropdown",
        options = [
            {"label": "K-Means Clustering", "value": "KMeans"},
            {"label": "Birch  Clustering", "value": "Birch"},
            {"label": "Graph-based spectral Clustering", "value": "SpectralClustering"},
            {"label": "Graph-based affinity Clustering", "value": "AffinityPropagation"},
            {"label": "Distribution-based Mean Shift Clustering", "value": "MeanShift"},
            {"label": "Agglomerative  Clustering", "value": "AgglomerativeClustering"},
            {"label": "Density Based  Clustering", "value": "DBSCAN"},
        ],
        value = "KMeans"
    ), dcc.RadioItems(
        id = "radio-items",
        options= [
            {"label": "3D Exploratory Plot", "value": "plot3D"},
            {"label": "2D Exploratory Plot", "value": "plot2D"}
        ],
        value = "plot2D",
        labelStyle={'display': 'inline-block'}
    )], style={'float': 'middle', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
        id='scatter_plt'
    )], style = {"float": "left",
                 "width": 1000})
], style={'float': 'middle', 'display': 'inline-block'})

@app.callback(
    dash.dependencies.Output("scatter_plt", 'figure'),
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input("radio-items", "value")])

def update_output(value_drp, value_radio):
    return report.tracker[value_drp][value_radio]

if __name__ == '__main__':
    app.run_server(debug= True, host = "localhost", port = 8000)
