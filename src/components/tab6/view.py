import dash_core_components as dcc
import dash_html_components as html
from src.components.dataPokemon import dfPokemon, dfPokemonTable

def renderIsiTab6():
    return [
        html.Center([
            html.H3('Predict Your New Pokemon!')
        ], className = 'title'),
        html.Div([
            html.Div([
                html.P('Name : '),
                dcc.Input(
                    id='predictname',
                    type='text',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-4'),
            html.Div([
                    html.P('Type 1 : '),
                    dcc.Dropdown(
                        id='predicttype1',
                        options= [{ 'label':i, 'value':i} for i in sorted(dfPokemon['Type 1'].unique())],
                        value=''
                    )
                ], className='col-4'),
            html.Div([
                    html.P('Type 2 : '),
                    dcc.Dropdown(
                        id='predicttype2',
                        options= [{ 'label':i, 'value':i} for i in sorted(dfPokemon['Type 2'].unique())],
                        value=''
                    )
                ], className='col-4'),
        ], className='row paddingtop'),
        html.Br(),
        html.Div([
            html.Div([
                    html.P('Generation : '),
                    dcc.Dropdown(
                        id='predictgeneration',
                        options=[i for i in [{ 'label': '1st Generation', 'value': '1' },
                                            { 'label': '2nd Generation', 'value': '2' },
                                            { 'label': '3rd Generation', 'value': '3' },
                                            { 'label': '4th Generation', 'value': '4' },
                                            { 'label': '5th Generation', 'value': '5' },
                                            { 'label': '6th Generation', 'value': '6' }]],
                        value=''
                    )
                ], className='col-3'),
            html.Div([
                html.P('Total : '),
                dcc.Input(
                    id='predicttotal',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
            html.Div([
                html.P('HP : '),
                dcc.Input(
                    id='predicthp',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
            html.Div([
                html.P('Speed : '),
                dcc.Input(
                    id='predictspeed',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
        ], className='row paddingtop'),
        html.Br(),
        html.Div([
            html.Div([
                html.P('Attack : '),
                dcc.Input(
                    id='predictattack',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
            html.Div([
                html.P('Defense : '),
                dcc.Input(
                    id='predictdefense',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
            html.Div([
                html.P('Sp. Attack : '),
                dcc.Input(
                    id='predictspattack',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
            html.Div([
                html.P('Sp. Defense : '),
                dcc.Input(
                    id='predictspdefense',
                    type='number',
                    value='',
                    style=dict(width='100%')
                )
            ], className='col-3'),
        ], className='row paddingtop'),
        html.Center([
            html.Div([
                    html.Br(),
                    html.Button('Predict', id='buttonpredict', style=dict(width='100%'))
                ], className='col-3')
        ]),
        html.Center([
            
        ], id='outputpredict', className = 'paddingtop')
    ]