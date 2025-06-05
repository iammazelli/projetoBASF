from getData import dataframeParaSimulacao
from simulation import SimuladorDaLimpeza
import os

df_medios = dataframeParaSimulacao() 
if not os.path.exists("database/"):
    os.makedirs("database/")
simulador = SimuladorDaLimpeza(df_medios, db_name = "database/simulacao_planta.db")
simulador.simular_periodo(350) #simulando 350 dias de atividade na planta
dados_limpeza = simulador.ler_banco()
print(dados_limpeza.head())
