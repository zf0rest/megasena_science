
# -*- coding: utf-8 -*-
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker 
from matplotlib import pyplot as plt
from matplotlib.pyplot import subplots, show, figure

def dispersao(dados,eixo_x,eixo_y,titulo):
    '''A função recebe dados e plota um scatterplot com o padrão visual do trabalho'''
    plt.figure(figsize=(10,6)) 
    
    ax = sns.scatterplot(data=dados, 
                         x=eixo_x, 
                         y=eixo_y, 
                         palette='magma'
                         
                         )
    return plt.show()


def comparativo_SQQ(win6,win5,win4):

    fig, axes = subplots(2,3, figsize=(16,8)) # nesse pedaço eu abro um quadro para vários plots
    cores = sns.color_palette("magma", 3)
    ##########              Histogramas                      ##########

    sns.histplot(x = win6, ax=axes[0,0], color=cores[2], bins = 50)# Usar a escala logarítimica aqui não vai ajudar muita coisa
    sns.rugplot(x=win6, ax=axes[0,0], color='gray', alpha=0.3)
    axes[0,0].xaxis.label.set_visible(False)

    sns.histplot(data= win5, ax=axes[0,1], color=cores[1], bins=50)
    sns.rugplot(x=win5, ax=axes[0,1], color='gray', alpha=0.3)

    sns.histplot(data= win4, ax=axes[0,2], kde=False, color=cores[0], bins = 50)
    sns.rugplot(x=win4, ax=axes[0,2], color='gray', alpha=0.3)

    ##########                Violin Plots                    ##########

    sns.violinplot(x= win6, ax=axes[1,0], color=cores[2])
    axes[0,0].set_title("Ganhadores da Sena")

    sns.violinplot(x= win5, ax=axes[1,1], color=cores[1])
    axes[0,1].set_title("Ganhadores da Quina")

    sns.violinplot(x= win4, ax=axes[1,2], color=cores[0])
    axes[0,2].set_title("Ganhadores da Quadra")

    for ax in axes.flatten(): #tirando os labels dos eixos desnecessários
        ax.set_xlabel("")
        ax.set_ylabel("")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10) 
    #preciso colocar a figura um pouco mais de espaço para o comentário abaixo
    fig.text(0.5, 0.01, "*As escalas variam drasticamente entre Sena e Quadra", 
         ha="center", fontsize=12, style='italic', bbox={'facecolor':'orange', 'alpha':0.2, 'pad':5})
    plt.show()





    ############ Limpeza de strings ###################

def limpar_strings(string):
    ''' Esta função recebe uma string e:
    - Coloca tudo em maiúsculo;
    - Retira os acentos;
    - Retira os espaços invisíveis antes e depois da string (mantém espaços internos)
    retorna, por fim a string limpa 
    '''
    return (string.str.upper()
         .str.normalize('NFKD')
         .str.encode('ascii', errors='ignore')
         .str.decode('utf-8')
         .str.strip()
         )
    
    

############## Analisando completude do Dataframe ###############

def vacancia(dataframe):
    '''Função recebe um dataframe e devolve um mapa de calor de valores vazios no dataframe.'''
    
    plt.figure(figsize=(16, 8))
    nulos = dataframe.isnull().sum() #isso aqui é uma lista da soma dos nulos em cada coluna
    ax = sns.heatmap(dataframe.isnull(), 
                     yticklabels=False, 
                     cbar=False, 
                     cmap='Greys_r' #reverti pra gerar um efeito visual de "vazio" melhor para o usuário
                                )
    
    for i in range(len(nulos)):
        plt.text(x = i + 0.5,y=-1.5 , s = nulos[i], ha='center') 
        #pra cada coluna de nulo, geramos um texto nas posições 'x' e 'y' com o 's' sendo o conteúdo

    plt.title(f'Total de registros vazios no dataframe:{nulos.sum()}\n~{(dataframe.shape[1]/dataframe.shape[0]):.2f}% do total', pad=30) #esse pad dá um espacinho pro titulo não ficar colado no gráfico    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.figtext(0.5, 0.01, "*Os números no topo das colunas são seus respectivos valores nulos", 
         ha="center", 
         fontsize=12, 
         style='italic', 
         bbox={'facecolor':'orange', 'alpha':0.2, 'pad':5})
    plt.show()

