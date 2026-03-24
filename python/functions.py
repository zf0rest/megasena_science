# -*- coding: utf-8 -*-
"""
Módulo de Visualização e Tratamento de Dados - Projeto Mega-Sena
Autor: Lucas Reges Lima
Versão: 1.0
"""

import numpy as np
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker 
from matplotlib import pyplot as plt
from matplotlib.pyplot import subplots, show, figure
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ==========================================
# FUNÇÕES DE LIMPEZA E UTILIDADE
# ==========================================
def dispersao(dados,eixo_x,eixo_y,titulo):
    '''A função recebe dados e plota um scatterplot com o padrão visual do trabalho'''
    plt.figure(figsize=(10,6)) 
    
    ax = sns.scatterplot(data=dados, 
                         x=eixo_x, 
                         y=eixo_y, 
                         palette='magma'
                         
                         )
    return plt.show()

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

# ==========================================
# FUNÇÕES DE PLOTAGEM ESTATÍSTICA
# ==========================================
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
        #pra cada coluna de nulo, geramos um texto nas posições 'x' e 'y' com o 's' sendo o valor

    plt.title(f'Total de registros vazios no dataframe:{nulos.sum()}\n~{(dataframe.shape[1]/dataframe.shape[0]):.2f}% do total', pad=30) #esse pad dá um espacinho pro titulo não ficar colado no gráfico    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.figtext(0.5, 0.01, "*Os números no topo das colunas são seus respectivos valores nulos", 
         ha="center", 
         fontsize=12, 
         style='italic', 
         bbox={'facecolor':'orange', 'alpha':0.2, 'pad':5})
    plt.show()

# ==========================================
# FUNÇÃO DE GEOPROCESSAMENTO
# ==========================================
def geo_x_bar(dataframe, col_valor, colors, titulo, subtitulo, legenda, label_gradiente):
    """Esta função recebe os argumentos acima, autoindicativos, afim de gerar um plot composto de dois itens: 
    
        1. Um mapa do Brasil na granularidade dos estados (por isso o dataframe deve ser um Geodf do geopandas)
        2. Um gráfico de barras que expressa a variação do mapa cloroplético segundo uma variável de gradação (col_valor)
    
    """ 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [2.2, 1]}) #quadro com dois plots novamente

    plt.subplots_adjust(top=0.9, bottom=0.20, left=0.2, right=0.8)
    ax1.set_xlim(-77, -34)
    ax1.set_ylim(-35, 10)

    dataframe.plot(column=col_valor,
                ax=ax1, # Agora apontamos para ax1
                legend=True, 
                cmap=colors,
                edgecolor='#7F8C8D',
                linewidth=0.5,
                legend_kwds={
                    'label': label_gradiente, 
                    'orientation': "horizontal",
                    'shrink': 0.3,
                    'pad': 0
                }
    )
    cor_do_tema = plt.get_cmap(colors)
    cor_titulo = cor_do_tema(0.95) #Isso aqui é a cor 95% mais escura do mapa de cores que o usuário passou.
    # Títulos alinhados ao ax1 que é o nosso mapinha
    ax1.text(0.05, 1.05, titulo, 
            transform=ax1.transAxes, fontsize=20, fontweight='bold', color= mcolors.to_hex(cor_titulo))
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

# ==========================================
# GRÁFICOS DE SÉRIES E BARRAS SIMPLES (ECONOMIA)
# ==========================================
def single_barplot(X, Y, titulo:str, subtitulo:str):
    """
    Este é um gráfico de barras específico, sem intuito de reutilizar,
    apenas deixá-lo aqui para que este código não ocupe espaço demasiado no notebook
    
    """
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(20, 10))
    ax = sns.barplot(x=X, y=Y, color='#00441b')

    plt.xticks(rotation=45)

    ax.text(0.0, 1.12, titulo, 
             transform=ax.transAxes, fontsize=20, fontweight='bold', color= '#00441b')
    ax.text(0.00, 1.075, subtitulo, 
             transform=ax.transAxes, fontsize=14, color='#7F8C8D')

    plt.subplots_adjust(top=0.82, bottom=0.15, left=0.1, right=0.95)
    plt.figtext(0.65, 0.07, 
                    'Dados extraídos da Caixa Econômica Federal (1996-2026) | Elaborado por Lucas Reges Lima', 
                    fontsize=10, 
                    color='#7F8C8D',
                    ha='left')

    sns.despine()
    plt.ylabel("R$ Bilhões", fontsize=12, color='#7F8C8D')
    plt.xlabel(None)
    ax.spines[['left', 'bottom']].set_visible(False)
    plt.show()

def doubleplot(X, Y, Y2, titulo:str, subtitulo:str, l1, l2):
    """
    Gera gráfico de linhas comparativo (Nominal vs. IPCA).
    
    Parâmetros:
    - X, Y, Y2: dados dos eixos (eixo X, série principal e série deflacionada).
    - titulo, subtitulo: textos do cabeçalho mantendo padrão visual do projeto.
    - l1, l2: legendas 1 e 2 do gráfico.
    
    Retorno: Exibe plot customizado com padrão visual corporativo.
    """
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(20, 10))

    #Plot da linha principal
    ax = sns.lineplot(x=X, y=Y, 
                      color='#00441b', linewidth=4, marker='o', label=l1)
    #Plot da linha secundária
    sns.lineplot(x=X, y=Y2, 
                 color='#7F8C8D', linewidth=2, linestyle='--', label=l2)

    plt.xticks(X, rotation=45)
    plt.ylabel("R$ Bilhões", fontsize=12, color='#7F8C8D')
    plt.xlabel(None)

    ax.text(0.0, 1.12, titulo, 
            transform=ax.transAxes, fontsize=20, fontweight='bold', color='#00441b')
    ax.text(0.00, 1.075, subtitulo, 
            transform=ax.transAxes, fontsize=14, color='#7F8C8D')

    plt.legend(frameon=False, fontsize=12, loc='upper left', bbox_to_anchor=(0, 1.05), ncol=2)

    plt.figtext(0.585, 0.07, 
                'Dados extraídos da Caixa Econômica Federal e SIDRA (IBGE) - (1996-2025) | Elaborado por Lucas Reges Lima', 
                fontsize=10, color='#7F8C8D', ha='left')

    sns.despine(left=True, bottom=True)
    plt.subplots_adjust(top=0.82, bottom=0.15, left=0.1, right=0.95)
    plt.show()    

# ==========================================
# FUNÇÃO DE CONVERGÊNCIA E HISTOGRAMAS (INFERÊNCIA)
# ==========================================

def plot_convergencia(df_hist):
    """
    Gera o gráfico de convergência do MAE (Lei dos Grandes Números) 
    (no padrãozinho visual dos outros gráficos que fizemos acima).
    """
    n = 60
    prob_teorica = 1 / n #(0,0166)
    erros_medios = [] #isso aqui vai ser o coração do plot, é basicamente o MAE ao longo do tempo 
    sorteios = range(60, len(df_hist) + 1, 12) # A partir do décimo sorteio (porque os primeiros sempre são bagunçados) até o último e de 10 em 10 números.

    for i in sorteios: #numeros sorteados
        dados_momento = df_hist.iloc[:i]
        contagem = dados_momento.iloc[:, 0].value_counts().reindex(range(1, 61), fill_value=0)
        #O reindex tá aqui basicamente para não quebrar o código se houver alguma janela de tempo (10 sorteios) com alguma dezena zerada e manter a lista na ordem crescente de 1 a 60
        freq_relativa = contagem / len(dados_momento)
        
        #MAE
        erro = np.mean(np.abs(freq_relativa - prob_teorica))
        erros_medios.append(erro)

    #Curva de tendência teórica (1/sqrt(N)) ancorada no primeiro erro médio [0]
    tendencia_teorica = [erros_medios[0]*(sorteios[0]**0.5)/ (s**0.5) for s in sorteios]

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(20, 10))
    ax = sns.lineplot(x=sorteios, y=erros_medios, 
    color='#00441b', linewidth=4, label='MAE real (desvio observado)')
    
    sns.lineplot(x=sorteios, y=tendencia_teorica, 
    color='#7F8C8D', linewidth=2, linestyle='--', label='Comportamento esperado (1/√N)')

    plt.ylabel("Erro Médio Absoluto", fontsize=12, color='#7F8C8D')
    plt.xlabel("Quantidade acumulada de dezenas sorteadas", fontsize=12, color='#7F8C8D')

    titulo = "A lei dos grandes números na Mega-Sena"
    subtitulo = "Convergência do erro médio em direção à uniformidade estatística (1996-2026)"
    
    ax.text(0.0, 1.12, titulo, transform=ax.transAxes, fontsize=20, fontweight='bold', color='#00441b')
    ax.text(0.00, 1.075, subtitulo,  transform=ax.transAxes, fontsize=14, color='#7F8C8D')

    plt.legend(frameon=False, fontsize=12, loc='upper left', bbox_to_anchor=(0, 1.05), ncol=2)
    plt.figtext(0.585, 0.07, 
                'Dados extraídos da Caixa Econômica Federal - (1996-2026) | Elaborado por Lucas Reges Lima', 
                fontsize=10, color='#7F8C8D', ha='left')
    sns.despine(left=True, bottom=True)
    plt.subplots_adjust(top=0.82, bottom=0.15, left=0.1, right=0.95)
    plt.show()

def plot_hist_dezenas_redline(dataset, freq_esp):

    plt.figure(figsize=(16,10))
    ax = sns.histplot(data=dataset, kde=False, bins=60, palette=['#00441b'], alpha=0.6, discrete=True, legend=False) 
    plt.xticks(range(1,61,2))


    ax.text(0.0, 1.12, 'O quanto os meus dados estão longe do alvo',
            transform=ax.transAxes, fontsize=22, fontweight='bold', color='#00441b')
    ax.text(0.00, 1.075, 'distribuição das dezenas em relação à frequência esperada', 
            transform=ax.transAxes, fontsize=16, color='#7F8C8D')

    plt.figtext(0.45, 0.05, 'Dados extraídos da Caixa Econômica Federal (1996-2026) | Elaborado por Lucas Reges Lima', 
                        fontsize=13, 
                        color='#7F8C8D',
                        ha='left')


    plt.tight_layout(rect=[-0.2, 0.08, 0.97, 1], w_pad=-50)

    plt.axhline(freq_esp, color='red', linestyle = '-', label = 'Freq. Esperada')

    plt.ylabel("Contagem de Sorteios", color='#7F8C8D')

    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.show()

def plot_hist_dezenas(dataset):
    plt.figure(figsize=(16,10))
    ax = sns.histplot(data=dataset, kde=False, bins=60, palette=['#00441b'], alpha=0.6, discrete=True, legend=False) 
    plt.xticks(range(1,61,2))


    ax.text(0.0, 1.12, 'Afinal, é ou não uniforme?',
            transform=ax.transAxes, fontsize=22, fontweight='bold', color='#00441b')
    ax.text(0.00, 1.075, 'distribuição das dezenas de 1996 a 2026', 
            transform=ax.transAxes, fontsize=16, color='#7F8C8D')

    plt.figtext(0.45, 0.05, 'Dados extraídos da Caixa Econômica Federal (1996-2026) | Elaborado por Lucas Reges Lima', 
                        fontsize=13, 
                        color='#7F8C8D',
                        ha='left')


    plt.tight_layout(rect=[-0.2, 0.08, 0.97, 1], w_pad=-50)

    plt.ylabel("Contagem de Sorteios", color='#7F8C8D')

    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.show()