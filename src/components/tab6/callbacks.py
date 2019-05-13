import pandas as pd
import pickle
import requests
import dash_html_components as html

loadModel = pickle.load(open('rfc_pokemon.sav', 'rb'))
encoderType1 = pickle.load(open('le1_type1.sav', 'rb'))
encoderType2 = pickle.load(open('le2_type2.sav', 'rb'))

def callbackPredict(n_clicks, name, type1, type2, generation, total,hp, speed, attack, defense, spatk, spdef):
    if (name != '' and type1 != '' and type2 != '' and generation != '' and total != '' and hp != '' 
    and attack != '' and defense != '' and spatk != '' and spdef != ''):
        t1 = encoderType1.transform([type1])
        t2 = encoderType2.transform([type2])
        predictProb = loadModel.predict_proba([[t1[0], t2[0], total, hp, attack, speed, defense, spatk, spdef, generation]])
        
        prediction = 'Normal'
        predictSave = 0

        if(predictProb[0,1] > 0.15):
            prediction = 'Legendary'
            predictSave = 1

        data = {
            'name': name,
            'type1': type1,
            'type2': type2,
            'total': total,
            'hp': hp,
            'attack': attack,
            'defense': defense,
            'spatk': spatk,
            'spdef': spdef,
            'speed': speed,
            'generation': generation,
            'legendary': predictSave,
            'legendaryproba': predictProb[0,1],
            'createdby': 'Warren'
        }

        res = requests.post('http://api-pokemon-baron.herokuapp.com/saveprediction', data = data)
        print(res.content)

        return [
            html.H3('Probability your Pokemon is Legendary: {}%'.format(predictProb[0,1]*100)),
            html.H3('So we predict {} is a {} Pokemon'.format(name, prediction))
        ]
    else:
        return html.H3('Please fill all inputs in the form above to predict your pokemon')
