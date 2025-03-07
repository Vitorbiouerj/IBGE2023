import streamlit as st
import pandas as pd

# Configuração da página para modo wide
st.set_page_config(layout="wide")

# Dicionários fornecidos
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

ordem_escolaridade = [
    'Sem informação', 'Sem gestor', 'Não informou', 'Ensino fundamental incompleto', 'Ensino fundamental completo',
    'Ensino médio incompleto', 'Ensino médio completo', 'Ensino superior incompleto', 'Ensino superior completo',
    'Especialização', 'Mestrado', 'Doutorado'
]

cores_personalizadas = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#1a55FF', '#ffcc00', '#660066', '#008080'
]

# Carregar os dados
assistencia_social = pd.read_csv('csv/assistencia_social_limpo.csv')

assistencia_social = assistencia_social.rename(columns={'AssSoc_CaracOrgGest ': 'AssSoc_CaracOrgGest'})

# Dicionário de substituição
substituicoes = {
    'Ensino médio (2º Grau) completo': 'Ensino médio completo',
    'Ensino fundamental (1º Grau) incompleto': 'Ensino fundamental incompleto',
    'Ensino fundamental ( 1º Grau) completo': 'Ensino fundamental completo',
    'Ensino médio (2º Grau) incompleto': 'Ensino médio incompleto',
    '(**) Sem gestor': 'Sem gestor'
}

# Aplicando as substituições
assistencia_social['AssSoc__Escolaridade'] = assistencia_social['AssSoc__Escolaridade'].replace(substituicoes)

# Adicionar colunas de Sigla e Região
assistencia_social['Sigla'] = assistencia_social['UF'].map(ufs)
assistencia_social['Região'] = assistencia_social['Sigla'].map(regioes)

def gerar_tabela(df, nivel, coluna, titulo):
    df = df[df[coluna].notna() & (df[coluna] != '-')]
    df_contagem = df.groupby([nivel, coluna]).size().unstack(fill_value=0)
    df_contagem = df_contagem.reset_index()
    st.subheader(titulo)
    st.dataframe(df_contagem)

st.title("Distribuição da Escolaridade dos Gestores de Assistência Social - Tabelas")

gerar_tabela(assistencia_social, 'Região', 'AssSoc__Escolaridade', 'Tabela: Escolaridade por Região')
gerar_tabela(assistencia_social, 'Região', 'AssSoc__FormNvSup', 'Tabela: Formação Superior por Região')
gerar_tabela(assistencia_social, 'Região', 'AssSoc_CaracOrgGest', 'Tabela: Características da Organização Gestora por Região')

gerar_tabela(assistencia_social, 'Sigla', 'AssSoc__Escolaridade', 'Tabela: Escolaridade por UF')
gerar_tabela(assistencia_social, 'Sigla', 'AssSoc__FormNvSup', 'Tabela: Formação Superior por UF')
gerar_tabela(assistencia_social, 'Sigla', 'AssSoc_CaracOrgGest', 'Tabela: Características da Organização Gestora por UF')

regiao_selecionada = st.selectbox("Selecione uma Região:", ['Todas'] + list(assistencia_social['Região'].dropna().unique()))

df_filtrado = assistencia_social if regiao_selecionada == 'Todas' else assistencia_social[assistencia_social['Região'] == regiao_selecionada]

gerar_tabela(df_filtrado, 'Sigla', 'AssSoc__Escolaridade', 'Tabela: Escolaridade por UF dentro da Região Selecionada')
gerar_tabela(df_filtrado, 'Sigla', 'AssSoc__FormNvSup', 'Tabela: Formação Superior por UF dentro da Região Selecionada')
gerar_tabela(df_filtrado, 'Sigla', 'AssSoc_CaracOrgGest', 'Tabela: Características da Organização Gestora por UF dentro da Região Selecionada')
