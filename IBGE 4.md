```python
%autosave 20
import pandas as pd
import folium
import geopandas as gpd
import json
import scipy.stats as stats
import numpy as np
import statsmodels.api as sm
```



    Autosaving every 20 seconds



```python
assistencia_social = pd.read_csv('csv/assistencia_social_limpo.csv')
primeira_infancia = pd.read_csv('csv/primeira_infancias_limpo.csv')
seguranca_alimentar = pd.read_csv('csv/seguranca_alimentar_limpo.csv')
```


```python
# Dicionário de substituição
substituicoes = {
    'Ensino médio (2º Grau) completo': 'Ensino médio completo',
    'Ensino fundamental (1º Grau) incompleto': 'Ensino fundamental incompleto',
    'Ensino fundamental ( 1º Grau) completo': 'Ensino fundamental completo',
    'Ensino médio (2º Grau) incompleto': 'Ensino médio incompleto',
    '(**) Sem gestor': 'Sem gestor',
    '-': 'Sem informação'
}

# Aplicando as substituições
assistencia_social['AssSoc__Escolaridade'] = assistencia_social['AssSoc__Escolaridade'].replace(substituicoes)
```


```python
ufs = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapá': 'AP',
    'Amazonas': 'AM',
    'Bahia': 'BA',
    'Ceará': 'CE',
    'Distrito Federal': 'DF',
    'Espírito Santo': 'ES',
    'Goiás': 'GO',
    'Maranhão': 'MA',
    'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG',
    'Pará': 'PA',
    'Paraíba': 'PB',
    'Paraná': 'PR',
    'Pernambuco': 'PE',
    'Piauí': 'PI',
    'Rio de Janeiro': 'RJ',
    'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO',
    'Roraima': 'RR',
    'Santa Catarina': 'SC',
    'São Paulo': 'SP',
    'Sergipe': 'SE',
    'Tocantins': 'TO'
}

regioes = {
    'AC': 'Norte',
    'AL': 'Nordeste',
    'AP': 'Norte',
    'AM': 'Norte',
    'BA': 'Nordeste',
    'CE': 'Nordeste',
    'DF': 'Centro-Oeste',
    'ES': 'Sudeste',
    'GO': 'Centro-Oeste',
    'MA': 'Nordeste',
    'MT': 'Centro-Oeste',
    'MS': 'Centro-Oeste',
    'MG': 'Sudeste',
    'PA': 'Norte',
    'PB': 'Nordeste',
    'PR': 'Sul',
    'PE': 'Nordeste',
    'PI': 'Nordeste',
    'RJ': 'Sudeste',
    'RN': 'Nordeste',
    'RS': 'Sul',
    'RO': 'Norte',
    'RR': 'Norte',
    'SC': 'Sul',
    'SP': 'Sudeste',
    'SE': 'Nordeste',
    'TO': 'Norte'
}
```


```python
colunas_para_remover = ['pop_2023', 'PlanoMun_Por qual instrumento', 'PlanoMun_Ano em que foi elaborado', 'ComiteIntersec_QtdReuniao_12m',
                       'PlanoMun_Foi criada uma Comissão para a elaboração do Plano','ComiteIntersec_SocCivOrganização da Sociedade Civil (OS, OSCIP, associações etc.)', 'ComiteIntersec_SocCivSetor privado', 'ComiteIntersec_SocCivUniversidades',
                       'ComiteIntersec_SocCivCrianças e adolescentes','ComiteIntersec_SocCivOutras áreas']
primeira_infancia = primeira_infancia.drop(columns=colunas_para_remover, errors='ignore')
```


```python
# Lista de colunas a serem convertidas para booleanas
colunas_booleanas = [
    'aux_a_fam_criancas_ed_inf',
    'Aux_creche_em_Dinheiro',
    'Aux_creche_em_Bolsa de estudo',
    'Aux_creche_em_Vaga adquirida pelo governo',
    'Aux_creche_em_Outro',
    'PlanoMun_existe',
    'PlanoMun_regulamentado'
]

# Converter as colunas para booleanas, tratando 'nan' e valores ausentes
for col in colunas_booleanas:
    primeira_infancia[col] = (
        primeira_infancia[col]
        .replace({'True': True, 'False': False, 'nan': pd.NA})  # Converte strings para boolean e trata 'nan'
        .astype('boolean')  # Converte para o tipo booleano do pandas (permite valores nulos)
    )
```


```python
# Criar um mapeamento de UF para região
regioes = {
    "Acre": "Norte", "Amapá": "Norte", "Amazonas": "Norte", "Pará": "Norte", "Rondônia": "Norte", "Roraima": "Norte", "Tocantins": "Norte",
    "Alagoas": "Nordeste", "Bahia": "Nordeste", "Ceará": "Nordeste", "Maranhão": "Nordeste", "Paraíba": "Nordeste", "Pernambuco": "Nordeste", 
    "Piauí": "Nordeste", "Rio Grande do Norte": "Nordeste", "Sergipe": "Nordeste",
    "Distrito Federal": "Centro-Oeste", "Goiás": "Centro-Oeste", "Mato Grosso": "Centro-Oeste", "Mato Grosso do Sul": "Centro-Oeste",
    "Espírito Santo": "Sudeste", "Minas Gerais": "Sudeste", "Rio de Janeiro": "Sudeste", "São Paulo": "Sudeste",
    "Paraná": "Sul", "Rio Grande do Sul": "Sul", "Santa Catarina": "Sul"
}

# Criar um dataframe combinando as duas tabelas com base no código do município
df_merged = assistencia_social.merge(primeira_infancia, on=['Codigo_do_Municipio', 'UF', 'mun'], how='inner')

# Adicionar a região ao dataframe com base na UF
df_merged['Regiao'] = df_merged['UF'].map(regioes)

# Selecionar variáveis relevantes, incluindo a população e a região
df_logit = df_merged[['AssSoc__FormNvSup', 'aux_a_fam_criancas_ed_inf', 'pop_2023', 'Regiao']].copy()

# Remover valores ausentes
df_logit.dropna(inplace=True)

# Remover a categoria "Não informado" da formação do gestor
df_logit = df_logit[df_logit['AssSoc__FormNvSup'] != 'Não informou']

# Determinar a região com maior número de auxílios concedidos
regiao_referencia = df_logit.groupby('Regiao')['aux_a_fam_criancas_ed_inf'].sum().idxmax()
print(f"Região escolhida como referência: {regiao_referencia}")

# Converter a variável categórica 'AssSoc__FormNvSup' em variáveis dummies
df_logit = pd.get_dummies(df_logit, columns=['AssSoc__FormNvSup'], drop_first=True, dtype=int)

# Converter a variável categórica 'Regiao' em variáveis dummies, usando a região de referência automaticamente
df_logit = pd.get_dummies(df_logit, columns=['Regiao'], drop_first=False, dtype=int)

# Remover a região de referência (ela será a base de comparação)
df_logit.drop(columns=[f'Regiao_{regiao_referencia}'], inplace=True)

# Garantir que 'aux_a_fam_criancas_ed_inf' esteja no formato numérico (0 e 1)
df_logit['aux_a_fam_criancas_ed_inf'] = df_logit['aux_a_fam_criancas_ed_inf'].astype(int)

# Normalizar a variável populacional (para evitar problemas de escala na regressão)
df_logit['pop_2023'] = (df_logit['pop_2023'] - df_logit['pop_2023'].mean()) / df_logit['pop_2023'].std()

# Remover colunas com pouca variação (se houver)
df_logit = df_logit.loc[:, df_logit.nunique() > 1]

# Definir variáveis independentes (X) e variável dependente (y)
X = df_logit.drop(columns=['aux_a_fam_criancas_ed_inf'])  # Formação do gestor codificada + pop_2023 + Região
y = df_logit['aux_a_fam_criancas_ed_inf']  # Auxílio (0 ou 1)

# Adicionar constante ao modelo
X = sm.add_constant(X)

# Garantir que todas as colunas sejam numéricas
X = X.apply(pd.to_numeric)
y = y.apply(pd.to_numeric)

# Ajustar o modelo de regressão logística com mais iterações
logit_model = sm.Logit(y, X)
result = logit_model.fit(maxiter=100)  # Aumentando o número de iterações

# Exibir os resultados
print(result.summary())
```

    Região escolhida como referência: Sudeste
    Optimization terminated successfully.
             Current function value: 0.268629
             Iterations 7
                                   Logit Regression Results                              
    =====================================================================================
    Dep. Variable:     aux_a_fam_criancas_ed_inf   No. Observations:                 5562
    Model:                                 Logit   Df Residuals:                     5542
    Method:                                  MLE   Df Model:                           19
    Date:                       Fri, 07 Mar 2025   Pseudo R-squ.:                 0.01616
    Time:                               11:32:01   Log-Likelihood:                -1494.1
    converged:                              True   LL-Null:                       -1518.7
    Covariance Type:                   nonrobust   LLR p-value:                 0.0001789
    =========================================================================================================
                                                coef    std err          z      P>|z|      [0.025      0.975]
    ---------------------------------------------------------------------------------------------------------
    const                                    -2.5286      0.135    -18.713      0.000      -2.793      -2.264
    pop_2023                                  0.0684      0.039      1.732      0.083      -0.009       0.146
    AssSoc__FormNvSup_Administração           0.2553      0.207      1.234      0.217      -0.150       0.661
    AssSoc__FormNvSup_Assistência social     -0.0958      0.155     -0.617      0.538      -0.400       0.209
    AssSoc__FormNvSup_Ciências Contábeis     -0.0401      0.438     -0.092      0.927      -0.898       0.817
    AssSoc__FormNvSup_Direito                 0.4478      0.201      2.223      0.026       0.053       0.843
    AssSoc__FormNvSup_Economia               -0.5534      1.030     -0.537      0.591      -2.573       1.466
    AssSoc__FormNvSup_Enfermagem             -0.6476      0.469     -1.381      0.167      -1.567       0.271
    AssSoc__FormNvSup_Jornalismo              1.1520      0.658      1.752      0.080      -0.137       2.441
    AssSoc__FormNvSup_Medicina                0.9855      0.761      1.295      0.195      -0.506       2.477
    AssSoc__FormNvSup_Nutrição                0.2760      0.537      0.514      0.607      -0.776       1.328
    AssSoc__FormNvSup_Outra                   0.1995      0.161      1.242      0.214      -0.115       0.514
    AssSoc__FormNvSup_Pedagogia               0.0991      0.173      0.572      0.567      -0.240       0.438
    AssSoc__FormNvSup_Psicologia             -0.0333      0.289     -0.115      0.908      -0.599       0.533
    AssSoc__FormNvSup_Sociologia             -0.0909      0.742     -0.123      0.902      -1.545       1.363
    AssSoc__FormNvSup_Terapia ocupacional     0.8363      1.090      0.768      0.443      -1.299       2.972
    Regiao_Centro-Oeste                       0.0011      0.194      0.006      0.995      -0.379       0.381
    Regiao_Nordeste                          -0.3929      0.139     -2.827      0.005      -0.665      -0.121
    Regiao_Norte                              0.1355      0.192      0.707      0.479      -0.240       0.511
    Regiao_Sul                                0.3023      0.134      2.256      0.024       0.040       0.565
    =========================================================================================================



```python
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

# Removendo as colunas
seguranca_alimentar = seguranca_alimentar.drop(columns=colunas_para_remover)
```


```python
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

# Exibindo os valores únicos após a transformação
for coluna in colunas_para_transformar:
    print(f"Valores únicos em '{coluna}':")
    print(seguranca_alimentar[coluna].unique(), "\n")
```

    Valores únicos em 'Lei_municipal_de_seguranca_alimentar__existencia':
    ['Não' 'Sim' 'Não Disponível'] 
    
    Valores únicos em 'ConsMunSegAli__existencia':
    ['Sim' 'Não' 'Não Disponível'] 
    
    Valores únicos em 'ConsMunSegAli_Consultivo':
    ['Não Disponível' 'Sim' 'Não'] 
    
    Valores únicos em 'ConsMunSegAli_Normativo':
    ['Não Disponível' 'Não' 'Sim'] 
    
    Valores únicos em 'ConsMunSegAli_Fiscalizador':
    ['Não Disponível' 'Não' 'Sim'] 
    
    Valores únicos em 'Plano_de_seguranca_alimentar__existencia':
    ['Não' 'Sim' 'Não Disponível'] 
    
    Valores únicos em 'Recursos_orcamentarios_municipais_previstos_para_o_financiamento_da_politica__Seg_Ali':
    ['Não' 'Sim' 'Não Disponível'] 
    



```python
print(assistencia_social.head())
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(assistencia_social.info())
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(primeira_infancia.head())
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(primeira_infancia.info())
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(seguranca_alimentar.head())
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
print(seguranca_alimentar.info())
print(print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'))
```

       Codigo_do_Municipio        UF                    mun  pop_2023  \
    0              1100015  Rondônia  Alta Floresta D'Oeste     21494   
    1              1100023  Rondônia              Ariquemes     96833   
    2              1100031  Rondônia                 Cabixi      5351   
    3              1100049  Rondônia                 Cacoal     86887   
    4              1100056  Rondônia             Cerejeiras     15890   
    
                                    AssSoc_CaracOrgGest  AssSoc__Sexo  \
    0  Secretaria municipal em conjunto com outras po...    Masculino   
    1                     Secretaria municipal exclusiva     Feminino   
    2                     Secretaria municipal exclusiva     Feminino   
    3  Secretaria municipal em conjunto com outras po...     Feminino   
    4                     Secretaria municipal exclusiva    Masculino   
    
      AssSoc__Idade  AssSoc__Cor AssSoc_Perfil do gestor RespostaProprio  \
    0             38       Parda                                     Sim   
    1             36      Branca                                     Não   
    2             53      Branca                                     Não   
    3             42      Branca                                     Sim   
    4             28       Parda                                     Não   
    
           AssSoc__Escolaridade   AssSoc__FormNvSup  
    0     Ensino médio completo                   -  
    1            Especialização           Pedagogia  
    2            Especialização           Pedagogia  
    3  Ensino superior completo  Assistência social  
    4            Especialização  Assistência social  
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5570 entries, 0 to 5569
    Data columns (total 11 columns):
     #   Column                                   Non-Null Count  Dtype 
    ---  ------                                   --------------  ----- 
     0   Codigo_do_Municipio                      5570 non-null   int64 
     1   UF                                       5570 non-null   object
     2   mun                                      5570 non-null   object
     3   pop_2023                                 5570 non-null   int64 
     4   AssSoc_CaracOrgGest                      5570 non-null   object
     5   AssSoc__Sexo                             5570 non-null   object
     6   AssSoc__Idade                            5570 non-null   object
     7   AssSoc__Cor                              5570 non-null   object
     8   AssSoc_Perfil do gestor RespostaProprio  5570 non-null   object
     9   AssSoc__Escolaridade                     5570 non-null   object
     10  AssSoc__FormNvSup                        5570 non-null   object
    dtypes: int64(2), object(9)
    memory usage: 478.8+ KB
    None
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
       Codigo_do_Municipio        UF ComiteIntersec_existência  \
    0              1100015  Rondônia                     False   
    1              1100023  Rondônia                     False   
    2              1100031  Rondônia                     False   
    3              1100049  Rondônia                     False   
    4              1100056  Rondônia                      True   
    
      ComiteIntersec_Mun_Assistência social ComiteIntersec_Mun_Educação  \
    0                                     -                           -   
    1                                     -                           -   
    2                                     -                           -   
    3                                     -                           -   
    4                                   Sim                         Não   
    
      ComiteIntersec_Mun_Saúde ComiteIntersec_Mun_Outras áreas  \
    0                        -                               -   
    1                        -                               -   
    2                        -                               -   
    3                        -                               -   
    4                      Sim                             Não   
    
      ComiteIntersec_Conselho tutelar  \
    0                               -   
    1                               -   
    2                               -   
    3                               -   
    4                             Sim   
    
      ComiteIntersec_Conselho Municipal dos Direitos da criança e do adolescente  \
    0                                                  -                           
    1                                                  -                           
    2                                                  -                           
    3                                                  -                           
    4                                                Sim                           
    
       aux_a_fam_criancas_ed_inf  Aux_creche_em_Dinheiro  \
    0                      False                    <NA>   
    1                      False                    <NA>   
    2                      False                    <NA>   
    3                      False                    <NA>   
    4                      False                    <NA>   
    
       Aux_creche_em_Bolsa de estudo  Aux_creche_em_Vaga adquirida pelo governo  \
    0                           <NA>                                       <NA>   
    1                           <NA>                                       <NA>   
    2                           <NA>                                       <NA>   
    3                           <NA>                                       <NA>   
    4                           <NA>                                       <NA>   
    
       Aux_creche_em_Outro                    mun  PlanoMun_existe  \
    0                 <NA>  Alta Floresta D'Oeste            False   
    1                 <NA>              Ariquemes             True   
    2                 <NA>                 Cabixi            False   
    3                 <NA>                 Cacoal            False   
    4                 <NA>             Cerejeiras            False   
    
       PlanoMun_regulamentado  
    0                    <NA>  
    1                   False  
    2                    <NA>  
    3                    <NA>  
    4                    <NA>  
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5570 entries, 0 to 5569
    Data columns (total 17 columns):
     #   Column                                                                      Non-Null Count  Dtype  
    ---  ------                                                                      --------------  -----  
     0   Codigo_do_Municipio                                                         5570 non-null   int64  
     1   UF                                                                          5570 non-null   object 
     2   ComiteIntersec_existência                                                   5565 non-null   object 
     3   ComiteIntersec_Mun_Assistência social                                       5570 non-null   object 
     4   ComiteIntersec_Mun_Educação                                                 5570 non-null   object 
     5   ComiteIntersec_Mun_Saúde                                                    5570 non-null   object 
     6   ComiteIntersec_Mun_Outras áreas                                             5570 non-null   object 
     7   ComiteIntersec_Conselho tutelar                                             5570 non-null   object 
     8   ComiteIntersec_Conselho Municipal dos Direitos da criança e do adolescente  5570 non-null   object 
     9   aux_a_fam_criancas_ed_inf                                                   5563 non-null   boolean
     10  Aux_creche_em_Dinheiro                                                      432 non-null    boolean
     11  Aux_creche_em_Bolsa de estudo                                               432 non-null    boolean
     12  Aux_creche_em_Vaga adquirida pelo governo                                   432 non-null    boolean
     13  Aux_creche_em_Outro                                                         432 non-null    boolean
     14  mun                                                                         5570 non-null   object 
     15  PlanoMun_existe                                                             5565 non-null   boolean
     16  PlanoMun_regulamentado                                                      1484 non-null   boolean
    dtypes: boolean(7), int64(1), object(9)
    memory usage: 511.4+ KB
    None
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
       Codigo_do_Municipio        UF  pop_2023  \
    0              1100015  Rondônia     21494   
    1              1100023  Rondônia     96833   
    2              1100031  Rondônia      5351   
    3              1100049  Rondônia     86887   
    4              1100056  Rondônia     15890   
    
                                           CaracOrgGest_  \
    0                               Não possui estrutura   
    1               Setor subordinado a outra secretaria   
    2                               Não possui estrutura   
    3  Setor subordinado diretamente à chefia do Exec...   
    4                               Não possui estrutura   
    
      Lei_municipal_de_seguranca_alimentar__existencia ConsMunSegAli__existencia  \
    0                                              Não                       Sim   
    1                                              Sim                       Sim   
    2                                              Não                       Não   
    3                                              Não                       Sim   
    4                                              Não                       Não   
    
      ConsMunSegAli_Consultivo ConsMunSegAli_Normativo ConsMunSegAli_Fiscalizador  \
    0           Não Disponível          Não Disponível             Não Disponível   
    1           Não Disponível          Não Disponível             Não Disponível   
    2           Não Disponível          Não Disponível             Não Disponível   
    3                      Sim                     Não                        Não   
    4           Não Disponível          Não Disponível             Não Disponível   
    
      Plano_de_seguranca_alimentar__existencia  \
    0                                      Não   
    1                                      Sim   
    2                                      Não   
    3                                      Não   
    4                                      Não   
    
      Recursos_orcamentarios_municipais_previstos_para_o_financiamento_da_politica__Seg_Ali  \
    0                                                Não                                      
    1                                                Não                                      
    2                                                Não                                      
    3                                                Sim                                      
    4                                                Não                                      
    
                    Desc_Mun  
    0  Alta Floresta D'Oeste  
    1              Ariquemes  
    2                 Cabixi  
    3                 Cacoal  
    4             Cerejeiras  
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5570 entries, 0 to 5569
    Data columns (total 12 columns):
     #   Column                                                                                 Non-Null Count  Dtype 
    ---  ------                                                                                 --------------  ----- 
     0   Codigo_do_Municipio                                                                    5570 non-null   int64 
     1   UF                                                                                     5570 non-null   object
     2   pop_2023                                                                               5570 non-null   int64 
     3   CaracOrgGest_                                                                          5570 non-null   object
     4   Lei_municipal_de_seguranca_alimentar__existencia                                       5570 non-null   object
     5   ConsMunSegAli__existencia                                                              5570 non-null   object
     6   ConsMunSegAli_Consultivo                                                               5570 non-null   object
     7   ConsMunSegAli_Normativo                                                                5570 non-null   object
     8   ConsMunSegAli_Fiscalizador                                                             5570 non-null   object
     9   Plano_de_seguranca_alimentar__existencia                                               5570 non-null   object
     10  Recursos_orcamentarios_municipais_previstos_para_o_financiamento_da_politica__Seg_Ali  5570 non-null   object
     11  Desc_Mun                                                                               5570 non-null   object
    dtypes: int64(2), object(10)
    memory usage: 522.3+ KB
    None
    
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    None



```python
# Realizando merge entre Primeira Infância e Segurança Alimentar usando o Código do Município como chave
df_merged_pi_sa = primeira_infancia.merge(seguranca_alimentar, on=['Codigo_do_Municipio', 'UF'], how='inner')

# Exibir informações básicas para verificar o merge
print(df_merged_pi_sa.info())
print(df_merged_pi_sa.head())
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5570 entries, 0 to 5569
    Data columns (total 27 columns):
     #   Column                                                                                 Non-Null Count  Dtype  
    ---  ------                                                                                 --------------  -----  
     0   Codigo_do_Municipio                                                                    5570 non-null   int64  
     1   UF                                                                                     5570 non-null   object 
     2   ComiteIntersec_existência                                                              5565 non-null   object 
     3   ComiteIntersec_Mun_Assistência social                                                  5570 non-null   object 
     4   ComiteIntersec_Mun_Educação                                                            5570 non-null   object 
     5   ComiteIntersec_Mun_Saúde                                                               5570 non-null   object 
     6   ComiteIntersec_Mun_Outras áreas                                                        5570 non-null   object 
     7   ComiteIntersec_Conselho tutelar                                                        5570 non-null   object 
     8   ComiteIntersec_Conselho Municipal dos Direitos da criança e do adolescente             5570 non-null   object 
     9   aux_a_fam_criancas_ed_inf                                                              5563 non-null   boolean
     10  Aux_creche_em_Dinheiro                                                                 432 non-null    boolean
     11  Aux_creche_em_Bolsa de estudo                                                          432 non-null    boolean
     12  Aux_creche_em_Vaga adquirida pelo governo                                              432 non-null    boolean
     13  Aux_creche_em_Outro                                                                    432 non-null    boolean
     14  mun                                                                                    5570 non-null   object 
     15  PlanoMun_existe                                                                        5565 non-null   boolean
     16  PlanoMun_regulamentado                                                                 1484 non-null   boolean
     17  pop_2023                                                                               5570 non-null   int64  
     18  CaracOrgGest_                                                                          5570 non-null   object 
     19  Lei_municipal_de_seguranca_alimentar__existencia                                       5570 non-null   object 
     20  ConsMunSegAli__existencia                                                              5570 non-null   object 
     21  ConsMunSegAli_Consultivo                                                               5570 non-null   object 
     22  ConsMunSegAli_Normativo                                                                5570 non-null   object 
     23  ConsMunSegAli_Fiscalizador                                                             5570 non-null   object 
     24  Plano_de_seguranca_alimentar__existencia                                               5570 non-null   object 
     25  Recursos_orcamentarios_municipais_previstos_para_o_financiamento_da_politica__Seg_Ali  5570 non-null   object 
     26  Desc_Mun                                                                               5570 non-null   object 
    dtypes: boolean(7), int64(2), object(18)
    memory usage: 946.6+ KB
    None
       Codigo_do_Municipio        UF ComiteIntersec_existência  \
    0              1100015  Rondônia                     False   
    1              1100023  Rondônia                     False   
    2              1100031  Rondônia                     False   
    3              1100049  Rondônia                     False   
    4              1100056  Rondônia                      True   
    
      ComiteIntersec_Mun_Assistência social ComiteIntersec_Mun_Educação  \
    0                                     -                           -   
    1                                     -                           -   
    2                                     -                           -   
    3                                     -                           -   
    4                                   Sim                         Não   
    
      ComiteIntersec_Mun_Saúde ComiteIntersec_Mun_Outras áreas  \
    0                        -                               -   
    1                        -                               -   
    2                        -                               -   
    3                        -                               -   
    4                      Sim                             Não   
    
      ComiteIntersec_Conselho tutelar  \
    0                               -   
    1                               -   
    2                               -   
    3                               -   
    4                             Sim   
    
      ComiteIntersec_Conselho Municipal dos Direitos da criança e do adolescente  \
    0                                                  -                           
    1                                                  -                           
    2                                                  -                           
    3                                                  -                           
    4                                                Sim                           
    
       aux_a_fam_criancas_ed_inf  ...  pop_2023  \
    0                      False  ...     21494   
    1                      False  ...     96833   
    2                      False  ...      5351   
    3                      False  ...     86887   
    4                      False  ...     15890   
    
                                           CaracOrgGest_  \
    0                               Não possui estrutura   
    1               Setor subordinado a outra secretaria   
    2                               Não possui estrutura   
    3  Setor subordinado diretamente à chefia do Exec...   
    4                               Não possui estrutura   
    
       Lei_municipal_de_seguranca_alimentar__existencia  \
    0                                               Não   
    1                                               Sim   
    2                                               Não   
    3                                               Não   
    4                                               Não   
    
       ConsMunSegAli__existencia ConsMunSegAli_Consultivo  \
    0                        Sim           Não Disponível   
    1                        Sim           Não Disponível   
    2                        Não           Não Disponível   
    3                        Sim                      Sim   
    4                        Não           Não Disponível   
    
       ConsMunSegAli_Normativo  ConsMunSegAli_Fiscalizador  \
    0           Não Disponível              Não Disponível   
    1           Não Disponível              Não Disponível   
    2           Não Disponível              Não Disponível   
    3                      Não                         Não   
    4           Não Disponível              Não Disponível   
    
       Plano_de_seguranca_alimentar__existencia  \
    0                                       Não   
    1                                       Sim   
    2                                       Não   
    3                                       Não   
    4                                       Não   
    
      Recursos_orcamentarios_municipais_previstos_para_o_financiamento_da_politica__Seg_Ali  \
    0                                                Não                                      
    1                                                Não                                      
    2                                                Não                                      
    3                                                Sim                                      
    4                                                Não                                      
    
                    Desc_Mun  
    0  Alta Floresta D'Oeste  
    1              Ariquemes  
    2                 Cabixi  
    3                 Cacoal  
    4             Cerejeiras  
    
    [5 rows x 27 columns]



```python
# Correlação entre existência de Plano Municipal de Primeira Infância e Plano de Segurança Alimentar
contingencia_pm_sa = pd.crosstab(df_merged_pi_sa['PlanoMun_existe'], df_merged_pi_sa['Plano_de_seguranca_alimentar__existencia'])

# Teste qui-quadrado para verificar associação estatística
chi2, p, dof, expected = stats.chi2_contingency(contingencia_pm_sa)

print("Tabela de contingência - Plano Municipal vs. Segurança Alimentar:")
print(contingencia_pm_sa)
print("\nResultado do Teste Qui-Quadrado:")
print(f"Qui-quadrado: {chi2:.3f}, p-valor: {p:.5f}")
```

    Tabela de contingência - Plano Municipal vs. Segurança Alimentar:
    Plano_de_seguranca_alimentar__existencia   Não  Não Disponível  Sim
    PlanoMun_existe                                                    
    False                                     3361               1  719
    True                                      1154               2  328
    
    Resultado do Teste Qui-Quadrado:
    Qui-quadrado: 16.917, p-valor: 0.00021



```python
# Importar biblioteca adicional para V de Cramér
from scipy.stats import chi2_contingency
import numpy as np

# Cálculo do qui-quadrado e do V de Cramér
def cramers_v(chi2, n, k):
    return np.sqrt(chi2 / (n * (k - 1)))

# Criar tabela de contingência
contingencia_pm_sa = pd.crosstab(df_merged_pi_sa['PlanoMun_existe'], df_merged_pi_sa['Plano_de_seguranca_alimentar__existencia'])

# Aplicar teste qui-quadrado
chi2, p, dof, expected = chi2_contingency(contingencia_pm_sa)

# Número total de observações
n = np.sum(contingencia_pm_sa.values)

# Número de categorias da variável com menor quantidade de níveis
k = min(contingencia_pm_sa.shape)

# Calcular V de Cramér
v_cramer = cramers_v(chi2, n, k)

print(f"V de Cramér: {v_cramer:.3f} (Força da Associação)")
```

    V de Cramér: 0.055 (Força da Associação)



```python
# Interpretação da força da associação para tabelas 2x2:
if v_cramer < 0.10:
    interpretacao = "Associação muito fraca"
elif v_cramer < 0.20:
    interpretacao = "Associação fraca"
elif v_cramer < 0.30:
    interpretacao = "Associação moderada"
else:
    interpretacao = "Associação forte"

print(f"Interpretação: {interpretacao}")
```

    Interpretação: Associação muito fraca



```python

```


```python

```


```python

```


```python

```

Parar análise aqui


```python
# Correlação entre existência de Comitê Intersetorial e Lei Municipal de Segurança Alimentar
contingencia_ci_lei = pd.crosstab(df_merged_pi_sa['ComiteIntersec_existência'], df_merged_pi_sa['Lei_municipal_de_seguranca_alimentar__existencia'])

# Teste qui-quadrado para verificar associação estatística
chi2, p, dof, expected = stats.chi2_contingency(contingencia_ci_lei)

print("Tabela de contingência - Comitê Intersetorial vs. Lei Municipal de Segurança Alimentar:")
print(contingencia_ci_lei)
print("\nResultado do Teste Qui-Quadrado:")
print(f"Qui-quadrado: {chi2:.3f}, p-valor: {p:.5f}")
```

    Tabela de contingência - Comitê Intersetorial vs. Lei Municipal de Segurança Alimentar:
    Lei_municipal_de_seguranca_alimentar__existencia   Não  Não Disponível   Sim
    ComiteIntersec_existência                                                   
    False                                             2537               1  1073
    True                                              1190               2   762
    
    Resultado do Teste Qui-Quadrado:
    Qui-quadrado: 51.015, p-valor: 0.00000



```python
# Certificar-se de que 'ComiteIntersec_existência' está no formato correto
# Substituir NaN por 0 (assumindo que NaN significa "não informado" e tratando como "Não")
df_corr['ComiteIntersec_existência'] = df_corr['ComiteIntersec_existência'].fillna(0).astype(int)
```


```python
# Calculando correlação de Pearson corrigida
correlacoes = df_corr[['Plano_de_seguranca_alimentar__existencia', 'Lei_municipal_de_seguranca_alimentar__existencia', 'ComiteIntersec_existência']].corr()

print("Matriz de Correlação entre Comitê Intersetorial e Segurança Alimentar:")
print(correlacoes)
```

    Matriz de Correlação entre Comitê Intersetorial e Segurança Alimentar:
                                                      Plano_de_seguranca_alimentar__existencia  \
    Plano_de_seguranca_alimentar__existencia                                          1.000000   
    Lei_municipal_de_seguranca_alimentar__existencia                                  0.305186   
    ComiteIntersec_existência                                                         0.044628   
    
                                                      Lei_municipal_de_seguranca_alimentar__existencia  \
    Plano_de_seguranca_alimentar__existencia                                                  0.305186   
    Lei_municipal_de_seguranca_alimentar__existencia                                          1.000000   
    ComiteIntersec_existência                                                                 0.094416   
    
                                                      ComiteIntersec_existência  
    Plano_de_seguranca_alimentar__existencia                           0.044628  
    Lei_municipal_de_seguranca_alimentar__existencia                   0.094416  
    ComiteIntersec_existência                                          1.000000  



```python

```
