import os

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import tools
import plotly.graph_objs as go

from src.components.dataPokemon import dfPokemon, dfPokemonTable

from src.components.tab1.view import renderIsiTab1
from src.components.tab2.view import renderIsiTab2
from src.components.tab3.view import renderIsiTab3
from src.components.tab4.view import renderIsiTab4
from src.components.tab5.view import renderIsiTab5

from src.components.tab1.callbacks import callbacksortingtable, callbackfiltertable
from src.components.tab2.callbacks import callbackupdatecatgraph
from src.components.tab3.callbacks import callbackupdatescattergraph
from src.components.tab4.callbacks import classupdatepiechart
from src.components.tab5.callbacks import callbackupdatehisto

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
    return callbacksortingtable(pagination_settings, sorting_settings)

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
    return callbackfiltertable(n_clicks,maxrows,name,generation,category,total)

# Plots
@app.callback(
    Output(component_id='categoryGraph', component_property='figure'),
    [Input(component_id='jenisplotcategory', component_property='value'),
    Input(component_id='xplotcategory', component_property='value'),
    Input(component_id='yplotcategory', component_property='value'),
    Input(component_id='statsplotcategory', component_property='value')])
def update_category_graph(jenisplot, xplot, yplot, statsplot):
    return callbackupdatecatgraph(jenisplot, xplot, yplot, statsplot)

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
    return callbackupdatescattergraph(hue,x,y)

# Pie Chart
@app.callback(
    Output(component_id='piegraph', component_property='figure'),
    [Input(component_id='groupplotpie', component_property='value')])
def update_pie_chart(group):
    return classupdatepiechart(group)

# Histogram
rowcolhist={
    'All': {'row':1, 'col':1},
    'Legendary':{'row':1,'col':2},
    'Generation':{'row':3,'col':2}
}
@app.callback(
    Output(component_id='histograph', component_property='figure'),
    [Input(component_id='xplothist', component_property='value'),
    Input(component_id='hueplothist', component_property='value'),
    Input(component_id='stdplothist', component_property='value')])
def update_histo(xx,hue,angka):
    return callbackupdatehisto(xx,hue,angka)
    
if __name__ == '__main__':
    app.run_server(debug=True)