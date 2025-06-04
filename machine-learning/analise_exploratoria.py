'''
Objetivo: compreender a base de dados gerada (simulando a real) e entender as relações entre as variaveis disponíveis para análise.
Isso deve permitir cogitar quais modelos podem ser aplicados à base de dados e quais tipos de análises são possíveis
'''

import pandas as pd
import sqlite3 
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

conn = sqlite3.connect("database/simulacao_planta.db")
df = pd.read_sql("SELECT * FROM registros_limpeza", conn)

#visualização básica dos dados disponíveis
print(df.head())
print(df.describe())

# 1. Boxplot (com legenda)
boxplot = px.box(
    df,
    x="produto",
    y="tempo_limpeza",
    color="produto",
    title="Boxplot: Tempo de Limpeza por Produto"
)

# 2. Scatterplot (sem legenda, mas com cores)
scatter = px.scatter(
    df,
    x="tempo_limpeza",
    y="volume_agua",
    color="produto",
    title="Relação Tempo vs Água",
    hover_name="produto"  # Nome do produto no hover
)

# Cria subplots
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Boxplot", "Scatterplot"),
    vertical_spacing=0.15
)

# Adiciona os gráficos
for trace in boxplot.data:
    fig.add_trace(trace, row=1, col=1)

for trace in scatter.data:
    fig.add_trace(trace, row=2, col=1)

# Ajustes de layout:
fig.update_layout(
    height=900,
    width=1000,
    showlegend=False,  # Remove TODAS as legendas (se quiser manter só no boxplot, veja abaixo)
    plot_bgcolor="white"
)

# Alternativa: Remove a legenda APENAS do scatter (linha 2, coluna 1)
fig.update_traces(showlegend=False, row=2, col=1)

# Rotaciona rótulos do boxplot
fig.update_xaxes(tickangle=-45, row=1, col=1)

fig.show()