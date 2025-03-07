import pandas as pd
import streamlit as st
import plotly.express as px

# Configurar o modo wide
st.set_page_config(layout="wide")

# Carregar o dataset
assistencia_social = pd.read_csv('csv/assistencia_social_limpo.csv')

# Limpeza e processamento dos dados
assistencia_social.columns = assistencia_social.columns.str.strip()
mapeamento = {
    'Masculino': True,
    'Feminino': False,
    '(**) Sem gestor': pd.NA,
    '-': pd.NA
}
assistencia_social['AssSoc__Sexo'] = assistencia_social['AssSoc__Sexo'].map(mapeamento).astype("boolean")

# Criar o DataFrame com as regiões e suas respectivas UFs (nomes completos)
regioes_ufs = {
    "UF": [
        "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal", "Espírito Santo",
        "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba",
        "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul",
        "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
    ],
    "Regiao": [
        "Norte", "Nordeste", "Norte", "Norte", "Nordeste", "Nordeste", "Centro-Oeste",
        "Sudeste", "Centro-Oeste", "Nordeste", "Centro-Oeste", "Centro-Oeste", "Sudeste",
        "Norte", "Nordeste", "Sul", "Nordeste", "Nordeste", "Sudeste", "Nordeste",
        "Sul", "Norte", "Norte", "Sul", "Sudeste", "Nordeste", "Centro-Oeste"
    ]
}

# Criar DataFrame de Regiões e UFs
regioes_df = pd.DataFrame(regioes_ufs)

# Mesclar o DataFrame de regiões com o assistencia_social
assistencia_social['UF'] = assistencia_social['UF'].replace({
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo",
    "SE": "Sergipe", "TO": "Tocantins"
})

assistencia_social = pd.merge(assistencia_social, regioes_df, on='UF', how='left')

# Filtrar apenas os dados válidos
assistencia_social_validos = assistencia_social.dropna(subset=['AssSoc__Sexo'])

# Contagem de valores por região e sexo
region_data = assistencia_social_validos.groupby(['Regiao', 'AssSoc__Sexo']).size().unstack(fill_value=0)
region_data['Total'] = region_data[True] + region_data[False]
region_data['Porcentagem Masculina'] = ((region_data[True] / region_data['Total']) * 100).round(2)
region_data['Porcentagem Feminina'] = ((region_data[False] / region_data['Total']) * 100).round(2)
region_data.reset_index(inplace=True)

# Contagem de valores por UF e sexo
uf_data = assistencia_social_validos.groupby(['UF', 'AssSoc__Sexo']).size().unstack(fill_value=0)
uf_data['Total'] = uf_data[True] + uf_data[False]
uf_data['Porcentagem Masculina'] = ((uf_data[True] / uf_data['Total']) * 100).round(2)
uf_data['Porcentagem Feminina'] = ((uf_data[False] / uf_data['Total']) * 100).round(2)
uf_data.reset_index(inplace=True)


# Função para plotar gráficos interativos
def plot_graph(df, title, x_column):
    df_melted = df.melt(id_vars=[x_column], value_vars=['Porcentagem Masculina', 'Porcentagem Feminina'],
                        var_name='Sexo', value_name='Porcentagem')
    df_melted['Sexo'] = df_melted['Sexo'].map({
        'Porcentagem Masculina': 'Masculino',
        'Porcentagem Feminina': 'Feminino'
    })

    fig = px.bar(df_melted, x=x_column, y='Porcentagem', color='Sexo', barmode='stack',
                 title=title, labels={'Porcentagem': 'Porcentagem (%)', x_column: x_column},
                 text_auto='.2f', height=600, hover_data={x_column: True, 'Sexo': True, 'Porcentagem': True})
    fig.update_traces(marker_line_width=1.5, marker_line_color='black')
    fig.update_layout(font=dict(size=14), hoverlabel=dict(font_size=14, font_family='Arial'))
    st.plotly_chart(fig)


# Layout do Streamlit
st.title('Distribuição de Gestores das Secretarias de Assistência Social por Sexo')
st.header('Distribuição por Região')
plot_graph(region_data, 'Distribuição de Homens e Mulheres por Região', 'Regiao')

# Adicionar gráfico para todas as UFs
st.header('Distribuição por Unidade Federativa (UF)')
plot_graph(uf_data, 'Distribuição de Homens e Mulheres por UF', 'UF')

# Menu Dropdown para seleção de Região
region_select = st.selectbox('Selecione uma Região', region_data['Regiao'].unique())

# Filtrar os dados para a região selecionada
selected_data = assistencia_social_validos[assistencia_social_validos['Regiao'] == region_select]
uf_region_data = selected_data.groupby('UF')['AssSoc__Sexo'].value_counts().unstack(fill_value=0)
uf_region_data['Total'] = uf_region_data[True] + uf_region_data[False]
uf_region_data['Porcentagem Masculina'] = ((uf_region_data[True] / uf_region_data['Total']) * 100).round(2)
uf_region_data['Porcentagem Feminina'] = ((uf_region_data[False] / uf_region_data['Total']) * 100).round(2)
uf_region_data.reset_index(inplace=True)

# Plotar gráfico para a UF selecionada
st.header(f'Distribuição em {region_select}')
plot_graph(uf_region_data, f'Distribuição de Homens e Mulheres em {region_select}', 'UF')
