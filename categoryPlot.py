
import pandas as pd
import requests
import plotly.graph_objs as go


res = requests.get('http://api-pokemon-baron.herokuapp.com/pokemon')
dfPokemon = pd.DataFrame(res.json(), columns=res.json()[0].keys())
    
listGoFunc = {
    'Bar': go.Bar,
    'Box': go.Box,
    'Violin': go.Violin
}

def generateValuePlot(legendary,xplot,yplot, statsplot = 'mean'):
    return {
        'x': {
            'Bar': dfPokemon[dfPokemon['Legendary'] == legendary][xplot].unique(),
            'Box': dfPokemon[dfPokemon['Legendary'] == legendary][xplot],
            'Violin': dfPokemon[dfPokemon['Legendary'] == legendary][xplot]
        },
        'y': {
            'Bar': dfPokemon[dfPokemon['Legendary'] == legendary].groupby(xplot)[yplot].describe()[statsplot],
            'Box': dfPokemon[dfPokemon['Legendary'] == legendary][yplot],
            'Violin': dfPokemon[dfPokemon['Legendary'] == legendary][yplot]
        }
    }