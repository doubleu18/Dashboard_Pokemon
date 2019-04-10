import dash_core_components as dcc
import dash_html_components as html
from src.components.dataPokemon import dfPokemon

def renderIsiTab5():
    return [
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
        ]