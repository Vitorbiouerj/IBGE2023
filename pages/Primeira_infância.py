import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para modo wide
st.set_page_config(layout="wide")
st.title("Distribuição de Auxílios a Famílias com Crianças na Educação Infantil")

# Carregar os dados
primeira_infancia = pd.read_csv('csv/primeira_infancias_limpo.csv')

# Dicionário de regiões
ufs = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA', 'Ceará': 'CE',
    'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO', 'Maranhão': 'MA', 'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG', 'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR',
    'Pernambuco': 'PE', 'Piauí': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC', 'São Paulo': 'SP', 'Sergipe': 'SE', 'Tocantins': 'TO'
}

regioes = {
    'AC': 'Norte', 'AL': 'Nordeste', 'AP': 'Norte', 'AM': 'Norte', 'BA': 'Nordeste', 'CE': 'Nordeste',
    'DF': 'Centro-Oeste', 'ES': 'Sudeste', 'GO': 'Centro-Oeste', 'MA': 'Nordeste', 'MT': 'Centro-Oeste',
    'MS': 'Centro-Oeste', 'MG': 'Sudeste', 'PA': 'Norte', 'PB': 'Nordeste', 'PR': 'Sul', 'PE': 'Nordeste',
    'PI': 'Nordeste', 'RJ': 'Sudeste', 'RN': 'Nordeste', 'RS': 'Sul', 'RO': 'Norte', 'RR': 'Norte', 'SC': 'Sul',
    'SP': 'Sudeste', 'SE': 'Nordeste', 'TO': 'Norte'
}

# Criar colunas categóricas
primeira_infancia['Sem Auxílio'] = primeira_infancia['aux_a_fam_criancas_ed_inf'] == False

# Selecionar colunas relevantes e renomear para legendas mais amigáveis
categorias = {
    'Sem Auxílio': 'Sem Auxílio',
    'Aux_creche_em_Dinheiro': 'Dinheiro',
    'Aux_creche_em_Bolsa de estudo': 'Bolsa de Estudo',
    'Aux_creche_em_Vaga adquirida pelo governo': 'Vaga Pública',
    'Aux_creche_em_Outro': 'Outro'
}

# Converter colunas para float
for col in categorias.keys():
    primeira_infancia[col] = primeira_infancia[col].astype(float)

# Adicionar colunas de sigla da UF e Região
primeira_infancia['UF_Sigla'] = primeira_infancia['UF'].map(ufs)
primeira_infancia['Regiao'] = primeira_infancia['UF_Sigla'].map(regioes)

# Criar opção de exibição
modo_exibicao = st.selectbox("Selecione o modo de exibição", ["Absoluto", "Percentual"])

# Função para calcular os dados agregados
def calcular_agrupado(df, coluna_agrupamento):
    agrupado = df.groupby(coluna_agrupamento)[list(categorias.keys())].sum().reset_index()
    if modo_exibicao == "Percentual":
        agrupado[list(categorias.keys())] = agrupado[list(categorias.keys())].div(agrupado[list(categorias.keys())].sum(axis=1), axis=0) * 100
    return agrupado.rename(columns=categorias)

# Gráfico Brasil por Região
df_regiao = calcular_agrupado(primeira_infancia, 'Regiao')
st.plotly_chart(px.bar(df_regiao, x='Regiao', y=list(categorias.values()), barmode='stack',
                       title='Distribuição dos Auxílios por Região',
                       labels={'value': 'Porcentagem' if modo_exibicao == "Percentual" else "Quantidade"}))

# Gráfico Brasil por UF
df_uf = calcular_agrupado(primeira_infancia, 'UF')
st.plotly_chart(px.bar(df_uf, x='UF', y=list(categorias.values()), barmode='stack',
                       title='Distribuição dos Auxílios por UF',
                       labels={'value': 'Porcentagem' if modo_exibicao == "Percentual" else "Quantidade"}))

# Seleção de Região
regiao_selecionada = st.selectbox("Selecione uma Região", df_regiao['Regiao'].dropna().unique())

# Gráfico da Região Selecionada
df_filtro = primeira_infancia[primeira_infancia['Regiao'] == regiao_selecionada]
df_filtro_uf = calcular_agrupado(df_filtro, 'UF')
st.plotly_chart(px.bar(df_filtro_uf, x='UF', y=list(categorias.values()), barmode='stack',
                       title=f'Distribuição dos Auxílios na Região {regiao_selecionada}',
                       labels={'value': 'Porcentagem' if modo_exibicao == "Percentual" else "Quantidade"}))