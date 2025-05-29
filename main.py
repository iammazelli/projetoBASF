from getData import dataframeParaSimulacao
from simulacao import SimuladorDaLimpeza

df_medios = dataframeParaSimulacao() 
simulador = SimuladorDaLimpeza(df_medios, db_name = "/home/derickoso/Area_de_Trabalho/Programming/Python/PEEBasf/planta_text.db")
simulador.simular_periodo(30)
dados_limpeza = simulador.ler_banco()
print(dados_limpeza.head())
