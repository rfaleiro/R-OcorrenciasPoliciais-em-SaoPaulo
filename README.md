Análise de Criminalidade no Estado de São Paulo (2016-2025)
================
github.com/RFaleiro
2026-03-13

## 1. Proposta

Este relatório fornece uma análise extensa dos dados de segurança
pública do Estado de São Paulo de 2016 até o início de 2025. Ao agregar
mais de 80 métricas distintas de criminalidade, buscamos descobrir
tendências macro, identificar as anomalias de crescimento mais rápido
pós-pandemia e destacar atividades criminosas correlacionadas.

### 1.1 Base de dados

A extração dos dados é realizada de forma automatizada (via *web
scraping*) diretamente do portal da Secretaria de Segurança Pública do
Estado de São Paulo (SSP-SP).

Para coletar o histórico completo ano a ano, o nosso script constrói
dinamicamente a URL de origem das tabelas estatísticas. O endereço base
segue um padrão estruturado onde o **ano** e o **trimestre** são
alterados programaticamente na URL:

`https://www.ssp.sp.gov.br/assets/estatistica/trimestral/arquivos/{ano}-{trimestre}.htm`

**Como funciona a montagem dinâmica da URL:**

- **`{ano}`**: Varia em um loop de 2016 até o ano atual (2025).
- **`{trimestre}`**: Varia de `01` a `04` (sempre com dois dígitos),
  representando cada trimestre do respectivo ano.

Desta forma, o *crawler* substitui essas variáveis iterativamente (por
exemplo, acessando a página de dados de `.../2023-01.htm`, seguida por
`.../2023-02.htm`, etc.) e faz o download de todos os relatórios,
consolidando todo o histórico em um único grande arquivo para a nossa
análise.

Os relatórios em formato PDF gerados durante a coleta dos dados brutos
podem ser acessados diretamente através [deste link para a pasta
`data/raw/pdf_ssp_reports/`](data/raw/pdf_ssp_reports/).

## 2. Tendências Gerais

![](README_files/figure-gfm/tendencias_gerais-1.png)<!-- -->![](README_files/figure-gfm/tendencias_gerais-2.png)<!-- -->

A análise exploratória das **Tendências Gerais** da segurança pública em
São Paulo nos revela dois panoramas bastante claros na série histórica:

1.  **A Escalada Alarmante dos Boletins Totais de Ocorrência:** Ao
    observar a linha geral do Estado, o período pré-pandemia (2016
    a 2019) mantinha um registro firme na ordem de **705.162 ocorrências
    por trimestre**. Após um natural e trágico engessamento do número em
    2020 e 2021 pela falta de mobilidade no isolamento dos lockdowns (o
    grande *vale* no gráfico), houve um rebote dramático: no período
    pós-2022 o número de boletins trimestrais bateu sucessivos recordes,
    se perpetuando numa média absurda de **990.152 registros por
    trimestre**. O cume desse volume denota um incremento estrondoso de
    **+40,4%** a mais de ocorrências despachadas rotineiramente perante
    a média histórica pré-crise.

2.  **O Crescimento Brando e Descorrelacionado dos Furtos:** Por vias
    analíticas opostas, ao insulormos os chamados casos de **Furto -
    Outros** (aqueles de baixa resolução e não enquadrados puramente em
    perfis como veículos pesados), percebemos que o seu padrão sofreu um
    deslocamento bem inferior. A base de dados revela que, antes de 2020
    a média era de *128.597* casos reportados nestas infrações e, mesmo
    após todo o boom de 2023 pra frente, ele subiu de forma contida para
    a base de *140.173 casos*. É uma alta de apenas **+9,0%**.

Isso nos leva a uma conclusão importantíssima do ponto de vista
investigativo: **como os furtos simples não cresceram na mesma proporção
desvairada do todo, conclui-se que o avanço crítico de mais de 40%
empurrado no volume macro da Secretaria da Segurança Pública de SP foi
insuflado pesadamente por crimes mais diversificados, ou até ocorrências
atípicas e violentas que fugiram ao controle ao longo dessa mesma linha
de tempo.**

### 2.1 Crimes que mais cresceram

![](README_files/figure-gfm/crimes_cresceram-1.png)<!-- -->

| Métrica | Média de ocorrências/Ano (Pré-2020) | Média de ocorrências/Ano (Pós-2022) | Crescimento |
|:---|:---|:---|:---|
| Contra a Dignidade Sexual | 14,970 | 27,570 | 84.2% |
| Contra o patrimônio | 1,152,063 | 1,803,896 | 56.6% |
| Contra a pessoa | 474,304 | 713,229 | 50.4% |
| Total de delitos | 1,850,511 | 2,766,427 | 49.5% |
| Não Criminais | 1,495,679 | 2,010,436 | 34.4% |
| Outros criminais (não inclui contravenções) | 109,970 | 129,669 | 17.9% |
| Contravencionais | 41,768 | 48,962 | 17.2% |
| Entorpecentes | 57,436 | 43,101 | -25.0% |

A Explosão da Violência Contra a Dignidade Sexual e Patrimônio

O primeiro gráfico de halteres revelando os perfis agregados **por
natureza criminal** explica visceralmente para onde a carga violenta
escorreu após todo o desmembramento promovido pelo fechamento social. O
grande propulsor que mais alavancou os números macabros contra a
sociedade civil paulista foi aterradoramente associado aos **Crimes
Contra a Dignidade Sexual** (que inflaram impressionantes **+84,2%** em
volume absoluto de ocorrências em todo fluxo pós-pandêmico comparado ao
histórico até 2019).

Na sequência do horror, os gigantes demográficos do relatório, como
**Crimes Contra o Patrimônio** (aumentando **+56,6%** e puxando uma
brutal volumetria real para casa dos milhões) e os **Crimes Contra a
Pessoa** (pesando **+50,4%** no Estado) atestam uma perda agressiva de
freios em todos os campos da convivência urbana e física, inflando
desproporcionalmente o Total de Delitos que comentamos alhures.

Nota-se também que **Entorpecentes** foi literalmente a única frente
criminal documentada que cedeu drasticamente (uma queda linear de
**-25%**). Isso sugere possivelmente um gargalo operacional,
subnotificação investigativa, mudança pesada de comando ou uma forte
alteração das estratégias e focos de operação na atuação flagrante nas
pontas nos últimos anos.

![](README_files/figure-gfm/crimes_cresceram-2.png)<!-- -->

| Métrica | Média de boletins de ocorrência/Ano (Pré-2020) | Média de boletins de ocorrência/Ano (Pós-2022) | Crescimento |
|:---|:---|:---|:---|
| Extorsão mediante seqüestro (5) | 19 | 177 | 817.7% |
| Homicídio culposo por Acidente de Trânsito | 3,356 | 3,951 | 17.7% |
| Lesão corporal dolosa | 133,105 | 155,160 | 16.6% |
| Homicídio Culposo (7) | 3,526 | 4,099 | 16.3% |
| Furto - outros | 514,388 | 560,691 | 9.0% |
| Tentativa de homicídio | 3,694 | 3,657 | -1.0% |
| Lesão corporal culposa outras | 3,236 | 3,022 | -6.6% |
| Furto de veículos | 101,440 | 91,863 | -9.4% |
| Lesão corporal culposa por Acidente de Trânsito | 84,933 | 71,603 | -15.7% |
| Tráfico de entorpecentes | 47,675 | 39,681 | -16.8% |
| Homicídio doloso | 3,136 | 2,520 | -19.6% |
| Nº de Vítimas em Homicídio Doloso | 3,298 | 2,628 | -20.3% |
| Homicídio Doloso por acidente de trânsito (10) | 39 | 21 | -46.5% |
| Latrocínio | 287 | 153 | -46.8% |
| Nº de Vítimas de Latrocínio | 294 | 156 | -47.1% |
| Roubo de Carga | 9,148 | 4,748 | -48.1% |
| Roubo de veículos | 62,850 | 31,397 | -50.0% |
| Roubo a Banco | 77 | 5 | -94.0% |

**A Migração do Crime: Extorsões Explodem, Roubos de Alto Padrão
Desabam:** Ao destrincharmos rigorosamente os dados dentro das
tipificações criminais do segundo gráfico, uma radiografia espantosa e
muito singular da sociedade paulista se desenha. O crime organizado
comum operou uma pivotagem brutal no Estado de São Paulo abandonando os
crimes tradicionalmente caracterizados como *‘defesa do patrimônio das
elites e corporações’* e escorrendo para a impunidade do ambiente
digital e da extorsão direta na rua.

**O Que Mais Desabou:** Houve um colapso gigantesco e estatisticamente
perfeito nas ocorrências que demandam confronto direto contra capital
fortificado e corporativo. A base revela que **Roubo a Banco
(derretimento de -94%)**, **Roubo de Veículos (-50%)**, **Roubo de Carga
(-48,1%)** e até o trágico **Latrocínio (-46,8%)** caíram praticamente
pela metade em comparação com a rotina paulista antes de 2020. O governo
obteve aparente controle pleno nas vitrines ostensivas de segurança
privada/pública nos redutos de grande patrimônio.

**O Que Mais Explodiu (O Novo Custo Brasil):** Toda a criminalidade
contida nos muros corporativos buscou uma assustadora compensação no
cidadão civil comum. A tipificação que sofreu o aumento mais alucinante
e bizarro de toda a história da SSP-SP foi a **Extorsão Mediante
Seqüestro (o famigerado ‘Golpe do PIX’ / Sequestro Relâmpago)** que
subiu absurdos **+817,7%** (saltando de 19 casos/ano para
estratosféricos 177 casos anuais mapeados em média). Essa transição do
criminoso saindo da porta do banco para invadir a transação bancária no
celular do refém na rua se provou um pesadelo incontornável.

Paralelamente, o convívio social urbano demonstrou esgarçamento fatal.
Os **Homicídios por Acidente de Trânsito** cresceram significativamente
(**+17,7%**, perfazendo em média quase 4.000 mortos registrados sob esse
flagelo anualmente), e a pura **Lesão Corporal Dolosa** (agressão com
intenção de ferir e brigas generalizadas da rua a lares civis) marcou
uma alta de **+16,6%**, superando um patamar horripilante de mais de
155.000 vítimas catalogadas por ano frente ao período antes do
isolamento.

### 2.2 Tendência para crimes contra a Pessoa

![](README_files/figure-gfm/tendencias_pessoa-1.png)<!-- -->![](README_files/figure-gfm/tendencias_pessoa-2.png)<!-- -->

A análise específica dos **Crimes contra a Pessoa**, abordando mortes
culposas e atentas à vida que não se consumaram, traz um contraponto
importante sobre qual perfil de violência está crescendo verdadeiramente
no Estado de São Paulo:

1.  **Aumento Consistente dos Homicídios Culposos:** Observamos uma
    tendência consolidada de alta nos homicídios culposos (onde não há
    intenção primária de matar, estando frequentemente associados a
    fatalidades sistêmicas, violência no trânsito ou negligência
    imprudente). A série apresentava uma média contida em cerca de **882
    casos** por trimestre antes da pandemia; porém, a curva cresceu de
    forma contínua a ponto de cruzar, repetidas vezes, a barreira de
    mais de **1.000 mortes/trimestre** a partir de 2023. Isso compõe um
    aumento sistemático e não-ignível de **+16,3%**.

2.  **Estabilidade Absoluta nas Tentativas de Homicídio:** Em
    contrapartida nítida, as *Tentativas de Homicídio* (crimes
    violentos, agressões diretas com dolo de matar, mas interceptadas)
    não pioraram estruturalmente. A sua média pré-crise orbitava na casa
    de 924 registros trimestrais, oscilando para exatos **914
    casos/trimestre** no período recente pós-2022. Essa é uma variação
    achatada de essencialmente **-1,0%** (estabilidade perfeita).

A união destes dois cenários endossa a lógica discutida na tendência
geral: ao cruzar a não-piora da intenção ativa de matar de um lado e o
salto formidável em vítimas letais de homicídios culposos do outro,
concluímos que a violência clássica e premeditada das ruas paulistas não
avançou massivamente — o perigo e as fatalidades estruturais cresceram
através de vias mais imprudentes/acidentais dentro da sociedade ou
tráfego civil.

### 2.3 Tendência para crimes contra o patrimônio

![](README_files/figure-gfm/tendencias_patrimonio-1.png)<!-- -->![](README_files/figure-gfm/tendencias_patrimonio-2.png)<!-- -->![](README_files/figure-gfm/tendencias_patrimonio-3.png)<!-- -->

Quando passamos a lupa nas estatísticas sobre aquilo que classicamente
se estrutura como a **“Defesa do Patrimônio”**, cruzamos com a única
frente de segurança que apresentou um sucesso operacional na última
década no Estado de São Paulo. Se as ocorrências totais estaduais
escalaram mais de +40%, os crimes vitrine não seguiram a mesma sorte:

1.  **A Erradicação do Roubo a Banco:** O roubo a instituições
    financeiras, que exigia quadrilhas pesadas, logística
    cinematográfica e armas de guerra — além de ferir de morte o capital
    blindado do Estado — desmoronou do mapa de ocorrências de forma
    fulminante. A média pré-pandemia de quase 80 casos por ano desabou
    brutalmente e agora beira a extinção (oscilando em torno de módicos
    5 casos por ano), desenhando um colapso avassalador de **-94%**
    sobre a modalidade.

2.  **A Sangria Estancada no Roubo de Carga e Veículos:** As modalidades
    de roubo de carga e de veículos apresentaram **quedas acentuadas de
    48% e 50%**, respectivamente, em suas volumetrias médias. A série
    histórica indica um declínio contínuo e simétrico nessas categorias,
    que dependem diretamente de fatores como fiscalização rodoviária,
    policiamento ostensivo e regulação de seguradoras. Os dados sugerem
    maior controle estatal sobre crimes patrimoniais tradicionalmente
    associados à infraestrutura logística e urbana no estado.

## 3. Crimes Graves - Estupro

![](README_files/figure-gfm/estupro_total-1.png)<!-- -->

O gráfico de série histórica revela uma pronunciada quebra de padrão
trazida pela pandemia. No segundo trimestre de 2020 ocorreu a maior
queda da série (atingindo apenas cerca de 2.167 casos num único
trimestre), o que reflete a trágica subnotificação gerada pelo
confinamento do isolamento social. Porém, imediatamente após a volta à
normalidade, a curva não apenas retornou à sua média, mas assumiu uma
vertiginosa tendência de aceleração, escalando e quebrando seguidos
recordes históricos até atingir níveis críticos acima de 3.800
ocorrências trimestrais em 2024 e no início de 2025.

### 3.1 Taxa de crescimento de estupros

![](README_files/figure-gfm/unnamed-chunk-1-1.png)<!-- -->

O gráfico acima revela que a categoria **Estupro de Vulnerável** foi o
verdadeiro motor do crescimento criminoso pós-pandemia, saltando
vertiginosamente +31% em relação a 2019 (de 8.487 para 11.118
vítimas/ano). Em contrapartida, as ocorrências comuns de “Estupro”
permaneceram quantitativamente estáveis (apenas +2,3% de aumento),
indicando que o alarmante agravamento estadual decorre primariamente de
violações contra vulneráveis e menores.

## 4. O Custo Humano do Confronto: Letalidade e Atuação Policial

![](README_files/figure-gfm/vitimas_e_autores-1.png)<!-- -->![](README_files/figure-gfm/vitimas_e_autores-2.png)<!-- -->

Este tópico analisa o cenário de letalidade decorrente da intervenção
estatal, onde o confronto direto entre forças de segurança e civis
revela o lado mais trágico da insegurança pública. Longe de serem apenas
números, esses dados representam uma guerra urbana que exige esforços
contínuos de controle e redução, uma vez que o desfecho letal sinaliza
uma falha no processo de pacificação onde todos os lados sofrem perdas
irreparáveis.

A análise dos indicadores aponta para uma dinâmica de resistência e
vitimização que, embora em patamares menores que no passado, ainda
demanda atenção crítica:

### 4.1 Vidas Perdidas em Intervenções Policiais

Os dados consolidados das polícias Civil e Militar indicam que o número
de civis mortos em confrontos durante o serviço apresentou uma redução.

- **Média Pré-2020:** ~660 mortes anuais.
- **Média Pós-2022:** ~590 mortes anuais.
- **Variação:** `-11%`

> **Nota Crítica:** Embora o recuo estatístico seja um passo em direção
> ao controle da força, o volume de óbitos ainda evidencia a alta
> voltagem dos conflitos nas periferias e centros urbanos.

### 4.2 A Vitimização dos Agentes de Segurança

A letalidade também atinge aqueles que operam o braço armado do Estado.
A perda de vidas de oficiais no cumprimento do dever registrou o
seguinte comportamento:

- **Média Pré-2020:** 18 agentes por ano.
- **Média Pós-2022:** 14 agentes por ano.
- **Variação:** `-20%`

A queda na perda de vidas de policiais é um indicador positivo de
preservação da integridade dos agentes, mas cada óbito representa uma
ruptura no sistema de segurança e um custo humano inaceitável para as
famílias e para a instituição.

------------------------------------------------------------------------

### Conclusão do Cenário

Os dados sugerem que o agravamento da insegurança percebido pelo cidadão
no dia a dia (como nos crimes digitais e patrimoniais) não tem sido
acompanhado, proporcionalmente, por uma escalada na guerra letal entre
Estado e crime organizado.

No entanto, a manutenção de centenas de mortes anuais reforça a urgência
de políticas de segurança baseadas em **inteligência e desescalada**,
visando reduzir ao máximo o confronto armado e preservar a vida de todos
os envolvidos.
