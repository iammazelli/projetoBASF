from getData import dataframeParaSimulacao
from simulacao import SimuladorDaLimpeza

df_medios = dataframeParaSimulacao() 
simulador = SimuladorDaLimpeza(df_medios, db_name = "planta_test.db")
simulador.simular_periodo(30)
dados_limpeza = simulador.ler_banco()
print(dados_limpeza.head())
