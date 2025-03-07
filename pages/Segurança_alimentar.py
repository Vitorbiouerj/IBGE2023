import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página para modo wide
st.set_page_config(layout="wide")
st.title("Segurança Alimentar")

# Carregar os dados
seguranca_alimentar = pd.read_csv('csv/seguranca_alimentar_limpo.csv')

# Lista das colunas a serem removidas
colunas_para_remover = [
    "CaracOrgGest_SecSetor_AssoSubor_Assistencia_social",
    "CaracOrgGest_SecSetor_AssoSubor_Agricultura",
    "CaracOrgGest_SecSetor_AssoSubor_Planejamento",
    "CaracOrgGest_SecSetor_AssoSubor_Saude",
    "CaracOrgGest_SecSetor_AssoSubor_Direitos_humanos",
    "CaracOrgGest_SecSetor_AssoSubor_Outra",
    "ConsMunSegAli_Ano_de_criacao",
    "ConsMunSegAli_O_conselho_esta",
    "ConsMunSegAli_Formacao",
    "ConsMunSegAli_Quantidade_de_reunioes_(presenciais_ou_remotas)_nos_ultimos_12_meses",
    "ConsMunSegAli_Numero_de_conselheiros_(titulares_e_suplentes)",
    "ConsMunSegAli_Deliberativo"
]

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

# Removendo as colunas
seguranca_alimentar = seguranca_alimentar.drop(columns=colunas_para_remover)

# Dicionário de mapeamento dos valores
mapeamento = {
    True: "Sim",
    False: "Não",
    np.nan: "Não Disponível",
    "Não informou": "Não Disponível"
}

# Aplicando a transformação nas colunas especificadas
colunas_para_transformar = [
    "Lei_municipal_de_seguranca_alimentar__existencia",
    "ConsMunSegAli__existencia",
    "ConsMunSegAli_Consultivo",
    "ConsMunSegAli_Normativo",
    "ConsMunSegAli_Fiscalizador",
    "Plano_de_seguranca_alimentar__existencia",
    "Recursos_orcamentarios_municipais_previstos_para_o_financiamento_da_politica__Seg_Ali"
]

seguranca_alimentar[colunas_para_transformar] = seguranca_alimentar[colunas_para_transformar].replace(mapeamento)

# Criando um mapeamento entre os nomes dos estados e as regiões
seguranca_alimentar["Regiao"] = seguranca_alimentar["UF"].map(lambda x: regioes.get(ufs.get(x, ""), "Desconhecido"))

# Verificando se a coluna foi criada corretamente
if "Regiao" not in seguranca_alimentar.columns:
    st.error("Erro: A coluna 'Regiao' não foi criada corretamente.")
else:
    # Criando menus dropdown
    opcao_valor = st.selectbox("Escolha o tipo de valor:", ["Absoluto", "Percentual"])

    # Definição de cores fixas para as categorias
    cores_personalizadas = {"Sim": "#2ca02c", "Não": "#d62728", "Não Disponível": "#7f7f7f"}

    # Contagem de conselhos por região
    df_regiao = seguranca_alimentar.groupby(["Regiao", "ConsMunSegAli__existencia"]).size().reset_index(name="Contagem")

    # Convertendo para percentual se selecionado
    if opcao_valor == "Percentual":
        df_regiao["Contagem"] = df_regiao.groupby("Regiao")["Contagem"].transform(lambda x: x / x.sum() * 100)

    # Criando o gráfico da distribuição por região
    fig_regiao = px.bar(
        df_regiao,
        x="Regiao",
        y="Contagem",
        color="ConsMunSegAli__existencia",
        title="Distribuição da Existência de Conselhos Municipais de Segurança Alimentar por Região",
        labels={
            "Regiao": "Região",
            "Contagem": "Quantidade" if opcao_valor == "Absoluto" else "Percentual",
            "ConsMunSegAli__existencia": "Existência de um Conselho Municipal para Segurança Alimentar"
        },
        color_discrete_map=cores_personalizadas,
        barmode="stack"
    )

    st.plotly_chart(fig_regiao, use_container_width=True)

    # Menu dropdown para selecionar a região
    regiao_selecionada = st.selectbox("Escolha uma região:", df_regiao["Regiao"].unique())

    # Filtrando dados para a região escolhida
    df_uf = seguranca_alimentar[seguranca_alimentar["Regiao"] == regiao_selecionada]
    df_uf = df_uf.groupby(["UF", "ConsMunSegAli__existencia"]).size().reset_index(name="Contagem")

    # Convertendo para percentual se selecionado
    if opcao_valor == "Percentual":
        df_uf["Contagem"] = df_uf.groupby("UF")["Contagem"].transform(lambda x: x / x.sum() * 100)

    # Criando o gráfico da distribuição por UF dentro da região escolhida
    fig_uf = px.bar(
        df_uf,
        x="UF",
        y="Contagem",
        color="ConsMunSegAli__existencia",
        title=f"Distribuição da Existência de Conselhos Municipais de Segurança Alimentar na Região {regiao_selecionada}",
        labels={
            "UF": "Unidade Federativa",
            "Contagem": "Quantidade" if opcao_valor == "Absoluto" else "Percentual",
            "ConsMunSegAli__existencia": "Existência de um Conselho Municipal para Segurança Alimentar"
        },
        color_discrete_map=cores_personalizadas,
        barmode="stack"
    )

    st.plotly_chart(fig_uf, use_container_width=True)

################################################################################################################

# ---------------------------------------------------------------
# SEÇÃO 1: GRÁFICO NACIONAL (SEPARADO POR REGIÃO)
st.markdown("---")
st.header("Distribuição Nacional das Funções dos Conselhos Municipais de Segurança Alimentar")
st.markdown("As diferenças no valores percentuais de 'Não Disponível' se deve ao fato de que existem municípios que possuem Conselhos, mas não foi informado se eles são consultivos, normativos ou fiscalizadores")
# Criando menu dropdown para selecionar o tipo de valor (afeta todos os gráficos abaixo)
opcao_valor_global = st.selectbox("Escolha o tipo de valor:", ["Absoluto", "Percentual"], key="opcao_global")

# Criando DataFrame para gráfico nacional
df_nacional_funcoes = seguranca_alimentar[["Regiao", "ConsMunSegAli__existencia",
                                           "ConsMunSegAli_Consultivo",
                                           "ConsMunSegAli_Normativo",
                                           "ConsMunSegAli_Fiscalizador"]].copy()

# Garantindo que "Não Disponível" seja consistente e conte APENAS onde "ConsMunSegAli__existencia" for "Não Disponível"
df_nacional_funcoes["Não Disponível"] = df_nacional_funcoes["ConsMunSegAli__existencia"].apply(lambda x: 1 if x == "Não Disponível" else 0)

# Contabilizando apenas os "Sim" nas colunas de interesse
df_nacional_funcoes["Consultivo"] = df_nacional_funcoes["ConsMunSegAli_Consultivo"].apply(lambda x: 1 if x == "Sim" else 0)
df_nacional_funcoes["Normativo"] = df_nacional_funcoes["ConsMunSegAli_Normativo"].apply(lambda x: 1 if x == "Sim" else 0)
df_nacional_funcoes["Fiscalizador"] = df_nacional_funcoes["ConsMunSegAli_Fiscalizador"].apply(lambda x: 1 if x == "Sim" else 0)

# Agrupando por região e somando os valores
df_nacional_funcoes = df_nacional_funcoes.groupby("Regiao")[["Consultivo", "Normativo", "Fiscalizador", "Não Disponível"]].sum().reset_index()

# Convertendo para percentual **dentro de cada região**
if opcao_valor_global == "Percentual":
    df_nacional_funcoes.iloc[:, 1:] = df_nacional_funcoes.iloc[:, 1:].div(df_nacional_funcoes.iloc[:, 1:].sum(axis=1), axis=0) * 100

# Criando o gráfico do Brasil separado por região
fig_nacional_funcoes = px.bar(
    df_nacional_funcoes,
    x="Regiao",
    y=["Consultivo", "Normativo", "Fiscalizador", "Não Disponível"],
    title="Distribuição Nacional das Funções dos Conselhos Municipais de Segurança Alimentar",
    labels={"value": "Quantidade" if opcao_valor_global == "Absoluto" else "Percentual (%)"},
    color_discrete_map={"Consultivo": "#1f77b4", "Normativo": "#ff7f0e", "Fiscalizador": "#2ca02c", "Não Disponível": "#7f7f7f"},
    barmode="stack"
)

st.plotly_chart(fig_nacional_funcoes, use_container_width=True)

# ---------------------------------------------------------------
# SEÇÃO 2: GRÁFICO POR REGIÃO (SEPARADO POR UF)
st.markdown("---")
st.header("Distribuição das Funções dos Conselhos Municipais de Segurança Alimentar por UF")

# Criando menu dropdown para selecionar a região
regiao_selecionada = st.selectbox("Escolha uma região:", df_nacional_funcoes["Regiao"].unique(), key="regiao_uf")

# Criando DataFrame apenas com as colunas de interesse
df_funcoes_uf = seguranca_alimentar[["Regiao", "UF", "ConsMunSegAli__existencia",
                                     "ConsMunSegAli_Consultivo",
                                     "ConsMunSegAli_Normativo",
                                     "ConsMunSegAli_Fiscalizador"]].copy()

# Filtrando os dados para a região escolhida
df_funcoes_uf = df_funcoes_uf[df_funcoes_uf["Regiao"] == regiao_selecionada]

# Garantindo que "Não Disponível" seja consistente e conte APENAS onde "ConsMunSegAli__existencia" for "Não Disponível"
df_funcoes_uf["Não Disponível"] = df_funcoes_uf["ConsMunSegAli__existencia"].apply(lambda x: 1 if x == "Não Disponível" else 0)

# Contabilizando apenas os "Sim" nas colunas de interesse
df_funcoes_uf["Consultivo"] = df_funcoes_uf["ConsMunSegAli_Consultivo"].apply(lambda x: 1 if x == "Sim" else 0)
df_funcoes_uf["Normativo"] = df_funcoes_uf["ConsMunSegAli_Normativo"].apply(lambda x: 1 if x == "Sim" else 0)
df_funcoes_uf["Fiscalizador"] = df_funcoes_uf["ConsMunSegAli_Fiscalizador"].apply(lambda x: 1 if x == "Sim" else 0)

# Agrupando por UF e somando os valores
df_uf_funcoes = df_funcoes_uf.groupby("UF")[["Consultivo", "Normativo", "Fiscalizador", "Não Disponível"]].sum().reset_index()

# Convertendo para percentual **dentro de cada UF**
if opcao_valor_global == "Percentual":
    df_uf_funcoes.iloc[:, 1:] = df_uf_funcoes.iloc[:, 1:].div(df_uf_funcoes.iloc[:, 1:].sum(axis=1), axis=0) * 100

# Criando o gráfico de barras empilhadas por UF dentro da região selecionada
fig_uf_funcoes = px.bar(
    df_uf_funcoes,
    x="UF",
    y=["Consultivo", "Normativo", "Fiscalizador", "Não Disponível"],
    title=f"Distribuição das Funções dos Conselhos Municipais de Segurança Alimentar na Região {regiao_selecionada}",
    labels={"value": "Quantidade" if opcao_valor_global == "Absoluto" else "Percentual (%)"},
    color_discrete_map={"Consultivo": "#1f77b4", "Normativo": "#ff7f0e", "Fiscalizador": "#2ca02c", "Não Disponível": "#7f7f7f"},
    barmode="stack"
)

st.plotly_chart(fig_uf_funcoes, use_container_width=True)

