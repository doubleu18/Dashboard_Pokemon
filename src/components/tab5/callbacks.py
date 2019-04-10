import plotly.graph_objs as go
from plotly import tools
from src.components.dataPokemon import dfPokemon

rowcolhist={
    'All': {'row':1, 'col':1},
    'Legendary':{'row':1,'col':2},
    'Generation':{'row':3,'col':2}
}

def callbackUpdateHisto(xx,hue,angka):
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
                    name='{} {} {} Normal'.format(xx,hue,uniqueData[i-1,j-1]),
                    marker=dict(
                        color='Green'
                    ),
                ),int(i),int(j))
                fig.append_trace(go.Histogram(
                    x=dfPokemon2[(dfPokemon2[xx]>=(dfPokemon2[xx].mean()+dfPokemon2[xx].std()*angka))|(dfPokemon2[xx]<=dfPokemon2[xx].mean()-dfPokemon2[xx].std()*angka)][xx],
                    nbinsx=0,
                    name='{} {} {} Abnormal'.format(xx,hue,uniqueData[i-1,j-1]),
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