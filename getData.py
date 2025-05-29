import pandas as pd
from tkinter import Tk, filedialog
import os

#função para retornar uma lista de arquivos csv
def getPlanilhas():
    planilhas = list()
    root = Tk()
    root.withdraw()
    caminhos = filedialog.askopenfilenames(
        title = "Selecione os arquivos",
        filetypes = [("Planilhas", "*.csv *.xlsx *.xls")]
    )

    if len(caminhos) < 1:
        print("Selecione ao menos 1 arquivo para upload!")
    else:
        for caminho in caminhos:
            planilhas.append(caminho)

    return planilhas
        

#função que retorna uma lista de dataframes sem as duas primeiras linhas
def geraDataFrames():
    planilhas = getPlanilhas()
    if not planilhas:
        return None
    dataframes_limpos = list()
    for planilha in planilhas:
        df = pd.read_csv(planilha, skiprows=2)
        df = df.rename(columns={"Próximo Produto" : "produto"})
        dataframes_limpos.append(df)
    
    return dataframes_limpos

#função para combinar os dataframes baseados nos produtos
def unificaDataframes():
    dataframes = geraDataFrames()
    if not dataframes:
        return None
    
    colunaProdutos = dataframes[0].columns[0]

    produtos = set()
    for df in dataframes:
        df[colunaProdutos] = df[colunaProdutos].astype(str).str.strip().str.upper()
        produtos.update(df[colunaProdutos].unique())

    base = pd.DataFrame({colunaProdutos: sorted(produtos)})

    df_unificado = base.copy()
    for df in dataframes:
        df_unificado = df_unificado.merge(df, on=colunaProdutos, how='left')
    
    return df_unificado

def dataframeParaSimulacao():
    df_unificado = unificaDataframes()
    if df_unificado is None:
        print("Nenhum DataFrame para processar!")
        return
    
    colunas_para_renomear = {
        "Média de NumRealAmostras" : "media_amostras",
        "Total" : "tempo_medio",
        "Soma de MediaWaterVolum_A" : "volume_medio_agua"
    }

    colunas_para_excluir = ['Média de NumMinAmostras', 'Média de NumMaxAmostras', 'Parte A', 'Parte B']
    df_unificado = df_unificado.rename(columns = colunas_para_renomear)
    colunas_existentes = [col for col in colunas_para_excluir if col in df_unificado.columns]
    if colunas_existentes:
        df_unificado = df_unificado.drop(columns=colunas_existentes)

    return df_unificado.dropna()#exclui aqueles produtos dados que não possuimos todos os parametros
