import pandas as pd
import sqlite3
import plotly.express as px
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Conexão com o banco de dados
conn = sqlite3.connect("database/simulacao_planta.db")
query = '''SELECT * FROM registros_limpeza'''

df = pd.read_sql(query, conn)
print(df.head())

# Codificação das variáveis categóricas
le = LabelEncoder()

df['operador_encoded'] = le.fit_transform(df['operador'])
df['equipamento_encoded'] = le.fit_transform(df['equipamento'])

operador_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
equipamento_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

print("\nMapeamento de Operadores:", operador_mapping)
print("\nMapeamento de Equipamentos:", equipamento_mapping)

# Preparação dos dados
X = df[['operador_encoded', 'equipamento_encoded', 'num_amostras']]
y = df['volume_agua']

# Modelo RandomForest
model_agua = RandomForestRegressor(n_estimators=100, random_state=42)
model_agua.fit(X, y)

# Feature Importance
importances = model_agua.feature_importances_
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    "Importance": importances
}).sort_values('Importance', ascending=False)

# Visualização com Plotly
fig = px.bar(feature_importance, 
             x='Importance', 
             y='Feature',
             title='Importância das Variáveis para Consumo de Água',
             labels={'Importance': 'Importância', 'Feature': 'Variável'},
             color='Importance',
             color_continuous_scale='Blues')
fig.show()

# Boxplot consumo por operador (Plotly)
fig_box_operador = px.box(df, 
                         x='operador', 
                         y='volume_agua',
                         title='Distribuição de Consumo de Água por Operador',
                         labels={'volume_agua': 'Volume de Água (L)', 'operador': 'Operador'})
fig_box_operador.show()

# Boxplot tempo por equipamento (Plotly)
fig_box_equipamento = px.box(df, 
                            x='equipamento', 
                            y='volume_agua',
                            title='Distribuição de Consumo de Água por Equipamento',
                            labels={'volume_agua': 'Volume de Água (L)', 'equipamento': 'Equipamento'})
fig_box_equipamento.show()

# ANOVA (mantido igual)
print("\nANOVA para Consumo de Água:")
model_agua_anova = ols('volume_agua ~ C(operador) + C(equipamento)', data=df).fit()
anova_agua = sm.stats.anova_lm(model_agua_anova, typ=2)
print(anova_agua)

conn.close()