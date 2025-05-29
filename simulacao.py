'''
Na ausência de dados reais e com a obtenção dos dados médios dos parâmetros Amostras, Tempo e Volume de Água,
este código tem o objetivo de gerar uma simulação de registros de dados usando estatística para que possamos obter um modelo de 
Machine Learning que utilize dados mais parecidos com os reais.
'''
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import sqlite3

class SimuladorDaLimpeza:
    def __init__(self, df_medios, variabilidade=0.15, db_name='limpeza_planta.db'):
        self.df_medios = df_medios.set_index('produto')
        self.variabilidade = variabilidade
        self.db_name = db_name 
        self._setup_database()

    def _setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_limpeza(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            data_hora DATETIME NOT NULL, 
            tempo_limpeza REAL NOT NULL,
            volume_agua REAL NOT NULL,
            num_amostras INTEGER NOT NULL,
            operador TEXT,
            equipamento TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def _gerar_valor(self, valor_medio, inteiro=False):
        variacao = random.uniform(-self.variabilidade, self.variabilidade)
        valor = valor_medio*(1+variacao)
        return round(valor) if inteiro else round(valor, 2)
    
    def simular_limpeza(self, produto, data_hora=None):
        if produto not in self.df_medios.index:
            raise ValueError(f"Produto {produto} não encontrado no DataFrame!")
        
        if data_hora is None:
            data_hora = datetime.now()

        dados = self.df_medios.loc[produto]

        registro = {
            'produto': produto,
            'data_hora': data_hora,
            'tempo_limpeza': self._gerar_valor(dados['tempo_medio']),
            'volume_agua': self._gerar_valor(dados['volume_medio_agua']),
            'num_amostras': self._gerar_valor(dados['media_amostras'], inteiro=True),
            'operador': f"OP{random.randint(1,20):03d}",
            'equipamento': f"EQ{random.randint(1,10):02d}"
        }

        return registro
    
    def salvar_no_banco(self, registro):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO registros_limpeza
        (produto, data_hora, tempo_limpeza, volume_agua, num_amostras, operador, equipamento)
        VALUES (?,?,?,?,?,?,?)''', (
            registro['produto'],
            registro['data_hora'],
            registro['tempo_limpeza'],
            registro['volume_agua'],
            registro['num_amostras'],
            registro['operador'],
            registro['equipamento']
        ))
        conn.commit()
        conn.close()

    def simular_periodo(self, dias, limpezas_por_dia=3):
        data_inicio = datetime.now()-timedelta(days=dias)
        for dia in range(dias):
            num_limpezas = max(1, int(random.gauss(limpezas_por_dia, 1)))

            for _ in range(num_limpezas):
                produto = random.choice(self.df_medios.index.tolist())
                hora = random.randint(6,22)
                minuto = random.randint(0,59)
                data_limpeza = data_inicio + timedelta(
                    days=dia, 
                    hours=hora,
                    minutes=minuto
                )

                registro = self.simular_limpeza(produto, data_limpeza)
                self.salvar_no_banco(registro)

    def ler_banco(self, query="SELECT * FROM registros_limpeza"):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
        