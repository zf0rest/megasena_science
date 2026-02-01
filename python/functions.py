
import geopandas as gpd
import seaborn as sns
import matplotlib as plt

def dispersao(dados,eixo_x,eixo_y,titulo):
    plt.figure(figsize(10,6)) 
    ax = sns.scatterplot(data=dados, x=eixo_x, y=eixo_y, )




