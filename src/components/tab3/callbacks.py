import plotly.graph_objs as go
from src.components.dataPokemon import dfPokemon
from src.components.dataSupport import legendDict


def callbackupdatescattergraph(hue,x,y):
    return dict(
                data=[
                    go.Scatter(
                        x=dfPokemon[dfPokemon[hue]==i][x],
                        y=dfPokemon[dfPokemon[hue]==i][y],
                        name=legendDict[hue][i],
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