import os

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import tools
import plotly.graph_objs as go

from src.components.dataPokemon import dfPokemon, dfPokemonTable, dfHistory

from src.components.tab1.view import renderIsiTab1
from src.components.tab2.view import renderIsiTab2
from src.components.tab3.view import renderIsiTab3
from src.components.tab4.view import renderIsiTab4
from src.components.tab5.view import renderIsiTab5
from src.components.tab6.view import renderIsiTab6
from src.components.tab7.view import renderIsiTab7

from src.components.tab1.callbacks import callbackSortingTable, callbackFilterTable
from src.components.tab2.callbacks import callbackUpdateCatGraph
from src.components.tab3.callbacks import callbackUpdateScatterGraph
from src.components.tab4.callbacks import classUpdatePieChart
from src.components.tab5.callbacks import callbackUpdateHisto
from src.components.tab6.callbacks import callbackPredict
from src.components.tab7.callbacks import callbackSortingTableHistory, callbackFilterTableHistory

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

server=app.server

app.title='Dashboard Pokemon'

app.layout = html.Div([
        html.H1('Dashboard Pokemon'),
        html.H3('''
                Created by: Brane Warren
                '''),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Pokemon', value='tab-1', children = renderIsiTab1()),
        dcc.Tab(label='Categorical Plots', value='tab-2',children = renderIsiTab2()),
        dcc.Tab(label='Scatter Plot', value='tab-3', children = renderIsiTab3()),
        dcc.Tab(label='Pie Chart', value='tab-4', children = renderIsiTab4()),
        dcc.Tab(label='Histogram', value='tab-5', children = renderIsiTab5()),
        dcc.Tab(label='Test Predict', value='tab-6', children = renderIsiTab6()),
        dcc.Tab(label='History Prediction', value='tab-7', children = renderIsiTab7()),
    ],style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily':'Arial',
        'borderBottom' : '1px solid #d6d6d6',
        'borderLeft' : '1px solid #d6d6d6',
        'borderRight' : '1px solid #d6d6d6',
        'padding' : '44px'
    })
], style={
    'maxWidth' : '1200px',
    'margin' : '0 auto'
})

# Tabel Canggih
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "pagination_settings"),
     Input('table-multicol-sorting', "sorting_settings")])
def update_sort_paging_table(pagination_settings, sorting_settings):
    return callbackSortingTable(pagination_settings, sorting_settings)

# Tabel
@app.callback(
    Output(component_id='tablediv', component_property='children'),
    [Input('buttonsearch', 'n_clicks'),
    Input('filterrowstable', 'value')],
    [State('filternametable', 'value'),
    State('filtergenerationtable', 'value'),
    State('filtercategorytable', 'value'),
    State('filtertotaltable', 'value')])
def update_table(n_clicks,maxrows,name,generation,category,total):
    return callbackFilterTable(n_clicks,maxrows,name,generation,category,total)

# Plots
@app.callback(
    Output(component_id='categoryGraph', component_property='figure'),
    [Input(component_id='jenisplotcategory', component_property='value'),
    Input(component_id='xplotcategory', component_property='value'),
    Input(component_id='yplotcategory', component_property='value'),
    Input(component_id='statsplotcategory', component_property='value')])
def update_category_graph(jenisplot, xplot, yplot, statsplot):
    return callbackUpdateCatGraph(jenisplot, xplot, yplot, statsplot)

# Jenis Plot
@app.callback(
    Output(component_id='statsplotcategory', component_property='disabled'),
    [Input(component_id='jenisplotcategory', component_property='value')])
def update_disabled_stats(jenisplot):
    if jenisplot=='Bar':
        return False
    return True

# Scatter Plot
@app.callback(
    Output(component_id='scattergraph', component_property='figure'),
    [Input(component_id='hueplotscatter', component_property='value'),
    Input(component_id='xplotscatter', component_property='value'),
    Input(component_id='yplotscatter', component_property='value')])
def update_scatter_plot(hue,x,y):
    return callbackUpdateScatterGraph(hue,x,y)

# Pie Chart
@app.callback(
    Output(component_id='piegraph', component_property='figure'),
    [Input(component_id='groupplotpie', component_property='value')])
def update_pie_chart(group):
    return classUpdatePieChart(group)

# Histogram
@app.callback(
    Output(component_id='histograph', component_property='figure'),
    [Input(component_id='xplothist', component_property='value'),
    Input(component_id='hueplothist', component_property='value'),
    Input(component_id='stdplothist', component_property='value')])
def update_histo(xx,hue,angka):
    return callbackUpdateHisto(xx,hue,angka)


# Predict
@app.callback(
    Output(component_id='outputpredict', component_property='children'),
    [Input('buttonpredict', 'n_clicks')],
    [State('predictname', 'value'),
    State('predicttype1', 'value'),
    State('predicttype2', 'value'),
    State('predictgeneration', 'value'),
    State('predicttotal', 'value'),
    State('predicthp', 'value'),
    State('predictspeed', 'value'),
    State('predictattack', 'value'),
    State('predictdefense', 'value'),
    State('predictspattack', 'value'),
    State('predictspdefense', 'value'),
    ])
def predict(n_clicks, name, type1, type2, generation, total,hp, speed, attack, defense, spatk, spdef):
    return callbackPredict(n_clicks, name, type1, type2, generation, total,hp, speed, attack, defense, spatk, spdef)

# History
@app.callback(
    Output('table-history-prediction', "data"),
    [Input('table-history-prediction', "pagination_settings"),
     Input('table-history-prediction', "sorting_settings")])
def update_sort_paging_table_history(pagination_settings, sorting_settings):
    return callbackSortingTableHistory(pagination_settings, sorting_settings)

@app.callback(
    Output(component_id='tablehistorydiv', component_property='children'),
    [Input('filtercreatedbyhistory', 'value'),
    Input('filterrowshistory', 'value')],
    )
def update_table_history(createdby, maxrows):
    return callbackFilterTableHistory(createdby, maxrows)

if __name__ == '__main__':
    app.run_server(debug=True)