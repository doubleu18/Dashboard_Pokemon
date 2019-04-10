import plotly.graph_objs as go
from src.components.dataPokemon import dfPokemon

def classupdatepiechart(group):
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