# Análise da Relação entre a Existência de Comitês Intersetoriais de Assistência Social e a Presença de um Plano Municipal de Segurança Alimentar

## 1. Introdução

A segurança alimentar é um dos pilares fundamentais para o bem-estar social e a saúde da população. No Brasil, garantir que todas as pessoas tenham acesso regular e permanente a alimentos de qualidade, em quantidade suficiente e de forma sustentável, é um desafio enfrentado pelos governos municipais, estaduais e federal. Para estruturar ações nessa área, muitos municípios adotam **Planos Municipais de Segurança Alimentar**, que regulamentam políticas públicas voltadas à nutrição e ao combate à fome.

Paralelamente, diversos municípios também implementam **Comitês Intersetoriais de Assistência Social**, órgãos que coordenam políticas sociais, buscando promover maior integração entre diferentes setores da administração pública. A ideia por trás desses comitês é que, ao reunir representantes de áreas como saúde, educação, assistência social e segurança alimentar, as ações governamentais possam ser mais eficazes, melhorando o atendimento à população e otimizando os recursos públicos.

Diante disso, este estudo busca responder à seguinte questão: **municípios que possuem Comitês Intersetoriais de Assistência Social são mais propensos a adotar um Plano Municipal de Segurança Alimentar?** Além disso, outros fatores, como a existência de Conselhos Municipais de Segurança Alimentar e características socioeconômicas dos municípios, podem influenciar essa decisão?

Para responder a essas questões, realizamos uma análise estatística detalhada utilizando três métodos principais:

1. **Correlação de Pearson**, para medir o grau de associação entre diferentes variáveis e identificar relações diretas.
2. **Regressão Logística Múltipla**, para estimar a influência de diferentes fatores na probabilidade de um município adotar um Plano Municipal de Segurança Alimentar.
3. **Interpretação dos Resultados**, para traduzir os achados estatísticos em informações úteis para gestores públicos e formuladores de políticas.

O objetivo deste estudo é fornecer uma análise clara e baseada em evidências sobre os fatores que influenciam a implementação de políticas de segurança alimentar nos municípios brasileiros. Isso permitirá que gestores públicos e pesquisadores desenvolvam estratégias mais eficazes para ampliar o alcance dessas políticas.

---

## 2. Escolha dos Testes Estatísticos

A escolha dos métodos estatísticos foi baseada na natureza das variáveis e no objetivo do estudo. Como estamos analisando variáveis categóricas (presença ou ausência de um Plano Municipal de Segurança Alimentar e presença ou ausência de um Comitê Intersetorial de Assistência Social), utilizamos abordagens estatísticas que permitem medir relações entre essas variáveis e quantificar seus impactos.

### 2.1. Correlação de Pearson

O **Coeficiente de Correlação de Pearson** é uma medida estatística que indica o grau de associação entre duas variáveis numéricas. Os valores variam entre **-1 e 1**:

- **Correlação positiva (+1):** Quando uma variável aumenta, a outra também tende a aumentar.
- **Correlação negativa (-1):** Quando uma variável aumenta, a outra tende a diminuir.
- **Correlação próxima de 0:** Indica que não há uma relação linear forte entre as variáveis.

No nosso caso, a Correlação de Pearson foi utilizada para medir **o grau de associação entre a presença de um Plano Municipal de Segurança Alimentar e outros fatores, como a existência de um Comitê Intersetorial de Assistência Social, um Conselho Municipal de Segurança Alimentar e características socioeconômicas do município**.

### 2.2. Regressão Logística Múltipla

A **Regressão Logística Múltipla** foi utilizada para entender **quais fatores aumentam ou reduzem a probabilidade de um município adotar um Plano Municipal de Segurança Alimentar**. Diferente da Correlação de Pearson, que apenas mede a relação entre duas variáveis, a Regressão Logística permite **controlar múltiplos fatores simultaneamente**, garantindo que a análise seja mais precisa.

Esse modelo estatístico retorna coeficientes que indicam **o efeito de cada variável na probabilidade de um município adotar um Plano de Segurança Alimentar**. Esses coeficientes podem ser interpretados em termos de **Razões de Chances (Odds Ratios)**, que indicam o quanto a presença de uma variável influencia a probabilidade do evento ocorrer.

---

## 3. Apresentação e Interpretação dos Resultados

### 3.1. Correlação de Pearson

Os resultados da análise de correlação indicam que:

- **Plano Municipal de Segurança Alimentar e Lei Municipal de Segurança Alimentar:** **Correlação de 0,305**  
  - Existe uma **correlação moderada**, indicando que municípios que criam leis municipais nessa área também estruturam planos formais.

- **Plano Municipal de Segurança Alimentar e Comitê Intersetorial de Assistência Social:** **Correlação de 0,044**  
  - **Correlação muito fraca**, sugerindo que a presença do Comitê Intersetorial de Assistência Social **não está fortemente associada à implementação de um Plano de Segurança Alimentar**.

- **Lei Municipal de Segurança Alimentar e Comitê Intersetorial de Assistência Social:** **Correlação de 0,094**  
  - **Correlação fraca**, indicando que municípios com Comitês Intersetoriais de Assistência Social **têm uma leve tendência a adotar Leis Municipais de Segurança Alimentar**.

### 3.2. Resultados da Regressão Logística

A regressão logística permitiu identificar **quais fatores têm um impacto significativo** na adoção de Planos Municipais de Segurança Alimentar.

| **Variável**                           | **Razão de Chances** | **Significância Estatística (p-valor)** | **Interpretação** |
|-----------------------------------------|----------------|-------------------------------|-------------------|
| **Conselho Municipal de Segurança Alimentar** | **4,14** | **<0,0001** | Municípios com um conselho **têm 4,14 vezes mais chance** de adotar um Plano de Segurança Alimentar. |
| **População do município** | **1,000001** | **0,010** | Municípios mais populosos **têm uma leve tendência maior** de adotar um Plano de Segurança Alimentar. |
| **Auxílio a famílias com crianças na educação infantil** | **1,78** | **<0,0001** | Municípios que oferecem esse auxílio **têm 78% mais chance** de ter um Plano de Segurança Alimentar. |
| **Comitê Intersetorial de Assistência Social** | **1,11** | **0,191** | **Não significativo**. A presença do comitê **não influencia diretamente** a adoção do plano. |

---

## 4. Conclusões e Implicações para Políticas Públicas

### Principais Conclusões

- **A presença de um Conselho Municipal de Segurança Alimentar é o fator mais relevante para a adoção de um Plano Municipal de Segurança Alimentar.**
- **A existência de um Comitê Intersetorial de Assistência Social não tem impacto estatisticamente significativo na adoção do plano.**
- **Municípios que oferecem auxílio a famílias com crianças em idade escolar têm maior probabilidade de implementar um Plano de Segurança Alimentar.**
- **A população do município tem um leve impacto na adoção do plano, mas não é o fator principal.**

### Implicações para Políticas Públicas

1. **Fortalecer a criação de Conselhos Municipais de Segurança Alimentar**, pois sua existência está fortemente associada à adoção de Planos Municipais de Segurança Alimentar.
2. **Ampliar programas de assistência social voltados para famílias com crianças em idade escolar**, pois esses programas também estão relacionados à segurança alimentar.
3. **Reavaliar o papel dos Comitês Intersetoriais de Assistência Social**, pois sua existência, isoladamente, não parece impactar a adoção de planos formais de segurança alimentar.
