import streamlit as st
import plotly.express as px
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

def gerar_grafico(df, nivel, titulo):
    df = df[df['AssSoc__Escolaridade'].notna() & (df['AssSoc__Escolaridade'] != '-')]
    df_contagem = df.groupby([nivel, 'AssSoc__Escolaridade']).size().unstack(fill_value=0)
    df_contagem = df_contagem.div(df_contagem.sum(axis=1), axis=0) * 100
    df_contagem = df_contagem.reset_index().melt(id_vars=nivel, var_name='Escolaridade', value_name='Porcentagem')
    fig = px.bar(df_contagem, x=nivel, y='Porcentagem', color='Escolaridade',
                 title=titulo, barmode='stack', category_orders={'Escolaridade': ordem_escolaridade},
                 color_discrete_sequence=cores_personalizadas)
    return fig

def gerar_grafico_formacao(df, nivel, titulo):
    df = df[df['AssSoc__FormNvSup'] != '-']
    df_contagem = df.groupby([nivel, 'AssSoc__FormNvSup']).size().unstack(fill_value=0)
    df_contagem = df_contagem.div(df_contagem.sum(axis=1), axis=0) * 100
    df_contagem = df_contagem.reset_index().melt(id_vars=nivel, var_name='Formação', value_name='Porcentagem')
    fig = px.bar(df_contagem, x=nivel, y='Porcentagem', color='Formação',
                 title=titulo, barmode='stack', color_discrete_sequence=cores_personalizadas)
    return fig

def gerar_grafico_carac_org(df, nivel, titulo):
    df_contagem = df.groupby([nivel, 'AssSoc_CaracOrgGest']).size().unstack(fill_value=0)
    df_contagem = df_contagem.div(df_contagem.sum(axis=1), axis=0) * 100
    df_contagem = df_contagem.reset_index().melt(id_vars=nivel, var_name='AssSoc_CaracOrgGest', value_name='Porcentagem')
    fig = px.bar(df_contagem, x=nivel, y='Porcentagem', color='AssSoc_CaracOrgGest',
                 title=titulo, barmode='stack', color_discrete_sequence=cores_personalizadas)
    return fig

st.title("Distribuição da Escolaridade dos Gestores de Assistência Social")

fig_regiao = gerar_grafico(assistencia_social, 'Região', 'Distribuição de Escolaridade por Região (%)')
st.plotly_chart(fig_regiao)

fig_formacao_regiao = gerar_grafico_formacao(assistencia_social, 'Região', 'Distribuição de Formação Superior por Região (%)')
st.plotly_chart(fig_formacao_regiao)

fig_carac_org_regiao = gerar_grafico_carac_org(assistencia_social, 'Região', 'Distribuição das Características da Organização Gestora por Região (%)')
st.plotly_chart(fig_carac_org_regiao)

fig_uf = gerar_grafico(assistencia_social, 'Sigla', 'Distribuição de Escolaridade por UF (%)')
st.plotly_chart(fig_uf)

fig_formacao_uf = gerar_grafico_formacao(assistencia_social, 'Sigla', 'Distribuição de Formação Superior por UF (%)')
st.plotly_chart(fig_formacao_uf)

fig_carac_org_uf = gerar_grafico_carac_org(assistencia_social, 'Sigla', 'Distribuição das Características da Organização Gestora por UF (%)')
st.plotly_chart(fig_carac_org_uf)

regiao_selecionada = st.selectbox("Selecione uma Região:", ['Todas'] + list(assistencia_social['Região'].dropna().unique()))

df_filtrado = assistencia_social if regiao_selecionada == 'Todas' else assistencia_social[assistencia_social['Região'] == regiao_selecionada]

fig_regiao_uf = gerar_grafico(df_filtrado, 'Sigla', 'Distribuição de Escolaridade por UF dentro de cada Região (%)')
st.plotly_chart(fig_regiao_uf)

fig_formacao_regiao_uf = gerar_grafico_formacao(df_filtrado, 'Sigla', 'Distribuição de Formação Superior por UF dentro de cada Região (%)')
st.plotly_chart(fig_formacao_regiao_uf)

fig_carac_org_regiao_uf = gerar_grafico_carac_org(df_filtrado, 'Sigla', 'Distribuição das Características da Organização Gestora por UF dentro de cada Região (%)')
st.plotly_chart(fig_carac_org_regiao_uf)