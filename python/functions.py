
# -*- coding: utf-8 -*-
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker 
from matplotlib import pyplot as plt
from matplotlib.pyplot import subplots, show, figure
import matplotlib.cm as cm
import matplotlib.colors as mcolors

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

def geo_x_bar(dataframe, col_valor, colors, titulo, subtitulo, legenda):
    """Esta função recebe os argumentos acima, autoindicativos, afim de gerar um plor composto de dois itens: 
    
        1. Um mapa do Brasil na granularidade dos estados (por isso o dataframe deve ser um Geodf do geopandas)
        2. Um gráfico de barras que expressa a variação do mapa cloroplético segundo uma variável de gradação (col_valor)
    
    """ 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [2.2, 1]}) #quadro com dois plots novamente

    plt.subplots_adjust(top=0.9, bottom=0.20, left=0.2, right=0.8)
    ax1.set_xlim(-77, -34)
    ax1.set_ylim(-35, 10)
    # --- LADO ESQUERDO: O MAPA (ax1) ---
    dataframe.plot(column=col_valor,
                ax=ax1, # Agora apontamos para ax1
                legend=True, 
                cmap=colors,
                edgecolor='#7F8C8D',
                linewidth=0.5,
                legend_kwds={
                    'label': "Nº de ganhadores (dos que se tem informação)", 
                    'orientation': "horizontal",
                    'shrink': 0.3,
                    'pad': 0
                }
    )

    # Títulos alinhados ao ax1 que é o nosso mapinha
    ax1.text(0.05, 1.05, titulo, 
            transform=ax1.transAxes, fontsize=20, fontweight='bold', color='#00441b')
    ax1.text(0.05, 0.97, subtitulo, 
            transform=ax1.transAxes, fontsize=14, color='#7F8C8D')
    ax1.axis('off') #EU prefiro um design minimalista para uma análise informal, então tiro as barras em torno do mapa



    df_topestados = dataframe.sort_values(col_valor, ascending=True).tail(10) #podia ser o ascending = False e o Head no lugar
    # A coisa mais complicad desse plot foi aplicar a mesma escala de cores do GeoMap no gráfico de barras. A lógia é a seguinte:
   
    # Importe o colormaps e o colors do matplotlib > Criamos um normalizador que escala seus dados de 0 a 1 (como a correlação de Pearson faz)
    Escala_numerica = mcolors.Normalize(vmin=dataframe[col_valor].min(), #seu mínimo
                            vmax=dataframe[col_valor].max()) #seu máximo
    
    # > Criamos o mapeador de cores usando o mesmo cmap do mapa (colors no caso) - ele vai atribui uma cor para cada valor da sua escala numérica >
    dict_cores = cm.ScalarMappable(norm=Escala_numerica, cmap=colors)
    
    # > Aplicamos as cores para cada valor na hora de plotar
    Escala_cores = [dict_cores.to_rgba(i) for i in df_topestados[col_valor]]
   
    # > Agora sim, passamos a lista de cores para o barh
    barras = ax2.barh(df_topestados['SIGLA_UF'], 
                    df_topestados[col_valor], 
                    color=Escala_cores
    ) #veja que a escala de cores foi aplicada no DF INTEIRO, e não nos top10, seguindo o padrão do gráfico

    for bar in barras: #pra cada barra, gere uma descrição com tais características.
        width = bar.get_width()
        ax2.text(int(width) + 5,
                bar.get_y() + bar.get_height()/2, 
                int(width),
                va='center', 
                fontsize=12, 
                color='#7F8C8D', 
                fontweight='bold'
                )

    #setando os atributos visuais das barras
    ax2.spines['left'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.get_xaxis().set_visible(False) 


    #Configurando a legenda
    plt.figtext(0.6, 0.07, 
                legenda, 
                fontsize=10, 
                color='#7F8C8D',
                ha='left')

    plt.tight_layout(rect=[-0.2, 0.08, 0.97, 1], w_pad=-50)

    plt.show()