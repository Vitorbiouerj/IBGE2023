# Análise da Relação entre o Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil e o Plano de Segurança Alimentar

## 1. Introdução

A implementação de políticas públicas voltadas para o bem-estar social e o desenvolvimento infantil tem sido uma prioridade em muitos municípios brasileiros. Entre essas políticas, destacam-se o **Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil** e o **Plano de Segurança Alimentar**. O primeiro busca garantir que crianças em idade escolar tenham apoio financeiro ou estrutural para frequentar a educação infantil, enquanto o segundo visa assegurar a segurança alimentar das populações vulneráveis.

Diante disso, surge uma questão central: **os municípios que implementam o Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil também tendem a adotar políticas de segurança alimentar?** Existe uma relação entre essas duas políticas, indicando que um plano pode incentivar ou facilitar a adoção do outro? Ou a implementação desses planos ocorre de maneira independente, sem relação significativa entre eles?

Para responder a essas perguntas, realizamos uma **análise estatística abrangente**, utilizando **Testes Qui-Quadrado e V de Cramér**, que verificam se há associação entre essas variáveis, e um **modelo de Regressão Logística**, que mede o impacto do Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil na existência do Plano de Segurança Alimentar, controlando para outros fatores como a presença de um Comitê Intersetorial.

O objetivo deste estudo é fornecer **informações concretas para gestores públicos, pesquisadores e profissionais da área de assistência social**, permitindo um melhor entendimento sobre os fatores que influenciam a adoção de políticas de segurança alimentar e educação infantil. Os resultados podem contribuir para a **formulação de estratégias mais eficazes**, garantindo que essas políticas sejam implementadas de forma integrada e atendam melhor às necessidades da população.

---

## 2. Escolha dos Testes Estatísticos

A escolha das ferramentas estatísticas utilizadas na análise foi baseada na natureza das variáveis e nos objetivos do estudo. Como estamos lidando com variáveis **categóricas binárias** (presença ou ausência dos planos nos municípios), foram escolhidos dois tipos de análises:

### 2.1. Teste Qui-Quadrado e V de Cramér

- O **Teste Qui-Quadrado** foi utilizado para verificar se há **uma associação estatisticamente significativa** entre a existência do **Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil** e a presença do **Plano de Segurança Alimentar**.
- O **V de Cramér** foi calculado para medir a **força** dessa associação.

### 2.2. Regressão Logística

- Esse modelo estatístico foi utilizado para avaliar se a **presença do Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil aumenta a probabilidade de um município ter um Plano de Segurança Alimentar**, ajustando também para a presença de um Comitê Intersetorial.
- Diferente do Qui-Quadrado, que apenas testa a associação entre duas variáveis, a regressão logística **quantifica o impacto** do plano municipal na segurança alimentar e permite avaliar se outros fatores podem influenciar essa relação.

---

## 3. Explicação dos Testes

### 3.1. Teste Qui-Quadrado

O **Teste Qui-Quadrado** foi aplicado para verificar se a proporção de municípios que possuem um Plano de Segurança Alimentar é maior entre aqueles que já implementaram o **Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil**.

**Resultados:**

- **Qui-Quadrado = 16,917**
- **p-valor = 0,00021**

O **p-valor muito baixo** indica que **existe uma associação estatisticamente significativa** entre os dois planos. Isso significa que os municípios que possuem um Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil **têm uma maior tendência** de possuir também um Plano de Segurança Alimentar.

### 3.2. V de Cramér

O **V de Cramér** foi calculado para indicar a **força** dessa associação. O valor encontrado foi **0,055**, o que significa que a associação é **muito fraca**. Para entender melhor essa métrica:

- **0 a 0,10** → Associação muito fraca  
- **0,10 a 0,20** → Associação fraca  
- **0,20 a 0,30** → Associação moderada  
- **Acima de 0,30** → Associação forte  

Embora os municípios com o Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil **sejam mais propensos a ter um Plano de Segurança Alimentar**, essa relação é **fraca**. Isso indica que **existem outros fatores mais importantes** que influenciam a adoção de políticas de segurança alimentar.

### 3.3. Regressão Logística

A **Regressão Logística** foi utilizada para medir **o impacto exato do Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil na existência de um Plano de Segurança Alimentar**.

**Resultados:**

- **Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil**  
  - **Coeficiente = 0,2123** (**p = 0,012**) → Estatisticamente significativo  
  - **Razão de Chances (OR) = 1,236** → Municípios com esse plano têm **23,6% mais chance** de ter um Plano de Segurança Alimentar.

- **Comitê Intersetorial**  
  - **Coeficiente = 0,1424** (**p = 0,075**) → **Não significativo**  
  - **Razão de Chances (OR) = 1,153** → Municípios com Comitê Intersetorial têm **15,3% mais chance**, mas o efeito **não é estatisticamente significativo**.

O **Pseudo R²** do modelo foi **0,0032**, indicando que o modelo explica **muito pouca variação nos dados**.

---

## 4. Conclusão

Os resultados da análise indicam que **existe uma relação estatisticamente significativa entre a presença do Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil e a adoção do Plano de Segurança Alimentar**, mas essa relação **não é forte**. O impacto da existência do plano municipal na implementação de políticas de segurança alimentar **é real, mas pequeno**.

Os principais achados são:

1. **Os municípios que implementaram o Plano Municipal de Auxílio a Famílias com Crianças em Idade Escolar na Educação Infantil têm maior probabilidade de possuir um Plano de Segurança Alimentar.**
2. **A força dessa associação é fraca**, indicando que a adoção de planos de segurança alimentar pode depender mais de outros fatores, como financiamento público, políticas estaduais e nível de envolvimento da sociedade civil.
3. **A presença de um Comitê Intersetorial não demonstrou impacto estatisticamente significativo**, sugerindo que esse comitê pode não ser determinante na adoção de um Plano de Segurança Alimentar.

Diante desses resultados, recomenda-se que futuras pesquisas incluam outras variáveis, como **níveis de investimento público, fatores socioeconômicos do município e incentivos estaduais**, para compreender melhor os fatores determinantes para a adoção de políticas de segurança alimentar.

---

## 5. Dados Brutos
```
Tabela de contingência - Plano Municipal vs. Segurança Alimentar:
Plano_de_seguranca_alimentar__existencia   Não  Não Disponível  Sim
PlanoMun_existe                                                    
False                                     3361               1  719
True                                      1154               2  328

Resultado do Teste Qui-Quadrado:
Qui-quadrado: 16.917, p-valor: 0.00021

V de Cramér: 0.055 (Força da Associação)

Optimization terminated successfully.
         Current function value: 0.482286
         Iterations 5
                                      Logit Regression Results                                      
====================================================================================================
Dep. Variable:     Plano_de_seguranca_alimentar__existencia   No. Observations:                 5564
Model:                                                Logit   Df Residuals:                     5561
Method:                                                 MLE   Df Model:                            2
Date:                                      Fri, 07 Mar 2025   Pseudo R-squ.:                0.003185
Time:                                              11:39:31   Log-Likelihood:                -2683.4
converged:                                             True   LL-Null:                       -2692.0
Covariance Type:                                  nonrobust   LLR p-value:                 0.0001890
=============================================================================================
                                coef    std err          z      P>|z|      [0.025      0.975]
---------------------------------------------------------------------------------------------
const                        -1.5733      0.045    -34.848      0.000      -1.662      -1.485
PlanoMun_existe               0.2123      0.085      2.505      0.012       0.046       0.378
ComiteIntersec_existência     0.1424      0.080      1.781      0.075      -0.014       0.299
=============================================================================================

Razões de Chances (Odds Ratios):
const                        0.207363
PlanoMun_existe              1.236520
ComiteIntersec_existência    1.153045
dtype: float64
```