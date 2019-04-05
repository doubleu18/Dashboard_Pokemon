import os

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from categoryPlot import dfPokemon, listGoFunc, generateValuePlot, go, res, dfPokemon, pd
from plotly import tools

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

server=app.server

df = pd.read_csv('PokemonKece.csv')

def generate_table(dataframe, max_rows=10) :
    return html.Table(
         # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe.iloc[i,col])) for col in range(len(dataframe.columns))
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.title='Dashboard Pokemon'

app.layout = html.Div([
        html.H1('Dashboard Pokemon'),
        html.H3('''
                Created by: Brane Warren
                '''),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Pokemon', value='tab-1', children=[
            html.Div([
                html.Div([
                    html.P('Name : '),
                    dcc.Input(
                        id='filternametable',
                        type='text',
                        value='',
                        style=dict(width='100%')
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Generation : '),
                    dcc.Dropdown(
                        id='filtergenerationtable',
                        options=[i for i in [{ 'label': 'All Generation', 'value': '' },
                                            { 'label': '1st Generation', 'value': '1' },
                                            { 'label': '2nd Generation', 'value': '2' },
                                            { 'label': '3rd Generation', 'value': '3' },
                                            { 'label': '4th Generation', 'value': '4' },
                                            { 'label': '5th Generation', 'value': '5' },
                                            { 'label': '6th Generation', 'value': '6' }]],
                        value=''
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Category : '),
                    dcc.Dropdown(
                        id='filtercategorytable',
                        options=[i for i in [{ 'label': 'All Category', 'value': '' },
                                            { 'label': 'Legendary', 'value': 'True' },
                                            { 'label': 'Non-Legendary', 'value': 'False' }]],
                        value=''
                    )
                ], className='col-4')
            ], className='row'),
            html.Br(),
            html.Div([
                html.Div([
                    html.P('Total : '),
                    dcc.RangeSlider(
                        marks={i: '{}'.format(i) for i in range(dfPokemon['Total'].min(), dfPokemon['Total'].max()+1,100)},
                        min=dfPokemon['Total'].min(),
                        max=dfPokemon['Total'].max(),
                        value=[dfPokemon['Total'].min(),dfPokemon['Total'].max()],
                        className='rangeslider',
                        id='filtertotaltable'
                    )
                ], className='col-9'),
                html.Div([

                ],className='col-1'),
                html.Div([
                    html.Br(),
                    html.Button('Search', id='buttonsearch', style=dict(width='100%'))
                ], className='col-2')
            ], className='row'),
            html.Br(),html.Br(),html.Br(),
            html.Div([
                html.Div([
                    html.P('Max Rows : '),
                    dcc.Input(
                        id='filterrowstable',
                        type='number',
                        value=10,
                        style=dict(width='100%')
                    )
                ], className='col-1')
            ], className='row'),
            html.Center([
                html.H2('Data Pokemon', className='title'),
                html.Div(id='tablediv')
            ])
        ]),
        dcc.Tab(label='Categorical Plots', value='tab-2',children=[
            html.Div([
                html.Div([
                    html.P('Jenis: '),
                    dcc.Dropdown(
                        id='jenisplotcategory',
                        options=[{'label' : i, 'value': i} for i in ['Bar','Box','Violin']],
                        value='Bar'
                    )
                ], className='col-3'),
                html.Div([
                    html.P('X: '),
                    dcc.Dropdown(
                        id='xplotcategory',
                        options=[{'label' : i, 'value': i} for i in ['Generation','Type 1','Type 2']],
                        value='Generation'
                    )
                ], className='col-3'),
                html.Div([
                    html.P('Y: '),
                    dcc.Dropdown(
                        id='yplotcategory',
                        options=[{'label' : i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='Total'
                    ),
                ], className='col-3'),
                html.Div([
                    html.P('Stats: '),
                    dcc.Dropdown(
                        id='statsplotcategory',
                        options=[i for i in [{'label' : 'Mean','value' :'mean'},
                                            {'label' : 'Standard Deviation','value':'std'},
                                            {'label' : 'Count','value':'count'},
                                            {'label' : 'Max','value':'max'},
                                            {'label' : 'Min','value':'min'},
                                            {'label' : '25th Percentiles','value':'25%'},
                                            {'label' : 'Median','value':'50%'},
                                            {'label' : '75th Percentiles','value':'75%'}]],
                        value='mean',
                        disabled=True
                    ),
                ], className='col-3')
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='categoryGraph'
            )
        ]),
        dcc.Tab(label='Scatter Plot', value='tab-3', children = [
            html.Div([
                html.Div([
                    html.P('Hue: '),
                    dcc.Dropdown(
                        id='hueplotscatter',
                        options=[{'label' : i, 'value': i} for i in ['Legendary','Generation','Type 1','Type 2']],
                        value='Legendary'
                    )
                ], className='col-4'),
                html.Div([
                    html.P('X: '),
                    dcc.Dropdown(
                        id='xplotscatter',
                        options=[{'label' : i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='Attack'
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Y: '),
                    dcc.Dropdown(
                        id='yplotscatter',
                        options=[{'label' : i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='HP'
                    ),
                ], className='col-4'),
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='scattergraph',
            )
        ]),
        dcc.Tab(label='Pie Chart', value='tab-4', children = [
            html.Div([
                html.Div([
                    html.P('Group : '),
                    dcc.Dropdown(
                        id='groupplotpie',
                        options=[{'label' : i, 'value': i} for i in ['Legendary','Generation','Type 1','Type 2']],
                        value='Legendary'
                    ),
                ], className='col-4'),
            ], className='row'),
            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            dcc.Graph(
                id='piegraph',
            )
        ]),
        dcc.Tab(label='Histogram', value='tab-5', children = [
            html.Div([
                html.Div([
                    html.P('Group : '),
                    dcc.Dropdown(
                        id='xplothist',
                        options=[{'label' : i, 'value': i} for i in dfPokemon.columns[4:11]],
                        value='Total')
                ], className='col-4'),
                html.Div([
                    html.P('Group : '),
                    dcc.Dropdown(
                        id='hueplothist',
                        options=[{'label' : i, 'value': i} for i in ['All','Legendary','Generation']],
                        value='All')
                ], className='col-4'),
                html.Div([
                    html.P('STD : '),
                    dcc.Dropdown(
                        id='stdplothist',
                        options=[{'label' : i, 'value': i} for i in [1,2,3]],
                        value='2')
                ], className='col-4'),
            ], className='row'),
            html.Br(),html.Br(),
            dcc.Graph(
                id='histograph'
            ),
        ]),
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


# Plots
@app.callback(
    Output(component_id='categoryGraph', component_property='figure'),
    [Input(component_id='jenisplotcategory', component_property='value'),
    Input(component_id='xplotcategory', component_property='value'),
    Input(component_id='yplotcategory', component_property='value'),
    Input(component_id='statsplotcategory', component_property='value')])
def update_category_graph(jenisplot, xplot, yplot, statsplot):
    return dict(
        layout = go.Layout(
                title= '{} Plot Pokemon'.format(jenisplot),
                xaxis= {'title': xplot} ,
                yaxis= dict(title=yplot),
                boxmode='group',
                violinmode='group'
            ),
        data=[
            listGoFunc[jenisplot](
                x=generateValuePlot('True',xplot,yplot,)['x'][jenisplot],
                y=generateValuePlot('True',xplot,yplot,statsplot)['y'][jenisplot],
                name='Legendary'
            ),
            listGoFunc[jenisplot](
                x=generateValuePlot('False',xplot,yplot)['x'][jenisplot],
                y=generateValuePlot('False',xplot,yplot,statsplot)['y'][jenisplot],
                name='Non-Legendary'
            )
        ]
    )

# Jenis Plot
@app.callback(
    Output(component_id='statsplotcategory', component_property='disabled'),
    [Input(component_id='jenisplotcategory', component_property='value')])
def update_disabled_stats(jenisplot):
    if jenisplot=='Bar':
        return False
    return True

# Scatter Plot
legendScatterDict = {
    'Legendary' : {'True' : 'Legendary', 'False' : 'Non-Legendary'},
    'Generation' : {1 : '1st Generation', 2 : '2nd Generation', 3 : '3rd Generation', 4 : '4th Generation', 5 : '5th Generation', 6 : '6th Generation'},
    'Type 1' : {i:i for i in dfPokemon['Type 1'].unique()},
    'Type 2' : {i:i for i in dfPokemon['Type 2'].unique()}
}
@app.callback(
    Output(component_id='scattergraph', component_property='figure'),
    [Input(component_id='hueplotscatter', component_property='value'),
    Input(component_id='xplotscatter', component_property='value'),
    Input(component_id='yplotscatter', component_property='value')])
def update_scatter_plot(hue,x,y):
    return dict(
                data=[
                    go.Scatter(
                        x=dfPokemon[dfPokemon[hue]==i][x],
                        y=dfPokemon[dfPokemon[hue]==i][y],
                        name=legendScatterDict[hue][i],
                        mode='markers')
                    for i in dfPokemon[hue].unique()
                ],
                    layout = go.Layout(
                        title= 'Scatter Plot Pokemon',
                        xaxis= {'title': x} ,
                        yaxis= dict(title=y),
                        margin={'l':40,'b':40, 't':40, 'r':10},
                        hovermode='closest'
                    )
            )

# Pie Chart
@app.callback(
    Output(component_id='piegraph', component_property='figure'),
    [Input(component_id='groupplotpie', component_property='value')])
def update_pie_chart(group):
    return dict(
                data=[
                    go.Pie(
                        labels=dfPokemon[group].unique(),
                        values=[
                            len(dfPokemon[dfPokemon[group] == dfPokemon[group].unique()[j]]) 
                            for i,j in zip(dfPokemon[group].unique(),range(len(dfPokemon[group].unique())))
                        ]
                    ) 
                ],
                layout=go.Layout(
                        title= 'Pie Chart Pokemon',
                        margin={'l':50,'b':40, 't':40, 'r':10}
                        )
    )

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
    dfFilter = dfPokemon[(dfPokemon['Name'].str.contains(name)) & ((dfPokemon['Total'] >= total[0]) & (dfPokemon['Total'] <= total[1]))]
    if(generation != '') :
        dfFilter = dfFilter[dfFilter['Generation'] == int(generation)]
    if(category != '') :
        dfFilter = dfFilter[dfFilter['Legendary'] == category]

    return generate_table(dfFilter, max_rows=int(maxrows))


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
    uniqueData=dfPokemon
    angka=int(angka)
    if(hue != 'All'):
        uniqueData = dfPokemon[hue].unique().reshape(rowcolhist[hue]['row'],rowcolhist[hue]['col'])
        titleHist = []
        for i in range(1,rowcolhist[hue]['row']+1):
            for j in range(1,rowcolhist[hue]['col']+1):
                dfPokemon2 = dfPokemon[dfPokemon[hue]==uniqueData[i-1,j-1]]
                x=dfPokemon2[(dfPokemon2[xx]>=(dfPokemon2[xx].mean()+dfPokemon2[xx].std()*angka))|(dfPokemon2[xx]<=dfPokemon2[xx].mean()-dfPokemon2[xx].std()*angka)][xx]
                outlierTitle = round(len(x)/len(dfPokemon2)*100, 2)
                titleHist.append('{} {} ({} Outlier)'.format(hue,uniqueData[i-1,j-1],outlierTitle))

        fig = tools.make_subplots(rows=rowcolhist[hue]['row'], cols=rowcolhist[hue]['col'], subplot_titles=tuple(titleHist))

        for i in range(1,rowcolhist[hue]['row']+1):
            for j in range(1,rowcolhist[hue]['col']+1):
                dfPokemon2 = dfPokemon[dfPokemon[hue]==uniqueData[i-1,j-1]]
                fig.append_trace(go.Histogram(
                    x=dfPokemon2[(dfPokemon2[xx]<=(dfPokemon2[xx].mean()+dfPokemon2[xx].std()*angka))&(dfPokemon2[xx]>=dfPokemon2[xx].mean()-dfPokemon2[xx].std()*angka)][xx],
                    nbinsx=0,
                    name='{} {} {} Normal'.format(xx,hue, uniqueData[i-1,j-1]),
                    marker=dict(
                        color='Green'
                    ),
                ),int(i),int(j))
                fig.append_trace(go.Histogram(
                    x=dfPokemon2[(dfPokemon2[xx]>=(dfPokemon2[xx].mean()+dfPokemon2[xx].std()*angka))|(dfPokemon2[xx]<=dfPokemon2[xx].mean()-dfPokemon2[xx].std()*angka)][xx],
                    nbinsx=0,
                    name='{} {} {} Abnormal'.format(xx,hue, uniqueData[i-1,j-1]),
                    marker=dict(
                        color='Red'
                    )
                ),int(i),int(j))
        
        for i in range (1, len(titleHist)+1):
            fig['layout']['xaxis{}'.format(i)].update(title=xx)
            fig['layout']['yaxis{}'.format(i)].update(title='Count')
        
        if hue=='Generation':
            fig['layout'].update(height=800)
        elif hue=='Legendary':
            fig['layout'].update(height=500)
        return fig
    elif(hue == 'All'):
        return dict(
            data=[
                go.Histogram(
                    x=dfPokemon[(dfPokemon[xx]<=(dfPokemon[xx].mean()+dfPokemon[xx].std()*angka))&(dfPokemon[xx]>=dfPokemon[xx].mean()-dfPokemon[xx].std()*angka)][xx],
                    name='{} {} Normal'.format(xx,hue),
                    marker=dict(
                        color='Green'
                    )
                ),
                go.Histogram(
                    x=dfPokemon[(dfPokemon[xx]>=(dfPokemon[xx].mean()+dfPokemon[xx].std()*angka))|(dfPokemon[xx]<=dfPokemon[xx].mean()-dfPokemon[xx].std()*angka)][xx],
                    name='{} {} Abnormal'.format(xx,hue),
                    marker=dict(
                        color='Red'
                    )
                )
            ],
            layout=go.Layout(
                    title='Histogram {} Stats Pokemon'.format(xx),
                    xaxis=dict(title=str(xx)),
                    yaxis=dict(title='Count'),
                    height=500
            )
        )

if __name__ == '__main__':
    app.run_server(debug=True)