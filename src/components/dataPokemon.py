import requests
import pandas as pd

res = requests.get('http://api-pokemon-baron.herokuapp.com/pokemon')
dfPokemon = pd.DataFrame(res.json(), columns=res.json()[0].keys())
dfPokemonTable = pd.DataFrame(res.json(), columns=res.json()[0].keys())

res2 = requests.get('http://api-pokemon-baron.herokuapp.com/getlistprediction')
dfHistory = pd.DataFrame(res2.json(), columns=res2.json()[0].keys())
dfHistoryTable = pd.DataFrame(res2.json(), columns=res2.json()[0].keys())
