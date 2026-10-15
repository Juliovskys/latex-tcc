# Avaliação Contextual de Serviços Públicos Digitais

## concepção e desenvolvimento de um sistema baseado em indicadores de navegação e qualidade percebida

**Autores:** Julio Cesar Gomes de Souza Crispim e Fernando Gabriel dos Santos Carrijo.

**Instituição:** Universidade de Brasília — Faculdade de Ciências e Tecnologias em Engenharia — Engenharia de Software.

**Orientador:** Wander Cleber Maria Pereira da Silva.

**Local e ano:** Brasília, DF, 2026.

Monografia submetida ao curso de graduação em Engenharia de Software da Universidade de Brasília como requisito parcial para obtenção do título de Bacharel em Engenharia de Software.

# Resumo

Este trabalho apresenta a concepção e o desenvolvimento inicial de um sistema de avaliação contextual de serviços públicos digitais. O problema investigado é a dificuldade de relacionar avaliações declaradas pelo cidadão ao contexto de navegação em que são solicitadas. O percurso combinou revisão bibliográfica e normativa, Lean Inception e prototipação incremental, com referência à Design Science Research. Foi implementado um protótipo local em Python, com API, páginas simuladas, regras operacionais sobre cliques e duração informada, formulário de feedback e painel administrativo. A telemetria fornece indícios comportamentais, sem medir qualidade percebida. Estrelas e atributos registram julgamentos declarados; o NPS foi mantido nesta versão como pergunta auxiliar de recomendação, sem validação de sua interpretação no setor público. Separadamente da implementação funcional, oito participantes avaliaram fluxos de interface no Figma, com registro automático de cliques e tempos pelo Useberry e questionário pós-sessão. Quatro participantes realizaram cada fluxo, com alocação auxiliada por inteligência artificial (IA), descrita como sorteio sem registro auditável, e com popup de redirecionamento presente em ambos. Os resultados descrevem conclusão de tarefa, facilidade percebida e relatos pós-sessão. Não comprovam maior participação, maior especificidade dos comentários do formulário, funcionamento dos gatilhos da API ou superioridade do fluxo contextual. A contribuição investigativa está na formulação de uma hipótese comparativa e na distinção entre evidências comportamentais e declaradas; a contribuição tecnológica está na implementação que permite relacioná-las. A continuidade exige operacionalizar as medidas, documentar o protocolo e calibrar as regras antes de uso real.

**Palavras-chave**: serviços públicos digitais. feedback contextual. avaliação de serviços. experiência do usuário. Design Science Research.

# Abstract

This work presents the design and initial development of a contextual evaluation system for digital public services. The research problem concerns linking citizens' declared evaluations to the navigation context in which feedback is requested. The work combined bibliographic and regulatory review, Lean Inception, and incremental prototyping, drawing on Design Science Research. A local Python prototype was implemented with an API, simulated pages, operational rules based on clicks and reported duration, a feedback form, and an administrative dashboard. Telemetry provides behavioral indications and does not measure perceived quality. Stars and attributes capture declared judgments; this version retains NPS as an auxiliary recommendation question whose interpretation in public services has not been validated. Separately from the functional implementation, eight participants evaluated interface flows in Figma, with automatic click and time records collected through Useberry and a post-session questionnaire. Four participants performed each flow, with artificial-intelligence-assisted allocation described as a draw without an auditable record, and with a redirect popup present in both flows. The results describe task completion, perceived ease, and post-session reports. They do not establish greater participation, more specific feedback-form comments, correct API-trigger behavior, or superiority of contextual feedback. The investigative contribution is the comparative hypothesis and the distinction between behavioral and declared evidence; the technological contribution is the implementation that can connect them. Further work requires operational measures, a documented protocol, and rule calibration before deployment.

**Key-words**: digital public services. contextual feedback. service evaluation. user experience. Design Science Research.

# Abreviaturas e siglas

| Sigla | Significado |
| --- | --- |
| API | Application Programming Interface |
| BRASP | Modelo Brasileiro de Avaliação de Serviços Públicos |
| CES | Customer Effort Score |
| CSAT | Customer Satisfaction Score |
| DSR | Design Science Research |
| ESM | Experience Sampling Method |
| FCTE | Faculdade de Ciências e Tecnologias em Engenharia |
| HTML | HyperText Markup Language |
| HTTP | Hypertext Transfer Protocol |
| IA | Inteligência artificial |
| IRPF | Imposto sobre a Renda da Pessoa Física |
| ISO | International Organization for Standardization |
| LGPD | Lei Geral de Proteção de Dados Pessoais |
| MVP | Minimum Viable Product |
| NPS | Net Promoter Score |
| PPA | Plano Plurianual |
| SQLite | Sistema de gerenciamento de banco de dados relacional embarcado |
| TCC | Trabalho de Conclusão de Curso |
| TCLE | Termo de Consentimento Livre e Esclarecido |
| TIC | Tecnologias de Informação e Comunicação |
| UnB | Universidade de Brasília |
| UX | User Experience |

# 1 Introdução

## 1.1 Contextualização

Nas últimas décadas, a relação entre Estado e cidadão passou por uma mudança estrutural: atividades que antes dependiam de balcões presenciais, deslocamentos e atendimento físico foram progressivamente incorporadas a portais, aplicações e fluxos digitais. A plataforma GOV.BR simboliza esse movimento ao concentrar a oferta digital de serviços federais e ao reforçar a ideia de que governo digital não é apenas troca de canal, mas reorganização da forma como o cidadão encontra, solicita, acompanha e avalia serviços públicos.

Os serviços públicos compõem uma das formas mais diretas dessa relação. Solicitar um documento, consultar uma situação cadastral, acompanhar um benefício, registrar uma demanda ou acessar uma política pública são situações em que a experiência do usuário influencia a qualidade percebida da administração pública. A digitalização ampliou o alcance e a velocidade desses atendimentos, mas também deslocou parte das dificuldades para a própria navegação: localizar o serviço correto, entender a linguagem institucional, preencher etapas intermediárias e perceber se a solicitação realmente avançou.

A escala dessa transição aparece de forma clara em experiências recentes de participação digital. O Plano Plurianual (PPA) Participativo 2024-2027, por exemplo, mobilizou mais de 1,5 milhão de participantes e superou 4 milhões de acessos na plataforma Brasil Participativo, demonstrando a capacidade de mobilização do ambiente digital. Ao mesmo tempo, a experiência registrou barreiras como problemas de conectividade, dificuldade de uso, fluxos de cadastro complexos e necessidade de melhor retorno ao cidadão sobre sua contribuição ([Brasil. Ministério da Gestão e da Inovação em Serviços Públicos, 2024](#ref-brasilMgi2024ppaParticipativo)). Esse contraste reforça a importância de avaliar não apenas se o serviço existe em formato digital, mas como ele é percebido e utilizado durante a jornada.

No Brasil, a avaliação dos serviços públicos possui base legal e gerencial. A Lei n<sup>o</sup> 13.460/2017 trata da participação, proteção e defesa dos usuários de serviços públicos e prevê que os resultados de avaliação subsidiem a reorientação e o ajuste da prestação estatal ([Brasil, 2017b](#ref-brasil2017lei13460)). O Decreto n<sup>o</sup> 9.094/2017 institui a Carta de Serviços ao Usuário e reforça a simplificação do atendimento ([Brasil, 2017a](#ref-brasil2017decreto9094)). A Lei n<sup>o</sup> 14.129/2021 associa governo digital, eficiência pública, desburocratização e participação do cidadão ([Brasil, 2021](#ref-brasil2021lei14129)). O Decreto n<sup>o</sup> 11.260/2022, ao tratar da Estratégia Nacional de Governo Digital, reforça esse movimento de organização e monitoramento da transformação digital na administração pública federal ([Brasil, 2022](#ref-brasil2022decreto11260)).

A avaliação da experiência digital, porém, não depende apenas de perguntar ao usuário se ele ficou satisfeito ao final do atendimento. Em serviços digitais, excesso de cliques, permanência por tempo acima do esperado, retorno repetido a páginas anteriores e abandono antes da conclusão constituem evidências comportamentais de possível dificuldade. Esses sinais não medem qualidade percebida e não autorizam, isoladamente, concluir que a experiência foi ruim. Quando coletados com finalidade clara e com cuidado em relação à privacidade, eles ajudam a localizar pontos da jornada que devem ser investigados e confrontados com a percepção declarada pelo usuário ([DeLone; McLean, 2003](#ref-deloneMclean2003); [Government Digital Service, 2021a](#ref-govuk2021completionRate); [Brasil, 2018](#ref-brasil2018lgpd)).

A proposta é relacionar evidências comportamentais e declaradas sem tratá-las como equivalentes. A implementação Python registra cliques em elementos instrumentados, página, serviço e informações do evento; recebe também uma duração informada à API, demonstrada por envio simulado de 120 segundos, sem cronômetro automático no cliente. Regras operacionais podem gerar uma sugestão de redirecionamento ou disponibilizar um convite. Estrelas, atributos e comentários permitem examinar julgamentos declarados; a pergunta auxiliar de recomendação não foi validada como medida de qualidade percebida. O estudo com participantes ocorreu separadamente, em interfaces no Figma, com cliques e tempos registrados automaticamente pelo Useberry.

A proposta adota uma interface curta de avaliação e mantém uma implementação local de registro de eventos e feedback. A visualização administrativa disponível apresenta alertas, contagens por serviço e médias de respostas. Identificação de sessões críticas, recorrência de atributos, taxa de resposta por fluxo e acompanhamento de melhorias são capacidades planejadas, não resultados entregues pelo painel. A Lean Inception orientou a delimitação do produto e do MVP, cujas funcionalidades foram implementadas parcialmente ([Caroli, 2018](#ref-caroli2018leanInception); [Fowler; Caroli, 2022](#ref-fowler2022leanInception)).

## 1.2 Problema de Pesquisa

A questão investigada é como relacionar a avaliação declarada pelo cidadão ao contexto de navegação em que ela é solicitada. Quando a coleta fica restrita ao final da jornada, pode deixar de registrar detalhes de uma etapa anterior ou de um fluxo interrompido. Essa possibilidade motiva o estudo do momento do convite, sem pressupor que a coleta contextual produza resultados superiores. Indicadores só se tornam úteis à gestão quando seu contexto e suas limitações são considerados ([Government Digital Service, 2021b](#ref-govuk2021usingData); [DeLone; McLean, 2003](#ref-deloneMclean2003)).

Modelos oficiais e instrumentos consolidados de avaliação de serviços públicos contribuem para a mensuração da satisfação e da qualidade percebida. Ainda assim, permanecem desafios relacionados à baixa adesão, ao esforço exigido do usuário e à transformação das respostas em informação acionável para o gestor. Avaliações longas podem reduzir a participação; avaliações curtas podem gerar indicadores pouco explicativos; dados de navegação sem interpretação podem produzir apenas registros técnicos sem valor gerencial. A literatura científica mostra que taxas de resposta variam entre modos de coleta e populações, e que a formulação e o contexto das perguntas influenciam os relatos dos respondentes ([Shih; Fan, 2008](#ref-shihFan2008responseRates); [Lozar Manfreda et al., 2008](#ref-manfreda2008webSurveys); [Schwarz, 1999](#ref-schwarz1999selfReports)). Esses estudos justificam examinar adesão e desenho da coleta, mas não demonstram superioridade do feedback contextual em serviços públicos digitais. O uso dos registros para melhoria também exige interpretação dos dados de desempenho e atenção à relação entre qualidade do sistema, satisfação e benefícios ([Government Digital Service, 2021b](#ref-govuk2021usingData); [DeLone; McLean, 2003](#ref-deloneMclean2003)).

Este trabalho parte da seguinte questão de pesquisa: como propor e prototipar um avaliador de serviços públicos digitais que identifique sinais de possível dificuldade na navegação, colete feedback contextual de baixo esforço e organize informações úteis para a melhoria dos serviços avaliados?

A comparação entre convite contextual e formulário final foi organizada nas hipóteses H1 e H2, formuladas na seção 3.5. Elas tratam, respectivamente, de participação e especificidade dos comentários do formulário. Os resultados disponíveis são observações exploratórias de interface e não testam essas hipóteses.

## 1.3 Objetivo Geral

Propor e desenvolver um protótipo inicial de avaliador de serviços públicos digitais capaz de registrar sinais de possível dificuldade na navegação, coletar feedback contextual estruturado, comparar esse fluxo com uma avaliação estática e apresentar indicadores administrativos que apoiem a melhoria contínua dos serviços.

## 1.4 Objetivos Específicos

Para alcançar o objetivo geral, foram definidos os seguintes objetivos específicos:

- levantar fundamentos legais, técnicos e teóricos sobre avaliação de serviços públicos, qualidade percebida, usabilidade, governo digital e Lean Inception;

- definir, por meio de Lean Inception, o fluxo de detecção de possível dificuldade, sugestão de redirecionamento e coleta de feedback;

- construir um protótipo funcional com API, páginas simuladas de serviço público, feedback contextual, formulário estático comparativo e visualização administrativa;

- estruturar os dados e indicadores necessários para apoiar a análise de cliques, tempo de navegação, taxa de resposta, avaliações, NPS e pontos recorrentes de melhoria.

A estrutura dos objetivos combina a fundamentação legal e técnica da avaliação de serviços públicos com práticas de definição de MVP e prototipação de software ([Brasil, 2017b](#ref-brasil2017lei13460); [Brasil, 2021](#ref-brasil2021lei14129); [Caroli, 2018](#ref-caroli2018leanInception); [Sommerville, 2011](#ref-Sommerville2011)).

## 1.5 Justificativa

Mecanismos digitais de avaliação podem fortalecer a participação do usuário na melhoria dos serviços públicos. Os materiais da Enap destacam que a avaliação centrada no cidadão desloca o foco das ferramentas tecnológicas para as necessidades, demandas e satisfação dos usuários ([Lima; Pereira, 2020a](#ref-limaPereira2020modulo1)). Também indicam que avaliações devem alimentar ciclos de melhoria, permitindo identificar problemas recorrentes, atributos críticos e prioridades de intervenção ([Lima; Pereira, 2020d](#ref-limaPereira2020modulo4)).

A proposta é relevante porque muitos usuários já conhecem avaliações simples por estrelas, motivos e comentários. Uma solução pública pode aproveitar essa familiaridade para reduzir o esforço de resposta, desde que use os dados para finalidades compatíveis com o interesse público. Além disso, a combinação entre eventos de navegação e feedback declarado permite que o gestor observe tanto o que o usuário informou quanto o que ocorreu durante a jornada digital.

Do ponto de vista investigativo, o trabalho formula hipóteses sobre o momento da coleta e distingue indícios comportamentais de percepção declarada. Trata-se de uma organização conceitual ainda sujeita à formalização da tabela construto → indicador → dado e à avaliação empírica. Do ponto de vista tecnológico, a contribuição é a implementação de API, telas, regras explícitas e painel que permitem associar contexto de navegação e relato do cidadão. A explicitação das regras permite inspecionar o código, mas não equivale a auditoria independente nem a versionamento formal das configurações ([DeLone; McLean, 2003](#ref-deloneMclean2003); [Hevner et al., 2004](#ref-hevner2004designscience); [Sommerville, 2011](#ref-Sommerville2011)).

## 1.6 Escopo Inicial

O escopo inicial concentra-se na proposta e prototipação de uma solução. O trabalho não pretende implantar um sistema em ambiente governamental real, nem substituir instrumentos oficiais de avaliação já existentes. A solução é complementar e exploratória: simula páginas de serviço público, registra eventos de navegação, aplica regras configuráveis de acionamento por sinais de possível dificuldade, abre uma coleta simples de feedback, inclui um formulário reutilizável e apresenta dados administrativos agregados. A comparação entre formulário final e convite contextual pertence ao desenho de interface no Figma; a aplicação Python ainda não distingue os grupos nem registra a exposição. Essa delimitação segue a lógica de prototipação como forma de reduzir incertezas antes de uma solução definitiva e mantém cuidado com minimização de dados pessoais ([Sommerville, 2011](#ref-Sommerville2011); [Brasil, 2018](#ref-brasil2018lgpd)).

A avaliação desta etapa reúne procedimentos distintos: inspeção funcional e heurística interna/preliminar relatada pelos autores, e sessões exploratórias de interface com oito participantes no Figma, instrumentadas pelo Useberry. Essas sessões não constituem teste de integração ou execução da API Python. Os resultados são descritivos, sem generalização estatística ou validação em contexto real de prestação de serviço público. Integração com portais governamentais, calibração e estudo comparativo permanecem etapas futuras.

# 2 Referencial Teórico

Avaliar um serviço público digital exige olhar para mais do que a tela final de confirmação. A experiência do cidadão começa quando ele tenta entender onde está o serviço, continua nos caminhos que percorre e termina apenas quando a demanda é resolvida ou abandonada. Por isso, este capítulo reúne os fundamentos que sustentam a proposta do avaliador: conceitos de serviço público, satisfação, qualidade percebida, usabilidade, modelos brasileiros de avaliação e sinais de possível dificuldade observáveis durante a navegação.

O capítulo também parte de uma tradição anterior à digitalização dos serviços: os modelos clássicos de qualidade em serviços. Essa base é importante porque mostra que a percepção do usuário sempre dependeu da comparação entre o que ele esperava receber e o que efetivamente experimentou. No ambiente público digital, essa comparação passa a envolver, além do resultado do serviço, a clareza da informação, a confiança no canal, a facilidade de navegação, o esforço exigido e a capacidade do órgão de responder ao problema identificado ([Grönroos, 1984](#ref-gronroos1984service); [Parasuraman et al., 1988](#ref-parasuraman1988servqual); [DeLone; McLean, 2003](#ref-deloneMclean2003)).

## 2.1 Serviços e Serviços Públicos

Serviços diferenciam-se de produtos porque são mais intangíveis, ocorrem como séries de atividades, envolvem algum grau de interação com o usuário e, em muitos casos, são produzidos e consumidos simultaneamente. Essa característica torna a avaliação de serviços mais dependente da experiência vivida pelo usuário, e não apenas de propriedades observáveis de um bem material ([Grönroos, 1984](#ref-gronroos1984service); [Lima; Pereira, 2020a](#ref-limaPereira2020modulo1)).

No setor público, o serviço é parte do relacionamento entre cidadão e Estado. Ele pode envolver uma entrega individualizada, como a emissão de um documento, ou uma entrega de interesse coletivo, como segurança, educação, saúde e infraestrutura. Por isso, a avaliação de serviços públicos possui uma dimensão adicional: além de medir satisfação ou qualidade, ela se conecta ao exercício da cidadania, à prestação de contas e ao aperfeiçoamento da administração pública ([Brasil, 2017b](#ref-brasil2017lei13460); [Brasil, 2021](#ref-brasil2021lei14129); [Lima; Pereira, 2020a](#ref-limaPereira2020modulo1)).

Com a digitalização, muitos serviços passaram a ser acessados por portais, aplicativos e sistemas integrados. Essa mudança amplia o alcance da prestação pública, mas também cria novas exigências de usabilidade, clareza, confiabilidade e disponibilidade. A usabilidade pode ser entendida como resultado de uso associado à efetividade, eficiência e satisfação em um contexto definido ([International Organization for Standardization, 2018](#ref-iso9241112018)). O usuário não avalia apenas o resultado final do serviço; ele também avalia o caminho percorrido, a linguagem utilizada, o esforço exigido, a facilidade de navegação e a capacidade do canal digital de resolver sua demanda.

## 2.2 Avaliação de Serviços

A avaliação de serviços pode ser entendida como uma investigação qualitativa ou quantitativa sobre a qualidade do serviço e a satisfação do usuário, considerando a relação entre expectativa e experiência concreta ([Lima; Pereira, 2020a](#ref-limaPereira2020modulo1)). Em outras palavras, avaliar um serviço significa observar se a entrega realizada corresponde ao que o usuário precisava, esperava ou considerava adequado. Modelos clássicos de qualidade de serviço indicam que a percepção do usuário é formada por lacunas entre o serviço esperado e o serviço recebido. O modelo de qualidade percebida de [Grönroos (1984)](#ref-gronroos1984service) e o modelo SERVQUAL de [Parasuraman et al. (1988)](#ref-parasuraman1988servqual) consolidaram a ideia de que qualidade em serviços depende de fatores como confiabilidade, responsividade, segurança, empatia e aspectos tangíveis. Embora esses modelos tenham origem no setor privado, eles influenciaram diversas iniciativas posteriores de avaliação de serviços públicos e serviços digitais.

No SERVQUAL, essas dimensões aparecem como tangibilidade, confiabilidade, responsividade, garantia e empatia. A contribuição central do modelo é tratar a qualidade percebida como diferença entre expectativa prévia e percepção após a experiência. Para serviços públicos, entretanto, essa leitura exige adaptação: o cidadão geralmente não escolhe entre prestadores concorrentes e muitas vezes depende daquele serviço para exercer um direito, cumprir uma obrigação ou acessar um benefício. Assim, a expectativa não é formada apenas por comparação de mercado, mas também por experiências anteriores com o Estado, comunicação institucional, relatos de outros usuários e, mais recentemente, pela comparação com serviços digitais privados que oferecem interfaces mais rápidas e responsivas ([Parasuraman et al., 1988](#ref-parasuraman1988servqual); [Lima; Pereira, 2020b](#ref-limaPereira2020modulo2)).

Nos serviços digitais, a avaliação passou a incorporar fatores ligados ao uso de sistemas de informação, como qualidade do sistema, qualidade da informação, qualidade do serviço, intenção de uso, satisfação do usuário e benefícios percebidos. Os materiais da Enap destacam que, à medida que cidadãos passaram a interagir com sistemas governamentais digitais, tornou-se necessário adotar modelos capazes de avaliar não apenas páginas ou portais, mas a experiência do usuário ao longo da prestação do serviço ([Lima; Pereira, 2020b](#ref-limaPereira2020modulo2); [DeLone; McLean, 2003](#ref-deloneMclean2003); [Pedrosa et al., 2019](#ref-pedrosa2019qualidadeGovbr)).

## 2.3 Satisfação e Qualidade Percebida

Satisfação e qualidade percebida são conceitos próximos, mas não idênticos. A satisfação costuma expressar um julgamento global do usuário após consumir o serviço, enquanto a qualidade percebida pode ser decomposta em atributos mais específicos da experiência, como rapidez, clareza das informações, atendimento, esforço, confiabilidade e facilidade de uso. Para [Oliver (2014)](#ref-oliver2014satisfaction), a satisfação está relacionada ao julgamento do usuário sobre o grau em que uma experiência atendeu ou não suas expectativas.

No contexto público, a distinção entre satisfação e qualidade percebida é importante porque uma nota geral, sozinha, nem sempre indica o que deve ser melhorado. Um usuário pode avaliar mal um serviço por demora, linguagem confusa, instabilidade do sistema, falta de atendimento ou excesso de etapas. Portanto, um avaliador de serviços públicos precisa combinar uma avaliação simples, como nota ou estrelas, com mecanismos que ajudem a qualificar o motivo da avaliação.

Essa lógica aparece na evolução dos instrumentos brasileiros de avaliação. O BRASP considera a qualidade percebida como um elemento central para compreender a experiência do usuário e apoiar o aprimoramento dos serviços ([Silva et al., 2019](#ref-silva2019brasp)). A proposta de modelo unificado busca integrar qualidade técnica, qualidade percebida, efetividade e satisfação, reduzindo o custo de resposta para o cidadão e tornando os resultados mais úteis para a gestão ([Silva; Menezes, 2022](#ref-silva2022modeloUnificado)).

## 2.4 Avaliação de Serviços Públicos no Brasil

A avaliação de serviços públicos no Brasil possui base normativa e base técnica. Do ponto de vista normativo, a Lei n<sup>o</sup> 13.460/2017 estabelece direitos dos usuários e prevê que os resultados de avaliação subsidiem a reorientação dos serviços ([Brasil, 2017b](#ref-brasil2017lei13460)). O Decreto n<sup>o</sup> 9.094/2017 institui a Carta de Serviços ao Usuário e reforça o uso de ferramenta de pesquisa de satisfação no governo federal ([Brasil, 2017a](#ref-brasil2017decreto9094)). A Lei n<sup>o</sup> 14.129/2021 relaciona o governo digital à eficiência pública, à desburocratização e à participação do cidadão ([Brasil, 2021](#ref-brasil2021lei14129)).

A partir desse conjunto normativo, a avaliação deixa de ser apenas uma prática gerencial desejável e passa a compor o próprio modo de prestação dos serviços públicos digitais. A Lei de Acesso à Informação reforça a transparência como base para acompanhamento social; a Lei n<sup>o</sup> 13.460/2017 vincula avaliação à proteção do usuário; a Lei do Governo Digital incorpora canais digitais de participação; e normas infralegais detalham instrumentos de simplificação, monitoramento e avaliação de satisfação. A Tabela [1](#tab:marcos-legais-avaliacao) resume os marcos mais relevantes para este trabalho.

<a id="tab:marcos-legais-avaliacao"></a>

**Tabela 1 — Marcos legais nacionais sobre avaliação de serviços públicos digitais**

| **Instrumento** | **Ano** | **Principais disposições relevantes** |
|:---|:---|:---|
| Lei n<sup>o</sup> 12.527 (LAI) ([Brasil, 2011](#ref-brasil2011lei12527)) | 2011 | Transparência ativa e passiva; base para acesso a informações públicas e dados sobre desempenho de serviços. |
| Lei n<sup>o</sup> 13.460 ([Brasil, 2017b](#ref-brasil2017lei13460)) | 2017 | Direitos do usuário, participação na avaliação dos serviços e uso dos resultados para reorientação da prestação pública. |
| Decreto n<sup>o</sup> 9.094 ([Brasil, 2017a](#ref-brasil2017decreto9094)) | 2017 | Simplificação do atendimento, Carta de Serviços ao Usuário e racionalização de exigências feitas ao cidadão. |
| Lei n<sup>o</sup> 14.129 ([Brasil, 2021](#ref-brasil2021lei14129)) | 2021 | Governo digital, eficiência pública, desburocratização, canais digitais de participação e melhoria da prestação estatal. |
| Decreto n<sup>o</sup> 11.260 ([Brasil, 2022](#ref-brasil2022decreto11260)) | 2022 | Elaboração e encaminhamento da Estratégia Nacional de Governo Digital, com organização das diretrizes de transformação digital. |
| Portaria SGD/ME n<sup>o</sup> 548 ([Brasil. Secretaria de Governo Digital, 2022](#ref-brasil2022portaria548)) | 2022 | Avaliação de satisfação dos usuários e padrões de qualidade para serviços públicos digitais. |


Fonte: elaborada pelos autores com base na legislação federal brasileira.

Do ponto de vista técnico, relatórios produzidos no âmbito da Universidade de Brasília, da Secretaria de Governo Digital e de instituições parceiras apresentam modelos voltados à mensuração da qualidade de serviços públicos digitais. A proposta Qualidade Gov.br organiza a avaliação em dimensões ligadas à consistência digital e à experiência do usuário, reconhecendo que a qualidade de um serviço digital depende tanto dos requisitos técnicos quanto da jornada do cidadão ([Pedrosa et al., 2019](#ref-pedrosa2019qualidadeGovbr)). O BRASP amplia essa discussão ao considerar serviços presenciais, digitizados e parcialmente digitizados ([Silva et al., 2019](#ref-silva2019brasp)).

O avanço desses modelos demonstra que a avaliação pública precisa equilibrar rigor metodológico e simplicidade operacional. Instrumentos longos e complexos podem gerar dados ricos, mas tendem a aumentar o esforço do respondente. Por outro lado, instrumentos muito curtos podem ampliar a adesão, mas produzir dados insuficientes para orientar melhorias. Esse equilíbrio é especialmente relevante para a proposta deste TCC, que busca um avaliador simples para o cidadão e útil para a gestão.

## 2.5 BRASP, API de Avaliação e Modelo Unificado

O Modelo Brasileiro de Avaliação de Serviços Públicos (BRASP) foi desenvolvido para construir e validar instrumentos de avaliação da qualidade adaptados à realidade brasileira. O modelo considera três modalidades de prestação: serviços digitizados, serviços parcialmente digitizados e serviços presenciais ([Silva et al., 2019](#ref-silva2019brasp)). Essa diferenciação é relevante porque a experiência do usuário muda de acordo com o canal. Um serviço presencial pode depender mais de atendimento, espera e estrutura física; um serviço digital pode depender mais de facilidade de uso, clareza, disponibilidade e segurança; e um serviço híbrido pode combinar problemas de ambos os contextos.

Nos materiais da Enap, o modelo brasileiro de avaliação é apresentado como instrumento para identificar fatores relacionados à satisfação do usuário, localizar pontos críticos e gerar comparações capazes de acompanhar a evolução dos serviços. Essa leitura é coerente com o BRASP e com a proposta de modelo unificado, que organizam satisfação, qualidade percebida, qualidade técnica e efetividade como dimensões complementares de análise ([Lima; Pereira, 2020c](#ref-limaPereira2020modulo3); [Silva et al., 2019](#ref-silva2019brasp); [Silva; Menezes, 2022](#ref-silva2022modeloUnificado)). A pesquisa de satisfação aparece ancorada em uma pergunta geral sobre a experiência com o serviço, enquanto a qualidade percebida é investigada por atributos que ajudam a explicar essa experiência.

A API de avaliação do governo brasileiro segue uma lógica semelhante. Segundo o relatório sobre os atributos da API, a satisfação é medida por uma estratégia simples inspirada no CSAT, com resposta por opções associadas a estrelas, e a qualidade percebida é explorada por atributos como clareza das informações, custo ou esforço para obtenção do serviço, disponibilidade, eficácia, facilidade de uso, qualidade dos canais de comunicação e tempo para obtenção do serviço ([Silva, 2024](#ref-silva2024atributosApi)). Essa abordagem se aproxima da proposta deste trabalho, pois combina avaliação rápida com categorização do motivo da nota.

A proposta de modelo unificado reforça essa direção ao articular quatro eixos: qualidade técnica, qualidade percebida, satisfação do usuário e efetividade ([Silva; Menezes, 2022](#ref-silva2022modeloUnificado)). Para um avaliador de serviços públicos, esses eixos podem orientar tanto a coleta quanto a visualização de dados. A satisfação indica o julgamento geral do cidadão; a qualidade percebida explica a experiência por atributos; a qualidade técnica pode apoiar análises de disponibilidade, integração e consistência; e a efetividade aproxima a avaliação da pergunta central: o serviço resolveu a necessidade do usuário?

## 2.6 Usabilidade, Inclusão Digital e Métricas de Experiência

A usabilidade em serviços públicos digitais possui impacto mais amplo do que em produtos privados. Quando uma interface privada é difícil, o usuário pode trocar de fornecedor; quando um serviço público digital é difícil, o cidadão pode perder prazo, deixar de acessar um benefício, não concluir uma obrigação ou depender de atendimento presencial. Por isso, os princípios de usabilidade precisam ser interpretados como parte do acesso efetivo ao serviço. As heurísticas de [Nielsen (1994)](#ref-nielsen1994heuristic), como visibilidade do status do sistema, correspondência entre linguagem da interface e linguagem do usuário, prevenção de erros e ajuda contextual, são diretamente relacionadas aos problemas que o avaliador busca observar durante a navegação.

A representatividade também é um ponto relevante. Serviços públicos atendem usuários com diferentes níveis de letramento digital, conectividade, idade, familiaridade com formulários e capacidade de compreender linguagem institucional. Os dados do PPA Participativo 2024-2027 indicam que participação digital em larga escala pode conviver com barreiras de uso e de retorno ao cidadão ([Brasil. Ministério da Gestão e da Inovação em Serviços Públicos, 2024](#ref-brasilMgi2024ppaParticipativo)). Da mesma forma, pesquisas sobre acesso às tecnologias de informação no Brasil mostram que o uso de serviços digitais ainda depende de condições desiguais de acesso, dispositivos e habilidades ([Comitê Gestor da Internet no Brasil, 2025](#ref-cetic2025ticDomicilios2024)). Para este TCC, isso reforça a necessidade de uma coleta de feedback simples, opcional e de baixo esforço.

Métricas como NPS, CSAT e CES ajudam a decompor a experiência. O NPS popularizou a pergunta de recomendação em escala de 0 a 10 ([Reichheld, 2003](#ref-reichheld2003nps)); em serviços públicos, sua leitura precisa ser adaptada, pois o cidadão nem sempre escolhe usar ou recomendar um serviço estatal. O CSAT registra satisfação imediata com uma interação específica, normalmente por uma escala curta. O CES mede o esforço percebido para concluir uma tarefa, aspecto especialmente importante em serviços públicos com muitas etapas ou linguagem burocrática. O momento da coleta pode influenciar a recordação e a interpretação da experiência. Resultados sobre avaliação retrospectiva motivam investigar esse efeito, mas não demonstram, isoladamente, a vantagem de um momento de coleta no cenário deste trabalho ([Kahneman et al., 1993](#ref-kahneman1993peakEnd)).

No formulário implementado, as estrelas registram uma avaliação geral e os atributos permitem declarar problemas associados a clareza, tempo percebido, esforço, usabilidade, atendimento ou eficácia. A pergunta auxiliar de recomendação, identificada como NPS na interface, permaneceu no instrumento, mas sua média de 0 a 10 não constitui cálculo do escore NPS nem valida sua interpretação no setor público. Sua resposta não é tratada como medida equivalente às estrelas ou aos atributos de qualidade percebida.

## 2.7 Experiência do Usuário e Avaliações Inspiradas em Plataformas Digitais

Plataformas digitais privadas popularizaram formas de avaliação de baixo esforço: nota de uma a cinco estrelas, comentários curtos, seleção de motivos e visualização agregada das avaliações. A referência a aplicações como plataformas de entrega deve ser entendida como inspiração de interação, e não como modelo de governança. Em uma plataforma privada, a avaliação frequentemente orienta reputação, consumo e concorrência. Em serviços públicos, ela deve orientar direitos, transparência, participação social e melhoria da entrega estatal. Mecanismos como o NPS, proposto originalmente como pergunta de lealdade e recomendação, também influenciaram práticas de avaliação de experiência por sua simplicidade de aplicação ([Reichheld, 2003](#ref-reichheld2003nps)).

Mesmo com essa diferença, a familiaridade do usuário com mecanismos simples de avaliação pode ser aproveitada. Um avaliador de serviços públicos pode reduzir barreiras de participação se oferecer uma interface direta, com poucos passos e linguagem compreensível. A nota geral permite captar a percepção imediata; os atributos permitem interpretar os motivos; e comentários opcionais podem revelar problemas não previstos pelo formulário. Essa escolha está alinhada ao design centrado no usuário, que orienta o desenvolvimento de sistemas interativos a partir das necessidades, capacidades e limitações das pessoas que irão utilizá-los ([International Organization for Standardization, 2019](#ref-iso92412102019)).

Para que a avaliação seja útil ao gestor, o sistema também precisa organizar os dados coletados. Isso envolve agrupar avaliações por serviço, período, órgão, canal e atributo; identificar itens recorrentes; apresentar médias e distribuições; e permitir comparação temporal. A literatura de melhoria de serviços reforça que as avaliações devem alimentar ciclos de melhoria contínua, funcionando como linha de base para decisões e como indicador para acompanhar a evolução do serviço ([Lima; Pereira, 2020d](#ref-limaPereira2020modulo4); [Government Digital Service, 2021b](#ref-govuk2021usingData); [Brasil, 2026](#ref-govbrFerramentaAvaliacao)).

### 2.7.1 Posicionamento em relação a soluções existentes

Embora o protótipo dialogue com ferramentas existentes de avaliação e análise de experiência, sua contribuição não está em substituí-las nem em afirmar superioridade. A contribuição está em combinar, em um MVP com regras explícitas e voltado a serviços públicos, sinais simples de possível dificuldade durante a navegação, coleta contextual de baixo esforço e organização administrativa dos dados por serviço e atributo.

A ferramenta oficial de avaliação do gov.br constitui uma referência institucional para medir satisfação em serviços públicos digitais. Ferramentas comerciais como Hotjar e Microsoft Clarity oferecem funcionalidades de analytics comportamental, mapas de calor, gravações de sessão e feedback. Suas páginas de documentação são utilizadas neste trabalho somente para caracterização tecnológica das funcionalidades declaradas, e não como evidência científica de eficácia ou adequação ao setor público ([Brasil, 2026](#ref-govbrFerramentaAvaliacao); [HOTJAR, 2026](#ref-hotjar2026); [MICROSOFT, 2026](#ref-microsoftClarity2026)). O Government Digital Service, por sua vez, é uma fonte institucional e metodológica sobre uso de dados de desempenho na melhoria de serviços digitais ([Government Digital Service, 2021b](#ref-govuk2021usingData)).

A Tabela [2](#tab:posicionamento-solucoes) sintetiza esse posicionamento.

<a id="tab:posicionamento-solucoes"></a>

**Tabela 2 — Posicionamento da proposta em relação a soluções existentes**

| **Solução** | **Foco principal** | **Contribuição** | **Limite em relação a este TCC** |
|:---|:---|:---|:---|
| Ferramenta de avaliação do gov.br | Avaliação institucional de satisfação | Padronização oficial no governo digital brasileiro | Não enfatiza, no escopo analisado, gatilhos baseados em cliques e tempo durante a jornada. |
| Hotjar | Analytics comportamental, mapas de calor, gravações e feedback | Observação de comportamento em sites | Documentação comercial; requer adaptação à governança pública e à minimização de dados. |
| Microsoft Clarity | Análise de sessões, mapas de calor e navegação | Observabilidade detalhada de páginas web | Documentação comercial; não constitui modelo de avaliação de serviço público. |
| GDS UK | Medição e melhoria de serviços digitais | Referência metodológica institucional para uso de dados | Contexto institucional distinto e sem equivalência direta ao protótipo. |
| Artefato deste TCC | Implementação local Python e interfaces de avaliação no Figma | Implementação parcial de eventos, feedback e painel; observações exploratórias de interface | Inspeção interna da implementação e avaliação de interface Figma/Useberry são procedimentos distintos. O estudo com participantes não verifica a API nem valida o serviço em contexto real. |


Fonte: elaborada pelos autores (2026).

A comparação é documental e de posicionamento: baseia-se nas funcionalidades declaradas pelas fontes institucionais e comerciais, sem teste independente ou auditoria técnica das soluções. Assim, delimita a lacuna explorada pelo trabalho sem transformar documentação de ferramentas em evidência científica.

## 2.8 Métricas de Navegação e Sinais de Dificuldade

Além do feedback declarado pelo usuário, serviços digitais podem ser avaliados por sinais observados durante a jornada. A taxa de conclusão, por exemplo, mede a proporção de transações iniciadas que chegam ao ponto definido como conclusão do serviço; sua leitura depende de identificar início, etapas intermediárias, abandono e término do fluxo ([Government Digital Service, 2021a](#ref-govuk2021completionRate)). Métricas de tempo, cliques, páginas visitadas e retorno a etapas anteriores também podem indicar dificuldade quando comparadas a faixas esperadas.

O uso dessas métricas aproxima a avaliação de serviços públicos da avaliação de sistemas de informação. O modelo de sucesso de sistemas de informação de [DeLone; McLean (2003)](#ref-deloneMclean2003) relaciona qualidade do sistema, qualidade da informação, qualidade do serviço, uso, satisfação do usuário e benefícios líquidos. Para a solução proposta, cliques, tempo e sequência de navegação são evidências comportamentais de possível esforço ou dificuldade. Eles não medem qualidade percebida. Estrelas, atributos e comentários constituem evidências declaradas sobre a experiência. A pergunta auxiliar de recomendação possui interpretação distinta e não foi validada como medida de qualidade percebida. A contribuição analítica está em relacionar essas fontes sem fundi-las: a telemetria localiza o contexto e o feedback permite interpretar a percepção.

O registro de eventos de navegação exige cuidado metodológico e jurídico. A coleta deve ser limitada ao necessário para a finalidade de melhoria do serviço, com uso de identificador técnico e minimização dos campos registrados, sem presumir anonimização. A Lei Geral de Proteção de Dados Pessoais estabelece princípios para o tratamento de dados, inclusive em meios digitais, com objetivo de proteger liberdade, privacidade e desenvolvimento da personalidade da pessoa natural ([Brasil, 2018](#ref-brasil2018lgpd)). Por isso, a proposta deste TCC considera o registro de cliques e tempo como mecanismo de análise agregada, não como instrumento de vigilância individual.

<a id="sec:feedback-contextual"></a>

## 2.9 Feedback Contextual e Acionamento por Sinais de Uso

O feedback contextual busca aproximar a coleta declarada do ponto da jornada em que uma experiência ocorre. Essa proposta dialoga com o Experience Sampling Method (ESM), desenvolvido para coletar autorrelatos durante a vida cotidiana ([Larson; Csikszentmihalyi, 1983](#ref-larson1983experienceSampling); [Hektner et al., 2007](#ref-hektner2007experienceSampling)). No presente trabalho, essa relação é conceitual: o convite acionado por um evento de navegação não representa, por si só, a aplicação integral de um protocolo de ESM.

A proximidade temporal pode reduzir a dependência de recordações retrospectivas e permitir investigar relatos mais situados. Estudos sobre avaliação retrospectiva mostram que o desfecho pode influenciar o julgamento de uma experiência ([Kahneman et al., 1993](#ref-kahneman1993peakEnd)); esse resultado não comprova que perguntar durante uma dificuldade de navegação produza respostas melhores. A formulação, as opções de resposta e o contexto da pergunta também influenciam o autorrelato ([Schwarz, 1999](#ref-schwarz1999selfReports)).

A eventual vantagem de obter um comentário mais específico precisa ser confrontada com o custo da interrupção. O estudo de [Mark et al. (2008)](#ref-mark2008interruptedWork) identificou maior estresse associado a interrupções em tarefas de trabalho. Esse achado oferece um motivo para investigar a intrusão do convite, sem estabelecer seu efeito no cenário deste TCC. Por isso, a pergunta contextual deve ser curta e opcional, e sua adequação precisa ser avaliada pelos usuários.

No protótipo deste TCC, os gatilhos comportamentais foram reduzidos a regras simples e explícitas: excesso de cliques, tempo acima da faixa esperada e persistência do sinal após a sugestão de redirecionamento. Esses sinais não substituem a percepção do usuário, mas indicam quando faz sentido solicitar uma avaliação de baixo esforço. A escolha por regras explícitas preserva a rastreabilidade do MVP e evita que a solução dependa de modelos estatísticos complexos antes de haver dados reais suficientes para calibração.

Esse tipo de coleta também precisa respeitar a carga cognitiva do cidadão. Questionários longos ou tecnicamente ambíguos aumentam esforço, erro e abandono. A Teoria da Carga Cognitiva indica que a memória de trabalho humana possui capacidade limitada; portanto, interfaces de feedback devem usar linguagem direta, poucas perguntas, opções de resposta claras e campos textuais opcionais ([Sweller, 1988](#ref-sweller1988cognitiveLoad)). O formulário reúne estrelas, atributos, pergunta auxiliar de recomendação e comentário opcional. Essa decisão de projeto não demonstra esforço reduzido ou utilidade dos dados, propriedades que dependem de avaliação específica.

## 2.10 Síntese do Referencial

O referencial teórico indica que a proposta de um avaliador de serviços públicos deve considerar quatro princípios. O primeiro é a centralidade do cidadão: a avaliação precisa capturar a experiência real do usuário, e não apenas métricas internas da administração. O segundo é a decomposição da avaliação em atributos: uma nota geral é útil, mas precisa ser acompanhada de critérios que expliquem o motivo da satisfação ou insatisfação. O terceiro é a orientação para melhoria: os dados coletados devem ser estruturados para apoiar decisões de gestão e acompanhar a evolução dos serviços. O quarto é a contextualidade como hipótese de desenho: investigar se aproximar a pergunta de um sinal de possível dificuldade altera a participação e o conteúdo das respostas, sem presumir que essa aproximação produza evidências melhores.

Com base nesses princípios, este TCC propõe um avaliador inspirado em interfaces simples de plataformas digitais, mas fundamentado em modelos de avaliação de serviços públicos, usabilidade, design centrado no usuário e sucesso de sistemas de informação. A solução deve permitir que o usuário avalie um serviço de forma rápida e compreensível, enquanto eventos de navegação e resultados agregados oferecem ao gestor indícios sobre quais aspectos do serviço precisam de priorização e aperfeiçoamento.

# 3 Metodologia

Este capítulo apresenta o caminho seguido para transformar a ideia do sistema de avaliação contextual em um protótipo demonstrável. A metodologia combinou pesquisa aplicada, revisão bibliográfica e normativa, Design Science Research, prototipação incremental e Lean Inception, de modo que a definição do produto e a implementação técnica avançassem de forma coerente.

## 3.1 Caracterização da Pesquisa

A pesquisa é aplicada e exploratória: propõe uma solução computacional para relacionar contexto de navegação e avaliação declarada em serviços públicos digitais. O artefato possui dois componentes: uma implementação funcional local em Python, com API, páginas, formulário e painel; e um protótipo de interface no Figma, com os fluxos A e B usados no estudo com participantes. A implementação recebeu inspeção interna funcional e heurística. As interfaces no Figma receberam avaliação exploratória de usabilidade, instrumentada pelo Useberry. Nenhum desses procedimentos constitui validação em contexto real de prestação de serviço público.

O percurso dialoga com a Design Science Research, na qual a construção e a avaliação de artefatos apoiam a produção de conhecimento em sistemas de informação ([Hevner et al., 2004](#ref-hevner2004designscience)). A demonstração técnica da implementação e as observações de interface oferecem evidências de naturezas diferentes. A avaliação com oito participantes se refere às interfaces no Figma; não verifica os endpoints, a persistência ou os gatilhos da implementação Python. A estruturação completa do percurso pelas etapas da DSR permanece parte da continuidade metodológica.

As fontes foram diferenciadas por natureza e finalidade. Artigos e livros acadêmicos fundamentam conceitos e questões de pesquisa; normas oferecem definições e critérios; legislação caracteriza o enquadramento normativo; relatórios técnicos e materiais institucionais descrevem modelos e práticas de governo digital. Os módulos da Enap são material didático institucional. Caroli, Fowler e Caroli, Cooper e Kalbach são usados como literatura profissional de concepção e projeto; Reichheld caracteriza a proposta original de NPS, sem constituir validação desse indicador para serviços públicos. Hotjar, Microsoft Clarity e Useberry são documentação comercial, limitada à descrição de funcionalidades declaradas e instrumentos utilizados. A classificação das fontes é apresentada a seguir; a presença de uma fonte não comprova a eficácia do mecanismo proposto.


- **Legislação:** [Brasil](#ref-brasil2011lei12527); [Brasil](#ref-brasil2017decreto9094); [Brasil](#ref-brasil2017lei13460); [Brasil](#ref-brasil2018lgpd); [Brasil](#ref-brasil2021lei14129); [Brasil](#ref-brasil2022decreto11260); [Brasil. Secretaria de Governo Digital](#ref-brasil2022portaria548).

- **Documentação ou pesquisa institucional:** [Brasil](#ref-govbrFerramentaAvaliacao); [Brasil. Ministério da Gestão e da Inovação em Serviços Públicos](#ref-brasilMgi2024ppaParticipativo); [Comitê Gestor da Internet no Brasil](#ref-cetic2025ticDomicilios2024); [Government Digital Service](#ref-govuk2021completionRate); [Government Digital Service](#ref-govuk2021usingData).

- **Literatura profissional:** [Caroli, Paulo](#ref-caroli2018leanInception); [Cooper, Alan](#ref-cooper1999inmates); [Fowler, Martin; Caroli, Paulo](#ref-fowler2022leanInception); [Kalbach, Jim](#ref-kalbach2016mapping); [Reichheld, Frederick F](#ref-reichheld2003nps).

- **Literatura acadêmica/científica:** [DeLone, William H.; McLean, Ephraim R](#ref-deloneMclean2003); [Grönroos, Christian](#ref-gronroos1984service); [Hektner, Joel M.; Schmidt, Jennifer A.; Csikszentmihalyi, Mihaly](#ref-hektner2007experienceSampling); [Hevner, Alan R.; March, Salvatore T.; Park, Jinsoo; Ram, Sudha](#ref-hevner2004designscience); [Kahneman, Daniel; Fredrickson, Barbara L.; Schreiber, Charles A.; Redelmeier, Donald A](#ref-kahneman1993peakEnd); [Larson, Reed; Csikszentmihalyi, Mihaly](#ref-larson1983experienceSampling); [Lozar Manfreda, Katja; Bosnjak, Michael; Berzelak, Jernej; Haas, Iris; Vehovar, Vasja](#ref-manfreda2008webSurveys); [Mark, Gloria; Gudith, Daniela; Klocke, Ulrich](#ref-mark2008interruptedWork); [Nielsen, Jakob](#ref-nielsen1994heuristic); [Oliver, Richard L](#ref-oliver2014satisfaction); [Parasuraman, A.; Zeithaml, Valarie A.; Berry, Leonard L](#ref-parasuraman1988servqual); [Schwarz, Norbert](#ref-schwarz1999selfReports); [Shih, Tse-Hua; Fan, Xitao](#ref-shihFan2008responseRates); [Sommerville, Ian](#ref-Sommerville2011); [Sweller, John](#ref-sweller1988cognitiveLoad).

- **Documentação comercial:** [HOTJAR](#ref-hotjar2026); [MICROSOFT](#ref-microsoftClarity2026); [Useberry](#ref-useberryFigma).

- **Norma técnica:** [International Organization for Standardization](#ref-iso9241112018); [International Organization for Standardization](#ref-iso92412102019).

- **Material didático institucional:** [Lima, Oto Buregio; Pereira, Wander Cleber](#ref-limaPereira2020modulo1); [Lima, Oto Buregio; Pereira, Wander Cleber](#ref-limaPereira2020modulo2); [Lima, Oto Buregio; Pereira, Wander Cleber](#ref-limaPereira2020modulo3); [Lima, Oto Buregio; Pereira, Wander Cleber](#ref-limaPereira2020modulo4).

- **Relatório técnico institucional:** [Pedrosa, Glauco Vitor; Gomes, Marília Miranda Forte; Silva, Wander Cleber Pereira; Sousa Oliveira Melo Veras, Daniel; Iwama, Gabriela Yukari; Menezes, Vítor Gomes](#ref-pedrosa2019qualidadeGovbr); [Silva, Wander Cleber M. P](#ref-silva2024atributosApi); [Silva, Wander Cleber Pereira; Gomes, Marília Miranda Forte; Pedrosa, Glauco Vitor; Andrade Soares, Vanessa; Iwama, Gabriela; Menezes, Vítor Gomes; Paiva Vaz, Daniele; Guedes, Débora Janini Campos; Costa Figueiredo, Rejane Maria](#ref-silva2019brasp); [Silva, Wander Cleber Pereira; Menezes, Vítor Gomes](#ref-silva2022modeloUnificado).

## 3.2 Lean Inception

A Lean Inception foi utilizada como protocolo metodológico para alinhar visão de produto, escopo e MVP. A abordagem de [Caroli (2018)](#ref-caroli2018leanInception) auxilia equipes a definir o produto certo antes de ampliar o desenvolvimento; [Fowler; Caroli (2022)](#ref-fowler2022leanInception) também a descreve como uma inception focada em compreender funcionalidades, clientes e Canvas MVP. Neste trabalho, a técnica organizou a definição do sistema de avaliação contextual e ajudou a transformar a ideia inicial em um conjunto priorizado de funcionalidades.

A atividade interna contou com quatro participantes. As perspectivas listadas a seguir representam suas contribuições à discussão, sem atribuir-lhes vínculo institucional ou condição de especialista independente:

- **Felipe**, atendimento público, representando dúvidas recorrentes e dificuldades relatadas por cidadãos;

- **Lucas**, gestão digital, representando a necessidade de indicadores acionáveis para priorização de melhorias;

- **Diassis**, estudante da UnB, representando viabilidade técnica, escopo acadêmico, segurança e LGPD;

- **Bruno**, estudante da UnB, representando experiência do usuário, jornada, clareza de interface e validação.

Lucas, participante da discussão, e Lucas Almeida, persona fictícia da seção 4.3, são referências distintas. A participação de Wesley Pedrosa dos Santos na Lean Inception esteve voltada ao tema de seu próprio trabalho; não é apresentada como avaliação independente do sistema aqui proposto. A dinâmica foi uma atividade interna de alinhamento e delimitação do produto, não uma validação externa. As decisões da Lean Inception não substituem especificação de requisitos, teste de usabilidade ou avaliação por especialistas independentes.

## 3.3 Etapas da Lean Inception

A agenda da Lean Inception foi organizada para que as funcionalidades surgissem a partir da jornada do usuário, e não apenas de possibilidades técnicas. As etapas executadas foram:

1.  **Kick-off**: alinhamento do problema, da hipótese e dos limites do MVP;

2.  **É / Não É / Faz / Não Faz**: delimitação do produto como solução de feedback contextual, não como ouvidoria, chatbot, ferramenta de identificação individual ou sistema governamental completo;

3.  **Objetivos do Produto**: definição de objetivos como capturar sinais de possível dificuldade, solicitar feedback no momento adequado, preservar privacidade e gerar dados acionáveis;

4.  **Personas**: definição de Carlos Pereira, cidadão usuário de serviço público digital, e Lucas Almeida, gestor público de serviço digital;

5.  **Jornadas**: comparação entre um fluxo com formulário estático ao final e um fluxo com feedback contextual durante a dificuldade;

6.  **Brainstorming de features**: levantamento de funcionalidades relacionadas a coleta de sinais, regras, feedback, painel e integração;

7.  **Revisão técnica, de negócio e UX**: avaliação relativa de esforço, valor para gestão e impacto na experiência do usuário;

8.  **Sequenciador**: organização das funcionalidades em ondas de entrega;

9.  **Canvas MVP**: consolidação da menor versão viável para validação inicial.

A construção de personas foi baseada na tradição de design centrado no usuário. [Cooper (1999)](#ref-cooper1999inmates) apresenta personas como arquétipos usados para orientar decisões de produto. O mapeamento de jornada seguiu a lógica de visualização de experiências discutida por [Kalbach (2016)](#ref-kalbach2016mapping), com identificação de pontos de contato, fricções e oportunidades de intervenção. As personas também consideraram o cenário brasileiro de uso de tecnologias digitais, descrito pela TIC Domicílios 2024 ([Comitê Gestor da Internet no Brasil, 2025](#ref-cetic2025ticDomicilios2024)), e a existência de mecanismos oficiais de avaliação de serviços públicos digitais ([Brasil, 2026](#ref-govbrFerramentaAvaliacao)).

## 3.4 Metodologia do Desenvolvimento da Solução

O desenvolvimento adotou prototipação incremental, com a finalidade de explorar decisões de solução e reduzir incertezas ([Sommerville, 2011](#ref-Sommerville2011)). A Lean Inception foi conduzida entre 18 e 27 de junho de 2026; a avaliação das interfaces no Figma ocorreu em 28 de junho de 2026. A existência de uma implementação funcional em Python antes das sessões não significa que ela tenha sido usada pelos participantes. Não se atribuem os resultados do Figma à API.

O sequenciador de concepção organizou cinco ondas:

1. **Onda 1 — Base técnica e desenho comparativo:** identificador de sessão, eventos e planejamento dos formulários contextual e final.
2. **Onda 2 — Regras e feedback:** condições de acionamento, sugestão de redirecionamento e formulário.
3. **Onda 3 — Painel básico:** agregações de eventos e respostas e planejamento de indicadores comparativos.
4. **Onda 4 — Incrementos de gestão:** parâmetros por serviço, filtros e apresentação de comentários.
5. **Onda 5 — Preparação de integração real:** organizações, autenticação, chave de API e cliente instalável.

As ondas 1 a 3 constituíram o MVP planejado, mas foram implementadas apenas em parte. Na aplicação Python existem identificadores técnicos, captura de cliques em elementos instrumentados, envio de duração simulada, regras, formulário reutilizável e agregações básicas. Não foram implementados cronômetro automático de navegação, registro dos grupos A/B, exposição ao convite, ranking por alertas ou taxa de resposta por fluxo. A comparação de interfaces foi realizada no Figma. Parâmetros por serviço, originalmente previstos como incremento da onda 4, já estão no backend; filtros e comentários recentes continuam pendentes. O sequenciador expressa o planejamento, não uma lista de entregas integralmente executadas.

## 3.5 Hipótese e Critérios da Avaliação Preliminar

As hipóteses direcionais propostas para um estudo futuro são: **H1**, em tarefas e condições equivalentes, o fluxo contextual terá maior proporção de participantes que enviam feedback do que o fluxo com formulário final; **H2**, os comentários enviados no fluxo contextual terão maior escore de especificidade do que os enviados no fluxo com formulário final, segundo rubrica definida antes da coleta. As hipóteses não foram testadas por esta avaliação exploratória. A regra de exposição ao convite e os denominadores deverão ser definidos previamente, com divulgação das respostas tanto por participante alocado quanto por participante exposto.

As variáveis previstas têm diferentes condições de observação nesta etapa:

- **Realização da avaliação:** considerou-se resposta, no fluxo A, quando o participante realizou a avaliação apresentada ao final da jornada e, no fluxo B, quando aceitou o convite e realizou a avaliação. Abrir o convite, sem realizar a avaliação, não corresponde a esse critério. Essa classificação não comprova envio de dados à API nem digitação de comentário. A exposição ao formulário final não foi discriminada para cada participante do A; as proporções por participante e por exposição devem permanecer distintas.
- **Conclusão da tarefa:** há classificação Sim/Parcial/Não; o resumo considera somente Sim como conclusão completa. Isso explicita o cálculo descritivo e não representa critério prévio de sucesso documentado.
- **Esforço percebido:** não foi medido por instrumento específico; a nota de facilidade do Apêndice F não corresponde ao CES.
- **Qualidade/especificidade dos comentários do formulário:** não há corpus separado nem rubrica aplicada. Os comentários do Apêndice G são do questionário pós-sessão e não permitem testar H2.
- **Interrupção e abandono associados ao convite:** há relatos pontuais de ignorar o convite; não há medida capaz de atribuir causalidade ao popup ou ao feedback.
- **Adequação do momento:** existem relatos pontuais, mas o conjunto de dados apresentado não inclui a série completa de respostas à pergunta correspondente do questionário.

H1 e H2 são as hipóteses comparativas principais. Conclusão da tarefa, esforço, interrupção e adequação do momento são variáveis secundárias previstas para caracterizar benefícios e custos da intervenção; nesta etapa, sua observação foi incompleta. H2 compara somente comentários de quem respondeu ao formulário. Essa seleção pode diferir entre os grupos e produzir viés; um estudo futuro deverá relatar a ausência de respostas e a composição dos respondentes, sem generalizar os escores para todos os participantes.

Tempo e cliques são medidas auxiliares. A tarefa no Figma foi instrumentada pelo Useberry, enquanto as regras da API constituem outra fonte de evidência, relativa à implementação. O planejamento de instrumentos e critérios comparativos deve preceder nova coleta.

Para a inspeção interna do artefato foram organizados sete critérios, retomados pelos mesmos identificadores na Tabela [10](#tab:criterios-avaliacao-preliminar):

1. **C1 — Registro mínimo de navegação:** existência de sessão técnica e estruturas para registrar eventos, com explicitação dos limites de captura do cliente de demonstração.
2. **C2 — Acionamento contextual:** correspondência entre parâmetros por serviço e ações previstas no código, sem interpretar acionamento como dificuldade confirmada.
3. **C3 — Esforço de resposta:** presença de formulário curto como decisão de projeto; esforço efetivamente percebido deve ser tratado como não medido nesta coleta.
4. **C4 — Apresentação para gestão:** existência de agregações e alertas; utilidade e acionabilidade dependem de avaliação com gestores.
5. **C5 — Inspeção das regras:** regras localizáveis no código e parâmetros por serviço; histórico de configuração e versionamento permanecem ausentes.
6. **C6 — Privacidade:** exame dos campos e das limitações de transparência, retenção e acesso, sem concluir conformidade jurídica.
7. **C7 — Interrupção:** possibilidade de ignorar o convite e limitar o popup; efeito sobre abandono ou irritação depende de mensuração posterior.

A apresentação dos resultados como exploratórios é uma regra de interpretação comum a todos os critérios, sem afirmação de superioridade ou generalização.

## 3.6 Procedimentos da Avaliação Exploratória

O relato do trabalho distingue três procedimentos. O primeiro é a inspeção funcional interna da implementação, com observação do registro de eventos, regras e indicadores descritos pelos autores, sem relatório de execução de testes anexado. O segundo é uma **avaliação heurística interna/preliminar**, também dos autores. O terceiro é a avaliação de fluxos de interface no Figma com oito participantes; os resultados desse procedimento não devem ser apresentados como verificação da API.

A avaliação exploratória de interface ocorreu em 28 de junho de 2026, com oito participantes externos ao grupo de desenvolvimento, quatro em cada fluxo. A alocação entre os grupos foi auxiliada por inteligência artificial e descrita como sorteio, sem registro auditável do mecanismo. Não se assume aleatorização verificável. O Figma foi instrumentado pelo Useberry para registro automático de cliques e tempos. O fluxo A previa formulário final e o B convite contextual; o popup de redirecionamento fez parte de ambos. A tarefa consistiu em localizar e iniciar a declaração do Imposto sobre a Renda da Pessoa Física (IRPF) de 2026, com limite de dez minutos. As sessões foram individuais e moderadas, sob coordenação de Julio Cesar Gomes de Souza Crispim e Fernando Gabriel dos Santos Carrijo, com TCLE que mencionava o Useberry e o registro de interações. A gravação se limitou à tela e aos eventos de interação, sem áudio ou vídeo de câmera dos participantes. Os comentários apresentados no Apêndice G provêm do questionário pós-sessão. O convite no fluxo B podia decorrer de tempo, entrada em tela ou clique no Figma. No fluxo A, resposta significa realizar a avaliação no formulário final; no B, aceitar o convite e realizar a avaliação sobre a experiência, não apenas abrir o convite. Os valores temporais, as telas e as interações específicas não estão discriminados neste protocolo. Esse procedimento permite observação formativa de interface, sem estabelecer funcionamento dos gatilhos do backend ou efeitos causais entre fluxos.

## 3.7 Tratamento dos Dados

A implementação organiza dois grupos de dados: eventos de interação, com contexto de sessão, página, serviço, clique e duração informada; e respostas declaradas, com estrelas, atributos, pergunta auxiliar de recomendação e comentário opcional. Eventos indicam contexto e possível esforço, sem medir qualidade percebida. Estrelas e atributos expressam julgamentos declarados; a pergunta NPS não foi validada como medida de qualidade percebida neste cenário. A base do estudo de interface é distinta: cliques e tempos registrados no Useberry, classificações de tarefa e respostas ao questionário pós-sessão, transcritos no Apêndice G. Não foi apresentado um conjunto separado de respostas do formulário que permita comparar seus comentários, estrelas e atributos.

A implementação oferece consulta de alertas, cliques e identificadores de sessão por serviço, total de feedbacks e médias de respostas. Não oferece contagem de sessões únicas alertadas, recorrência de atributos ou análise A/B. O formulário não solicita nome, CPF, e-mail ou credencial de login. O backend aceita um `user_id` opcional e registra URL e coordenadas do clique na tela, não geolocalização. Essas condições não comprovam anonimização. Aviso de coleta, retenção e controle de acesso exigem requisitos próprios ([Brasil, 2018](#ref-brasil2018lgpd)).

# 4 Desenvolvimento da Solução

Este capítulo apresenta o desenvolvimento do sistema de avaliação contextual a partir dos artefatos da Lean Inception e da implementação do protótipo. O desenvolvimento foi orientado pela hipótese de que o feedback contextual, acionado próximo a um sinal de possível dificuldade, pode ampliar a participação e produzir evidências declaradas mais específicas do que uma avaliação estática exibida apenas ao final da jornada. A avaliação exploratória desta etapa não é suficiente para confirmar essa hipótese.

## 4.1 Visão Geral do Produto

O sistema de avaliação contextual foi definido como uma solução de feedback contextual para serviços públicos digitais. A solução registra eventos de navegação permitidos, identifica sinais de possível dificuldade, solicita feedback por meio de um formulário curto e apresenta indicadores agregados para apoio à decisão do gestor.

A visão do produto foi usada como norte da solução: ela precisava deixar claro para quem o avaliador é construído, qual problema de navegação e avaliação ele enfrenta e de que forma o feedback contextual se diferencia de formulários estáticos exibidos apenas ao final da jornada.

A Figura [1](#fig:visao-produto-lean-inception) registra a síntese visual dessa visão na Lean Inception, antes da delimitação negativa e operacional do escopo.

As Figuras 1 a 4 foram produzidas por Fernando Gabriel dos Santos Carrijo e registram a concepção do projeto. Sua terminologia e suas metas expressam o planejamento daquela etapa. As capacidades efetivamente implementadas são discriminadas nas seções 3.4 e 4.7 a 4.12.

<a id="fig:visao-produto-lean-inception"></a>

![Figura 1 — Visão do produto construída na Lean Inception](../latex/figuras/apendices/lean-inception-visao-produto.png)

**Figura 1 — Visão do produto construída na Lean Inception.**

Fonte: elaboração de Fernando Gabriel dos Santos Carrijo (2026). A imagem registra decisões e metas de concepção, não resultados de avaliação.


A dinâmica É / Não É / Faz / Não Faz delimitou o escopo inicial. O produto é uma implementação local demonstrativa, com integração a portais reais prevista como evolução. Também é um apoio à melhoria de serviços digitais e à decisão administrativa. Não é um substituto de ouvidoria, não é chatbot, não solicita nome ou CPF na interface e não representa uma implantação governamental completa. O registro visual dessa definição de escopo aparece nas Figuras [2](#fig:e-nao-e-faz-nao-faz-1) e [3](#fig:e-nao-e-faz-nao-faz-2).

Na implementação Python, o sistema registra cliques instrumentados, recebe duração informada à API, aplica regras e disponibiliza um formulário com estrelas, atributos, pergunta auxiliar de recomendação e comentário opcional. A duração é demonstrada por envio simulado, sem cronômetro automático no cliente. O formulário não solicita identificação civil ou credenciais de login, mas o backend admite identificador opcional de usuário e dados de evento. Não há garantia de anonimização, resolução automática do problema do serviço ou integração governamental real.

<a id="fig:e-nao-e-faz-nao-faz-1"></a>

![Figura 2 — Dinâmica É / Não É / Faz / Não Faz da Lean Inception, parte inicial](../latex/figuras/apendices/lean-inception-e-nao-e-faz-nao-faz-1.png)

**Figura 2 — Dinâmica É / Não É / Faz / Não Faz da Lean Inception, parte inicial.**

Fonte: elaboração de Fernando Gabriel dos Santos Carrijo (2026). A imagem registra decisões e metas de concepção, não resultados de avaliação.


<a id="fig:e-nao-e-faz-nao-faz-2"></a>

![Figura 3 — Dinâmica É / Não É / Faz / Não Faz da Lean Inception, continuação](../latex/figuras/apendices/lean-inception-e-nao-e-faz-nao-faz-2.png)

**Figura 3 — Dinâmica É / Não É / Faz / Não Faz da Lean Inception, continuação.**

Fonte: elaboração de Fernando Gabriel dos Santos Carrijo (2026). A imagem registra decisões e metas de concepção, não resultados de avaliação.


## 4.2 Objetivos do Produto

A dinâmica de objetivos do produto separou o que o MVP precisava provar daquilo que seria apenas evolução futura. Os objetivos levantados foram: capturar sinais de possível dificuldade durante a navegação, solicitar feedback no momento adequado, reduzir o esforço de resposta, gerar dados agregados e acionáveis, coletar dados comparáveis entre fluxo contextual e fluxo estático, preservar privacidade e validar o MVP em protótipo controlado.

Foram priorizados três objetivos essenciais. O primeiro é capturar sinais de possível dificuldade, pois sem eventos de navegação não há como identificar o momento adequado para solicitar feedback. O segundo é solicitar feedback contextual, pois essa é a diferença principal em relação a formulários tradicionais. O terceiro é coletar dados comparáveis, porque a hipótese do MVP depende da comparação entre um fluxo estático e um fluxo contextual.

## 4.3 Personas

As personas representam os usuários e beneficiários da solução. Elas não são os participantes da Lean Inception; são arquétipos usados para orientar decisões de produto.

A primeira persona é Carlos Pereira, cidadão usuário de serviço público digital. Carlos acessa portais públicos para emitir documentos, consultar solicitações ou encontrar orientações. Ele tem pressa, muitas vezes acessa pelo celular e espera concluir a tarefa sem entender a estrutura interna do órgão. Suas dores incluem menus confusos, linguagem institucional, páginas parecidas, excesso de etapas e avaliações exibidas tarde demais. Seus comportamentos observáveis são cliques repetidos, permanência acima do esperado, retorno de página, abandono e baixa disposição para responder pesquisas longas.

A segunda persona é Lucas Almeida, gestor público de serviço digital. Lucas precisa acompanhar a qualidade de serviços digitais e priorizar melhorias. Sua dificuldade está em transformar notas genéricas, reclamações isoladas e dados técnicos em decisões objetivas. Para ele, o produto só gera valor se apontar onde o cidadão está travando e quais atributos do serviço devem ser priorizados.

A equipe técnica e de UX foi reconhecida como persona secundária de evolução. Ela seria importante em um piloto real, especialmente para configurar regras, acompanhar integrações e interpretar dados técnicos, mas não é essencial para validar o MVP em ambiente de protótipo.

## 4.4 Jornadas

A jornada principal descreve Carlos tentando usar um serviço público digital. Ele acessa um portal público, procura um serviço, encontra termos confusos, clica repetidamente, permanece tempo acima do esperado, tem os sinais registrados pelo avaliador, recebe feedback contextual e pode responder ou ignorar a avaliação. Em seguida, os dados são enviados ao painel para que a persona gestora investigue um possível ponto de atrito.

O ponto crítico ocorre entre a dificuldade observada e o abandono da jornada. É nesse intervalo que o feedback contextual se diferencia de uma avaliação estática. A proposta é perguntar quando a experiência ainda está recente, sem exigir um formulário longo e sem pressupor que um sinal comportamental comprove dificuldade.

Foram definidos dois fluxos comparáveis. No fluxo A, o cidadão navega, enfrenta dúvidas e recebe um formulário apenas ao final da jornada. No fluxo B, o cidadão clica ou demora além do esperado, o sistema registra o sinal e solicita feedback contextual. A comparação futura seguirá H1 e H2 da seção 3.5. A apresentação de alertas no painel é uma capacidade de implementação distinta do teste dessas hipóteses.

## 4.5 Funcionalidades Priorizadas

O brainstorming de features agrupou as funcionalidades em cinco categorias: coleta de sinais, regras e detecção, feedback, painel e integração. A revisão técnica, de negócio e UX classificou cada funcionalidade por esforço, valor para gestão, impacto na experiência do usuário e confiança.

A Figura [4](#fig:features-mvp-lean-inception) mostra como as features foram organizadas antes da seleção do MVP, separando capacidades essenciais de itens de evolução futura.

<a id="fig:features-mvp-lean-inception"></a>

![Figura 4 — Features categorizadas e essenciais para o MVP](../latex/figuras/apendices/lean-inception-features-mvp.png)

**Figura 4 — Features categorizadas e essenciais para o MVP.**

Fonte: elaboração de Fernando Gabriel dos Santos Carrijo (2026). A imagem registra decisões e metas de concepção, não resultados de avaliação.


As funcionalidades essenciais definidas para o MVP foram implementadas com os seguintes limites:

- sessão com identificador técnico, para agrupar eventos por identificador técnico, sem solicitação direta de nome ou CPF;

- registro de cliques instrumentados e recepção de duração simulada na API; medição automática de tempo e cliques apenas no estudo de interface Figma/Useberry;

- detecção por regra simples, para definir quando o sistema deve atuar;

- feedback contextual, para diferenciar o MVP do formulário estático;

- desenho de formulário final comparativo no Figma; instrumentação A/B na aplicação funcional permanece pendente;

- painel básico, para explorar a apresentação dos dados ao gestor;

- taxa de resposta dos fluxos, para preparar a mensuração futura de H1, com denominadores definidos previamente.

Funcionalidades como inteligência artificial para resumir comentários, integração com portal real, autenticação avançada, separação multi-organização completa e calibração estatística refinada foram deixadas fora do MVP inicial. Essas funcionalidades ampliam o escopo técnico e dependem de dados reais, autorização institucional ou governança de produção.

## 4.6 Sequenciamento e Canvas MVP

O sequenciador definiu as ondas 1 a 3 como escopo do MVP. A implementação foi parcial, conforme a seção 3.4: API e interfaces no Figma materializam partes distintas do desenho. As regras por serviço já estão implementadas, embora tenham sido inicialmente associadas à onda 4; ranking, indicadores A/B, filtros e comentários recentes não estão disponíveis no painel. A preparação para piloto real permanece futura.

O Canvas MVP consolidou o planejamento de uma solução contextual com identificadores técnicos, formulário curto e indicadores administrativos. O resultado alcançado foi uma implementação local parcial e um estudo exploratório das interfaces no Figma. A execução integrada do MVP planejado e seus benefícios comparativos continuam sujeitos a desenvolvimento e avaliação.

## 4.7 Arquitetura do Protótipo

O protótipo foi implementado como uma aplicação local em Python, com servidor HTTP, banco SQLite e páginas HTML geradas pelo próprio backend. A escolha por uma estrutura simples reduz dependências externas e facilita a demonstração do fluxo completo durante o TCC.

A arquitetura possui quatro camadas principais. A primeira é a camada de interface, composta por uma página inicial de portal público de demonstração, páginas de serviço, popup de redirecionamento, formulário de feedback e painel visual. A segunda é o script cliente de demonstração, que inicia sessão e envia cliques dos elementos marcados para rastreamento. Na implementação Python, o envio de duração ocorre por um controle de simulação que informa 120 segundos; não há cronômetro automático de navegação nesse cliente. A existência do endpoint temporal não comprova captura automática de tempo na aplicação Python. A terceira é a API, responsável por receber eventos, aplicar regras e devolver ações. A quarta é a camada de dados, armazenada em SQLite.

A Figura [5](#fig:prototipo-portal) mostra a página de portal público usada no protótipo, incluindo a área lateral que evidencia a comunicação com a API durante a navegação.

<a id="fig:prototipo-portal"></a>

![Figura 5 — Página de portal público usada no protótipo](../latex/figuras/apendices/prototipo-portal.png)

**Figura 5 — Página de portal público usada no protótipo.**

Fonte: captura produzida por Fernando Gabriel dos Santos Carrijo a partir da implementação Python (2026).


## 4.8 API e Endpoints

A API disponibiliza endpoints para saúde do serviço, listagem de serviços, registro de eventos, envio de feedback e consulta administrativa. A Tabela [3](#tab:endpoints-prototipo) resume os principais endpoints.

<a id="tab:endpoints-prototipo"></a>

**Tabela 3 — Endpoints principais do protótipo**

| **Endpoint** | **Finalidade** |
|:---|:---|
| `GET /health` | Verificar disponibilidade da API. |
| `GET /api/services` | Listar serviços cadastrados e suas regras. |
| `POST /api/events/click` | Registrar clique, página, serviço, origem e instante. |
| `POST /api/events/page-time` | Receber e armazenar duração informada; demonstração com valor simulado, sem cronômetro automático no cliente. |
| `GET /feedback` | Exibir página simples de feedback para uma sessão. |
| `POST /api/feedback` | Salvar estrelas, atributos, NPS e comentário. |
| `GET /api/admin/alerts` | Consultar alertas administrativos de possível dificuldade. |
| `GET /api/admin/dashboard` | Consultar dados agregados para o painel. |

Fonte: elaboração dos autores com base nos endpoints da implementação Python (2026).

## 4.9 Regras de Detecção de Possível Dificuldade

A detecção de possível dificuldade foi implementada com regras explícitas no backend. A API mantém, para cada serviço, um limite de cliques e um tempo médio esperado. Um alerta por clique é criado quando a contagem de cliques da mesma sessão, no mesmo serviço, fica **maior** que o limite configurado. Um alerta por duração informada é criado quando esse valor fica **maior** que 1,5 vez o tempo esperado do serviço.

O identificador técnico é persistido no navegador; o backend também admite `user_id`, URL e coordenadas do clique na tela (`x` e `y` em pixels), não coordenadas geográficas. Não solicitar nome ou CPF não torna os dados automaticamente anônimos. A implementação não demonstrou anonimização irreversível ou ausência de possibilidade de associação entre registros.

O backend armazena a marcação administrativa com o campo `silent` ativo. Essa gravação interna não equivale à exibição de um aviso específico ao usuário; o convite de feedback é uma ação distinta. A ausência de aviso a cada marcação não supre a necessidade de transparência sobre a coleta. O protótipo não foi apresentado como solução com aviso de coleta, retenção e controle de acesso plenamente implementados.

Essas regras operacionalizam o conceito de feedback contextual discutido na Seção [2.9](#sec:feedback-contextual): o sistema não pergunta aleatoriamente, mas usa sinais de uso para decidir quando solicitar uma manifestação do usuário. O acionamento não confirma que houve dificuldade nem mede qualidade percebida; ele apenas seleciona um contexto para coleta do feedback declarado.

A lógica aproxima-se da coleta contingente a eventos discutida na literatura de Experience Sampling Method (ESM), com uma adaptação ao contexto de software. A literatura de ESM descreve procedimentos de coleta de autorrelatos no cotidiano ([Larson; Csikszentmihalyi, 1983](#ref-larson1983experienceSampling); [Hektner et al., 2007](#ref-hektner2007experienceSampling)). A Tabela [4](#tab:formas-coleta-situada) organiza formas de acionamento para discutir o desenho do MVP; não representa uma classificação validada por este estudo. Neste protótipo, cliques acima do limite, tempo acima da faixa esperada e persistência após redirecionamento funcionam como sinais comportamentais de possível dificuldade. Eles não são equivalentes a uma confirmação de dificuldade e não expressam qualidade percebida; indicam apenas um momento plausível para solicitar feedback declarado. Por isso, o convite deve ser opcional, curto e não bloqueante.

A Tabela [4](#tab:formas-coleta-situada) explicita essa adaptação metodológica.

<a id="tab:formas-coleta-situada"></a>

**Tabela 4 — Formas de coleta situada e relação com o protótipo**

| **Forma de coleta situada** | **Funcionamento geral** | **Relação com o protótipo** | **Limitação** |
|:---|:---|:---|:---|
| Amostragem temporal | O participante responde em horários ou intervalos definidos. | Não foi adotada, pois a jornada do serviço não depende de horários fixos. | Poderia acionar perguntas fora do momento de dificuldade. |
| Amostragem aleatória | O participante é solicitado em momentos sorteados durante a observação. | Não foi adotada no MVP, pois poderia interromper usuários sem sinal de atrito. | Reduz viés de seleção, mas aumenta o risco de interrupção sem contexto. |
| Amostragem orientada a evento | A coleta ocorre quando um evento previamente definido acontece. | É a lógica mais próxima do MVP: cliques, tempo e persistência funcionam como eventos operacionais. | O evento técnico pode não corresponder a dificuldade real. |
| Acionamento por proxy comportamental | O sistema usa indícios observáveis como substitutos de um evento subjetivo. | Foi adotado para tornar o feedback contextual demonstrável sem inferência complexa. | Exige calibração futura e análise de falsos positivos. |


Fonte: elaborada pelos autores (2026).

Os limiares usados no protótipo foram definidos como parâmetros operacionais de demonstração, e não por calibração estatística com dados de produção. A escolha permite que o MVP exiba três estados do fluxo: navegação sem alerta, alerta administrativo de possível dificuldade e convite de feedback contextual. Em uma implantação real, esses parâmetros deveriam ser calibrados por serviço, página, perfil de tarefa e histórico de uso.

No backend Python, o parâmetro `click_threshold` é 12 para a página inicial e o serviço genérico, e 10 para Imposto de Renda. A condição é estrita: a regra aciona quando a contagem é maior que esse parâmetro, portanto no 13º e no 11º clique, respectivamente. Nos contextos com redirecionamento, o convite de feedback por clique ocorre a partir de `click_threshold + 2`: 14º clique na página inicial e 12º em Imposto de Renda. Esses valores se referem à contagem por sessão e serviço no backend, não ao total de cliques de uma tarefa no Figma. A duração informada é comparada com 1,5 vez o tempo esperado: acima de 90 segundos para os serviços com parâmetro 60 e acima de 67,5 segundos para Imposto de Renda, com parâmetro 45. O cliente Python demonstra essa regra com envio manual de duração simulada. Os tempos totais do Useberry não permitem deduzir se uma regra da API teria sido acionada.

Portanto, o primeiro acionamento no 13º clique corresponde ao parâmetro armazenado 12, não a um parâmetro 13. São valores operacionais de demonstração, sem calibração empírica. A Tabela [5](#tab:sensibilidade-limiares) apresenta uma análise qualitativa dos efeitos esperados de alterar os parâmetros.

<a id="tab:sensibilidade-limiares"></a>

**Tabela 5 — Análise qualitativa de sensibilidade dos limiares**

| **Parâmetro** | **Valor menor** | **Efeito provável** | **Valor maior** | **Efeito provável** |
|:---|:---|:---|:---|:---|
| Cliques | 10 cliques | Maior sensibilidade, mais alertas e maior risco de falso positivo. | 15 a 20 cliques | Menos alertas e maior risco de perder dificuldades reais. |
| Tempo | 1,2 vez o tempo esperado | Acionamento mais rápido, com possível interrupção de leitura normal. | 2,0 vezes o tempo esperado | Acionamento mais conservador, com possível atraso na coleta contextual. |
| Persistência após redirecionamento | Acionamento imediato | Maior chance de interromper cedo demais. | Acionamento após nova evidência | Menor interrupção, mas maior demora para coletar o relato. |


Fonte: elaborada pelos autores (2026).

A Tabela 5 é uma análise de projeto elaborada pelos autores, distinta das sessões empíricas com participantes. Ela organiza efeitos esperados e riscos dos parâmetros; não mede taxas reais de acionamento nem calibra limiares para produção.

### 4.9.1 Simulação Sintética dos Limiares

Foi registrada uma análise sintética com 1.000 sessões de cliques e durações log-normais, medianas de 7 cliques e 60 segundos e cenários identificados por 10, 13 e 18 cliques. Os arquivos de execução e resultados intermediários não estão disponíveis. O valor da semente e os parâmetros de dispersão não foram preservados no relato. A Tabela 6 apresenta a síntese numérica dessa etapa, sem possibilidade de reprodução a partir dos materiais disponíveis.

O resultado sintético não valida um limiar de dificuldade e não corresponde à observação dos oito participantes. Sem o script, os dados gerados e todos os parâmetros, sua reprodutibilidade não pode ser afirmada. A confirmação ou substituição desse ensaio depende de execução futura documentada, apresentada como nova análise e sem atribuí-la à coleta anterior.

<a id="tab:simulacao-sintetica-limiares"></a>

**Tabela 6 — Simulação sintética de sensibilidade dos limiares de clique**

| **Limiar** | **Tempo**  | **Por clique** | **Por tempo** | **Total acionado** |
|:-----------|:-----------|:---------------|:--------------|:-------------------|
| 10 cliques | > 90 s | 28,3%          | 25,9%         | 42,9% (429/1000)   |
| 13 cliques | > 90 s | 13,7%          | 25,9%         | 32,8% (328/1000)   |
| 18 cliques | > 90 s | 5,1%           | 25,9%         | 27,3% (273/1000)   |


Fonte: registros de síntese da análise sintética do projeto (2026). Os arquivos de execução não estão disponíveis para reprodução.

Na síntese numérica, o cenário denominado 13 cliques tem taxa intermediária de acionamento. Não foi preservada a definição do comparador aplicado à contagem: não se sabe se os rótulos significavam `> 13`, `≥ 13` ou primeiro acionamento associado ao parâmetro 12. Portanto, essa linha não pode ser equiparada ao `click_threshold` da implementação, nem fundamenta a escolha de um limite de dificuldade.

No protótipo atual, as regras são as seguintes:

<a id="tab:regras-dificuldade"></a>

**Tabela 7 — Regras operacionais de acionamento por possível dificuldade no protótipo**

| **Serviço** | **Cliques** | **Tempo** | **Ação principal** |
|:---|:---|:---|:---|
| Página inicial do governo | parâmetro 12; alerta e sugestão no 13º; convite no 14º clique | duração informada maior que 90 segundos | sugere Imposto de Renda; persistência do sinal pode gerar convite |
| Imposto de Renda | parâmetro 10; alerta e sugestão no 11º; convite no 12º clique | duração informada maior que 67,5 segundos | retorna sugestão de redirecionamento e pode gerar convite |
| Serviço público genérico | parâmetro 12; alerta e convite no 13º clique | duração informada maior que 90 segundos | gera convite sem sugestão prioritária |


Fonte: elaboração dos autores com base nas regras implementadas no backend Python (2026).

A página inicial do governo é tratada como contexto capaz de recomendar um serviço prioritário. O serviço de Imposto de Renda foi marcado como importante e de alto tráfego. O serviço genérico representa uma situação comum, na qual a API registra o acionamento da regra e pode gerar um convite sem sugerir redirecionamento. Em todos os casos, o alerta administrativo registra somente que uma regra operacional foi acionada. O gestor visualiza o evento como indício para investigação, e não como diagnóstico automático de dificuldade ou de baixa qualidade percebida.


## 4.10 Fluxos Implementados

O fluxo de clique começa quando o usuário acessa uma página simulada. O script cliente cria ou recupera uma sessão com identificador técnico, captura o evento e envia os dados para a API. A API registra o clique, atualiza a contagem por serviço, verifica o limite configurado e decide se deve retornar fluxo normal, popup de redirecionamento ou convite de feedback.

Quando o serviço é prioritário, a API pode retornar uma ação de popup sugerindo redirecionamento para o serviço correto. Esse popup é exibido apenas uma vez por sessão, serviço e motivo, evitando repetição excessiva. Quando o sinal persiste ou quando a duração informada ultrapassa a faixa esperada, a API pode retornar uma ação para disponibilizar o convite de feedback.

O fluxo de feedback coleta avaliação por estrelas, características do problema, NPS e comentário opcional. As características previstas incluem clareza, tempo, esforço, usabilidade, atendimento e eficácia. O objetivo é transformar uma nota geral em dados explicativos para o gestor.

A escolha desses atributos buscou decompor a avaliação geral em dimensões acionáveis. Clareza relaciona-se à compreensão da informação; tempo, à demora percebida; esforço, à quantidade de passos e decisões; usabilidade, à interação e navegação; atendimento, ao suporte complementar; e eficácia, à percepção de alcance do resultado pretendido. Essas categorias não constituem um modelo definitivo e devem ser confrontadas com a linguagem de cidadãos e com a taxonomia oficial. A Tabela [8](#tab:atributos-feedback) explicita a relação.

<a id="tab:atributos-feedback"></a>

**Tabela 8 — Atributos do feedback e relação com dimensões de qualidade**

| **Atributo no protótipo** | **Relação com atributos oficiais ou literatura** | **Justificativa no MVP** | **Limitação** |
|:---|:---|:---|:---|
| Clareza | Clareza das informações e correspondência entre linguagem do sistema e do usuário. | Identifica problemas de compreensão, instrução ou linguagem institucional. | Não separa linguagem, orientação e organização visual. |
| Tempo | Tempo para obtenção do serviço e percepção de demora. | Associa permanência excessiva ou espera percebida a uma avaliação declarada. | Não distingue lentidão técnica, leitura cuidadosa ou complexidade legítima. |
| Esforço | Aproxima-se do CES e do custo/esforço para obtenção do serviço. | Indica se a jornada exigiu muitos passos ou decisões difíceis. | Pode se sobrepor a usabilidade e tempo. |
| Usabilidade | Facilidade de uso, prevenção de erros e navegação. | Captura problemas de interação, fluxo e compreensão operacional da interface. | É uma categoria ampla e exige comentário para diagnóstico mais preciso. |
| Atendimento | Qualidade dos canais de comunicação e suporte. | Mantém espaço para experiências em que o canal digital depende de orientação complementar. | Pode ser pouco aplicável a serviços totalmente automatizados. |
| Eficácia | Efetividade e resolução da necessidade do cidadão. | Indica se o serviço ajudou o usuário a atingir o resultado esperado. | Não comprova a conclusão real da tarefa sem integração com sistemas de produção. |


Fonte: elaborada pelos autores com base nos atributos do protótipo e em [Silva (2024)](#ref-silva2024atributosApi).

A pergunta de recomendação identificada como NPS foi mantida como item auxiliar do formulário, sem validação de sua interpretação no serviço público e sem cálculo do escore no painel. Também foram considerados riscos de falso positivo: permanência longa pode representar leitura cuidadosa, tarefa complexa, conexão lenta, tecnologia assistiva ou interrupção externa, e não necessariamente dificuldade. Os alertas, portanto, são indícios comportamentais para investigação; a interpretação da qualidade percebida depende do feedback declarado.

O popup de redirecionamento segue a mesma cautela. Ele pode ajudar quando o usuário parece estar no serviço incorreto, mas também pode interromper a navegação e aumentar o abandono. No MVP, o risco foi mitigado por exibição limitada e pela possibilidade de continuar a tarefa. A Tabela [9](#tab:decisoes-design) registra benefícios, riscos e formas de mitigação das principais decisões.

<a id="tab:decisoes-design"></a>

**Tabela 9 — Decisões de design, benefícios, riscos e mitigações**

| **Decisão de design** | **Benefício esperado** | **Risco** | **Mitigação no MVP** | **Avaliação futura necessária** |
|:---|:---|:---|:---|:---|
| Popup de redirecionamento | Ajudar o usuário a encontrar o serviço correto antes de registrar reclamação. | Interromper a navegação, irritar ou aumentar o abandono. | Exibição limitada, sem bloqueio definitivo da navegação. | Medir abandono, aceitação do redirecionamento e percepção de intrusão. |
| Feedback contextual | Coletar relato próximo ao ponto de dificuldade. | Aumentar carga cognitiva durante uma tarefa já difícil. | Formulário curto, campos opcionais e poucos atributos. | Medir taxa de resposta, abandono e qualidade dos comentários. |
| Atributos predefinidos | Transformar nota geral em categorias acionáveis. | Reduzir problemas complexos a opções simplificadas. | Comentário opcional para complementar a categoria. | Comparar com taxonomia oficial e ajustar nomes. |
| Pergunta auxiliar de recomendação, identificada como NPS | Registrar uma resposta declarada de recomendação. | Atribuir qualidade percebida ou lealdade a uma resposta sem validação no contexto público. | Manter sua interpretação separada de estrelas e atributos; o painel calcula apenas média de 0 a 10. | Reavaliar o item em função do objetivo e do contexto de uso. |


Fonte: elaborada pelos autores (2026).

A Figura [6](#fig:prototipo-feedback) apresenta a tela de feedback contextual, com avaliação por estrelas, atributos do problema, NPS e comentário opcional.

<a id="fig:prototipo-feedback"></a>

![Figura 6 — Formulário de feedback contextual do protótipo](../latex/figuras/apendices/prototipo-feedback.png)

**Figura 6 — Formulário de feedback contextual do protótipo.**

Fonte: captura produzida por Fernando Gabriel dos Santos Carrijo a partir da implementação Python (2026).


## 4.11 Painel Administrativo e Indicadores

A implementação do painel exibe JSON com total de alertas, cliques e identificadores de sessão distintos por serviço, total de feedbacks e médias de estrelas e da pergunta auxiliar de recomendação. O campo denominado `average_nps` contém a média aritmética das respostas de 0 a 10, não o escore NPS. O contador visual de sessões soma os identificadores distintos de cada serviço; pode contar o mesmo identificador em mais de um serviço e não representa sessões únicas ou sessões com alertas. Não estão implementados frequência de atributos, comentários recentes, taxa de resposta por fluxo ou ranking de serviços por alerta. Essas agregações pertencem à evolução do painel. Os registros disponíveis apontam situações para investigação; excesso de cliques não comprova gargalo e utilidade gerencial não foi avaliada.

O painel organiza registros técnicos e médias de respostas, sem substituir instrumentos oficiais. Cliques e duração informada à API são dados comportamentais, não medidas de qualidade percebida. Estrelas, atributos e comentários são declarações sobre a experiência; a pergunta auxiliar de recomendação tem interpretação própria e não validada neste contexto. A implementação não calcula o escore NPS nem demonstra integração dos dados do estudo no Figma.

## 4.12 Resultado do Desenvolvimento

O desenvolvimento resultou em uma implementação local parcial das ondas 1 a 3. Na aplicação Python há captura de cliques instrumentados, recepção de duração simulada, regras, formulário e agregações básicas. A construção não entrega integralmente o fluxo de avaliação planejado: faltam, entre outros elementos, instrumentação A/B, registro de exposição ao convite e coleta automática de duração no cliente. O estudo com participantes examinou o componente de interface no Figma.

A implementação funcional e a avaliação de interface representam frentes distintas do trabalho. O desenho prevê formulário final no fluxo A e convite contextual no B. As sessões com oito participantes, descritas na seção [4.14](#sec:avaliacao-participantes), ocorreram no Figma/Useberry. Seus resultados não verificam integração com SQLite, funcionamento dos endpoints ou aderência dos convites às regras do código Python.

## 4.13 Avaliação Preliminar do Artefato

A análise interna do artefato distingue inspeção funcional e **avaliação heurística interna/preliminar** dos autores. A organização heurística tomou como referência [Nielsen (1994)](#ref-nielsen1994heuristic), sem equivaler a inspeção externa. O registro da inspeção não discrimina avaliadores, data ou severidade, e o trabalho não inclui relatório completo de execução dos testes. Os resultados abaixo devem ser lidos como apreciação interna da implementação e do desenho de interface.

A Tabela [10](#tab:criterios-avaliacao-preliminar) retoma os sete critérios C1–C7 da seção 3.5. Ela separa existência de implementação, julgamento interno e propriedades que não foram medidas.

<a id="tab:criterios-avaliacao-preliminar"></a>

**Tabela 10 — Critérios da avaliação preliminar do protótipo**

| **Critério** | **Situação da evidência** | **Base disponível** | **Limitação** |
|:---|:---|:---|:---|
| C1 — Registro mínimo de navegação | Implementado com limites de captura | Código de sessão, eventos e persistência | Cliques restritos a elementos marcados; duração demonstrada por envio simulado; sem relatório de testes anexado. |
| C2 — Acionamento contextual | Regras explícitas no código | Parâmetros por serviço e condições de acionamento | A sessão no Figma não verifica sua execução; sem calibração empírica. |
| C3 — Esforço de resposta | Não medido | Formulário curto como decisão de projeto | Não há medida CES, tempo de preenchimento ou análise sistemática de abandono neste estudo. |
| C4 — Apresentação para gestão | Agregações básicas implementadas; utilidade não avaliada | Total de alertas, cliques/sessões por serviço e médias de respostas | Sem agregação de atributos, taxa de resposta ou avaliação com gestores; o contador não identifica sessões únicas alertadas. |
| C5 — Inspeção das regras | Parcialmente atendido | Condições localizáveis no backend e parâmetros por serviço | Sem histórico de configuração ou versionamento formal de regras. |
| C6 — Privacidade | Requisitos completos não verificados | Interface sem solicitação de nome, CPF, e-mail ou login | Isso não comprova anonimização; backend admite identificador de usuário, URL e coordenadas do clique na tela (`x` e `y` em pixels), não coordenadas geográficas. Transparência, retenção e acesso ainda exigem requisitos. |
| C7 — Interrupção | Efeito não medido sistematicamente | Controles de recusa/fechamento e relatos pontuais | Sem taxa de intrusão ou efeito causal sobre abandono; popup presente nos dois fluxos. |


Fonte: elaborada pelos autores (2026).

A inspeção permite localizar os componentes que materializam o fluxo proposto. Não comprova benefício ao cidadão, baixo esforço, utilidade gerencial ou superioridade sobre formulários finais. A calibração, a transparência da coleta, o risco de falsos positivos e a avaliação externa permanecem limites da proposta.

<a id="tab:avaliacao-heuristica-preliminar"></a>

**Tabela 11 — Avaliação heurística interna/preliminar do protótipo**

| **Heurística observada** | **Evidência no protótipo** | **Avaliação preliminar** | **Ajuste recomendado** |
|:---|:---|:---|:---|
| Visibilidade do status do sistema | O painel lateral e o administrativo indicam eventos, alertas e respostas da API. | Parcialmente atendida | Exibir estados mais claros de carregamento, erro e feedback enviado. |
| Correspondência com a linguagem do usuário | O formulário usa termos simples para informações confusas, demora e excesso de passos. | Parcialmente atendida | Testar os rótulos com cidadãos para evitar termos ambíguos. |
| Controle e liberdade do usuário | O feedback é opcional e o popup não deve bloquear definitivamente a navegação. | Parcialmente atendida | Garantir ação evidente para ignorar, fechar e continuar o fluxo. |
| Prevenção de erros | O popup pode orientar o usuário que parece estar no serviço incorreto. | Parcialmente atendida | Evitar redirecionamento automático e registrar se a sugestão foi aceita ou recusada. |
| Reconhecimento em vez de memorização | Estrelas e atributos predefinidos reduzem a necessidade de relato longo. | Atendida | Manter comentário opcional para problemas não previstos. |
| Eficiência e baixo esforço | O formulário é curto e estruturado. | Parcialmente atendida | Medir tempo de preenchimento e abandono em teste ampliado. |
| Diagnóstico e recuperação | A lista de alertas indica serviço e tipo de sinal; recorrência não é agregada no painel. | Parcialmente atendida | Relacionar alertas a recomendações de melhoria ou prioridade de investigação. |
| Ajuda e orientação | O protótipo demonstra o fluxo, mas não oferece ajuda contextual robusta. | Não atendida plenamente | Incluir microtextos explicativos e orientação sobre a finalidade da coleta. |


Fonte: elaborada pelos autores (2026).

A leitura heurística interna/preliminar indicou que a interface apresenta o estado básico das ações, usa linguagem relativamente direta, mantém o feedback opcional e procura limitar a extensão do formulário por meio de atributos predefinidos. Como limitações, foram registrados a necessidade de estados mais claros de carregamento e erro, microtextos explicativos, maior evidência para ignorar ou fechar o convite e uma ligação mais explícita entre alertas e ações de melhoria. Esses achados são hipóteses de aprimoramento produzidas pelos autores, não parecer independente de especialistas.

<a id="sec:avaliacao-participantes"></a>

## 4.14 Avaliação Exploratória com Participantes

Em 28 de junho de 2026 foi conduzida uma avaliação exploratória de interface com oito participantes externos ao grupo de desenvolvimento. As tarefas foram realizadas no Figma, com registro automático de cliques e tempos pelo Useberry. A documentação do fornecedor caracteriza a integração para testes de protótipos; não constitui evidência independente dos dados desta coleta ([Useberry, s.d.](#ref-useberryFigma)). Quatro participantes realizaram o fluxo A, com formulário final, e quatro o B, com convite contextual. A alocação foi auxiliada por inteligência artificial e descrita como sorteio, sem registro auditável de seu mecanismo. O popup de redirecionamento fez parte de ambos os fluxos; não há registro individual de sua exibição ou aceitação. A tarefa consistia em localizar e iniciar a declaração do IRPF 2026, com limite de dez minutos. As sessões foram individuais e moderadas, sob coordenação de Julio Cesar Gomes de Souza Crispim e Fernando Gabriel dos Santos Carrijo, com TCLE que mencionava o Useberry e o registro de interações. A gravação se limitou à tela e aos eventos de interação, sem áudio ou vídeo de câmera dos participantes.

No fluxo A, a avaliação era apresentada ao final da jornada. No fluxo B, o convite podia ser acionado por tempo decorrido, entrada em uma tela ou interação de clique no Figma. Esses acionamentos pertencem ao protótipo de interface, sem execução das regras da API Python. A descrição do protocolo não discrimina os intervalos de tempo, as telas e os cliques configurados, nem identifica o gatilho específico de cada exposição registrada. Assim, os tipos de acionamento estão definidos, mas não se reconstrói a configuração exata de cada caso apenas com os dados apresentados.

No fluxo A, a classificação “respondeu ao feedback” corresponde à realização da avaliação no formulário final. No B, corresponde ao aceite do convite seguido da realização da avaliação na interface. O aceite isolado do convite no B não foi suficiente. Essas classificações não comprovam digitação de comentário ou envio a um backend. Os comentários literais apresentados no Apêndice G foram obtidos no questionário pós-sessão. As Figuras 5 e 6 mostram a implementação Python; não reproduzem as telas A e B efetivamente avaliadas no Figma.

Os participantes foram recrutados voluntariamente entre estudantes da FCTE e cidadãos em geral, incluindo profissionais das áreas administrativa, educação, empreendedorismo e finanças, além de pessoa aposentada. Em P05, houve um pedido de confirmação sobre a segurança do protótipo e a orientação verbal do moderador para agir como em casa. Essa intervenção deve ser considerada como possível influência sobre a experiência. Quando necessário, foi feita uma demonstração inicial em tela neutra para reduzir a interferência da ferramenta de prototipação, registrada em P07. O tamanho da amostra foi definido para observação qualitativa formativa, e não para inferência estatística ou estimação de efeito entre os fluxos.

Os resultados são apresentados de forma descritiva. Com quatro participantes por grupo e seleção não probabilística, os dados não sustentam conclusões comparativas robustas nem generalização dos achados. Os números constituem indícios iniciais para orientar iterações e planejar um estudo posterior, não evidência de superioridade do feedback contextual.

<a id="tab:resultados-preliminares-fluxos"></a>

**Tabela 12 — Resultados exploratórios por fluxo de avaliação**

| **Métrica** | **Fluxo A – formulário final** | **Fluxo B – feedback contextual** |
|:---|:---|:---|
| Participantes | 4 | 4 |
| Taxa de conclusão | 2/4 (50%) | 3/4 (75%) |
| Tempo médio observado, incluindo encerramentos no limite | 8min32s | 7min31s |
| Cliques médios | 20,25 | 19,00 |
| Convite contextual apareceu | N.A. | 3/4 |
| Realizou a avaliação / participantes | 2/4 (50%) | 2/4 (50%) |
| Resposta quando o convite apareceu | N.A. | 2/3 (67%) |
| Nota média de facilidade | 2,50/5 | 3,75/5 |
| Encontrou o que procurava | 2/4 (50%) | 3/4 (75%) |


Fonte: elaborada pelos autores com base na avaliação exploratória preliminar (2026).

O fluxo B apresentou maior proporção descritiva de conclusão completa e maior nota de facilidade, além de menor tempo médio observado. A exposição ao formulário final não está registrada por participante no fluxo A; por isso, 2/4 em cada grupo é a proporção de participantes que realizaram a avaliação segundo o critério de cada fluxo, não uma comparação condicionada à exposição. Entre os três participantes com convite registrado no B, dois responderam. As médias temporais incluem P06 e P07, encerrados no limite de dez minutos; não são médias de tempo de conclusão apenas entre tarefas completas. O caso Parcial de P03 foi contabilizado como não conclusão completa no resumo, sem que isso indique um critério prévio de sucesso documentado. A seleção, a alocação sem mecanismo auditável, o popup e as diferenças de familiaridade limitam qualquer interpretação comparativa ou causal.

Os comentários do Apêndice G são respostas ao questionário pós-sessão, inclusive de participantes que não realizaram a avaliação na interface. Não representam um corpus de comentários coletados pelo mecanismo contextual. Sem esse corpus e uma rubrica aplicada, não há base para concluir maior qualidade ou especificidade dos comentários do fluxo B. Os relatos permitem discutir impressões sobre a interface e o convite. A confusão entre consultar e declarar foi mencionada sobretudo por participantes do fluxo A, o que também impede atribuir a identificação desse problema ao mecanismo contextual. Os TCLEs foram arquivados separadamente; sua descrição consta no Apêndice E e o questionário no Apêndice F.

Quatro temas descritivos merecem registro: ambiguidade entre consultar e declarar, nos relatos de P01, P03 e P05; percepção de oportunidade do convite em P02 e P08; decisão de ignorá-lo em P06; e baixa familiaridade de P07 com GOV.BR e Figma. São observações pós-sessão e do moderador, não medidas de eficácia do feedback. Os convites no Figma podiam decorrer de tempo, tela ou clique; as medidas agregadas da Tabela 12 não identificam a configuração ou a sequência específica de eventos de cada caso. Os limiares da API não explicam os casos P04 e P06, pois pertencem a outro componente do artefato.

## 4.15 Síntese Crítica do Desenvolvimento

A contribuição investigativa desta etapa é formular hipóteses e organizar a distinção entre contexto comportamental e percepção declarada. A contribuição tecnológica é a implementação que permite associar essas fontes. A tabela de rastreabilidade dos construtos e os instrumentos comparativos ainda precisam ser concluídos; não se apresenta um modelo de mensuração validado. O estudo no Figma oferece observações formativas de interface e não verifica a execução do backend nem confirma H1 ou H2.

Permanecem como riscos centrais os falsos positivos dos gatilhos, a interrupção inoportuna, a simplificação de problemas complexos em atributos predefinidos e a ausência de avaliação externa por especialistas e gestores. Por isso, o sistema deve ser lido como artefato investigativo e protótipo tecnológico, não como produto pronto ou instrumento cientificamente calibrado.

## 4.16 Alternativas de Design Consideradas

Durante a definição do MVP, alternativas de design foram consideradas, mas não priorizadas na primeira versão. A Tabela [13](#tab:alternativas-design) torna explícitas essas decisões de escopo.

<a id="tab:alternativas-design"></a>

**Tabela 13 — Alternativas de design consideradas no MVP**

| **Decisão adotada no MVP** | **Alternativa considerada** | **Motivo para não adotar no MVP** | **Consequência da escolha atual** |
|:---|:---|:---|:---|
| Regras simples de clique e tempo | Modelo estatístico ou aprendizado de máquina para detectar dificuldade. | Exigiria base histórica, volume de dados e validação inexistentes nesta etapa. | Mantém rastreabilidade, mas reduz precisão. |
| Acionamento por limite de cliques e tempo | Análise de sequência de páginas, retorno a etapas ou padrões de navegação. | Aumentaria a complexidade de instrumentação e análise. | Facilita a demonstração, mas perde sinais mais ricos de desorientação. |
| Popup de redirecionamento | Banner discreto, mensagem inline ou recomendação no painel lateral. | O popup torna a intervenção mais visível na demonstração. | Aumenta o risco de interrupção e precisa de teste de aceitação. |
| Atributos predefinidos | Campo aberto obrigatório ou taxonomia oficial completa. | Campo obrigatório aumentaria o esforço; taxonomia extensa poderia reduzir a resposta. | Reduz esforço, mas simplifica problemas complexos. |
| Pergunta auxiliar de recomendação, identificada como NPS | CSAT ou CES como métrica principal. | A pergunta foi mantida na concepção inicial pela familiaridade de uso, sem validação de sua interpretação. | Não representa medida validada de qualidade percebida nem escore NPS calculado no painel. |
| Sessão com identificador técnico | Login, CPF ou integração com conta gov.br. | A identificação aumentaria o risco de privacidade e a dependência institucional. | Evita solicitação de identificação civil, mas não comprova anonimização. |
| Painel administrativo básico | Ferramenta completa de analytics ou exportação avançada. | Escopo incompatível com o MVP e com a ausência de implantação real. | Entrega visão inicial, mas não substitui sistema de gestão de melhoria. |


Fonte: elaborada pelos autores (2026).

Essas alternativas indicam caminhos de evolução do artefato. A análise de sequência de páginas e retorno a etapas anteriores pode melhorar a detecção sem depender apenas de cliques ou tempo. Uma intervenção menos intrusiva também pode reduzir abandono. Tais escolhas exigem avaliação externa e estudos com usuários para determinar se aumentam a utilidade do feedback contextual ou apenas acrescentam complexidade.

# 5 Considerações Finais

Este trabalho teve como objetivo conceber e desenvolver um protótipo inicial de avaliação contextual de serviços públicos digitais, capaz de registrar sinais de possível dificuldade na navegação, solicitar feedback de baixo esforço e apresentar indicadores agregados para apoiar a melhoria dos serviços avaliados. A proposta partiu de um problema prático: avaliações exibidas apenas ao final da jornada nem sempre capturam o contexto em que o usuário se perde, demora ou abandona a busca por um serviço.

A fundamentação distingue satisfação, qualidade percebida, efetividade e usabilidade. O desenho relaciona contexto comportamental e julgamento declarado, mas cada componente tem limites: a API recebe duração simulada, o estudo Figma/Useberry registra automaticamente tempo e cliques, e o questionário pós-sessão reúne impressões da interface. Estrelas e atributos não são substituídos por telemetria. A pergunta de recomendação mantida no formulário possui interpretação própria e não foi validada como qualidade percebida.

A Lean Inception contribuiu para transformar a ideia inicial em um MVP mais delimitado. As dinâmicas de escopo, objetivos, personas, jornadas, brainstorming, revisão técnica, sequenciamento e Canvas MVP permitiram separar o que deveria entrar na primeira versão do que deveria permanecer como evolução. Com isso, o trabalho evitou ampliar o escopo para ouvidoria, chatbot, identificação individual, autenticação avançada ou integração real com portais governamentais.

O protótipo funcional implementa registro de eventos, regras de acionamento, convite de feedback e agregações administrativas em ambiente local. Essa implementação constitui a contribuição tecnológica. A contribuição investigativa é a formulação de hipóteses sobre o momento da coleta e a distinção entre evidências comportamentais e declaradas. A avaliação no Figma examina o desenho da interface; não demonstra integração funcional nem valida um modelo de mensuração.

## 5.1 Resultados em Relação aos Objetivos

O primeiro objetivo específico foi levantar fundamentos legais, técnicos e teóricos sobre avaliação de serviços públicos, qualidade percebida, usabilidade, governo digital e Lean Inception. O referencial reúne parte dessa base, e a metodologia apresenta a aproximação à DSR. O referencial ainda requer ampliação com modelos de qualidade de serviços eletrônicos, além de aprofundamento das fontes e de sua aplicação ao artefato.

O segundo objetivo específico foi definir, por meio de Lean Inception, o fluxo de detecção de possível dificuldade, sugestão de redirecionamento e coleta de feedback. Esse resultado aparece na definição do MVP, nas personas, nas jornadas, no sequenciamento de funcionalidades e no fluxo conceitual apresentado nos apêndices. A Lean Inception ajudou a justificar por que o produto deveria ser um mecanismo contextual de apoio à melhoria, e não uma ouvidoria, um chatbot ou um sistema completo de atendimento.

O terceiro objetivo específico foi construir API, páginas navegáveis, coleta de feedback e visualização administrativa, além de prever a comparação com formulário final. A implementação Python contém endpoints, páginas, popup, formulário reutilizável e agregações básicas. A comparação entre A e B foi desenhada e avaliada na interface Figma. O backend não registra grupo, modalidade do convite, conclusão da tarefa ou exposição efetiva ao formulário; portanto, a instrumentação comparativa funcional desse objetivo permanece parcial.

O quarto objetivo específico foi estruturar dados e indicadores para analisar eventos, avaliações e possíveis pontos de investigação. A implementação contém estruturas de eventos, alertas e feedbacks, além de consultas para agregação. A avaliação de interface no Figma oferece outro conjunto de registros, sem comprovar sua integração a essa base. A tabela construto → indicador → dado e a operacionalização das variáveis permanecem pendentes; não foi demonstrado que a estrutura atual basta para testar todas as hipóteses.

## 5.2 Limitações

A principal limitação é o tamanho e a seleção da amostra. A avaliação exploratória preliminar com oito participantes permitiu observar indícios sobre o uso do protótipo, mas não oferece base empírica suficiente para afirmar que o feedback contextual aumenta a taxa de resposta ou melhora a qualidade dos dados quando comparado a um formulário estático. Além disso, a avaliação heurística foi interna/preliminar, conduzida pelos autores, e não substitui inspeção independente por especialistas ou avaliação com gestores públicos.

O desenvolvimento também evidencia uma limitação organizacional. A tecnologia, isoladamente, não garante melhoria de serviços públicos. Para que o sistema gere impacto real, o órgão precisa tratar feedback negativo como insumo de aprendizado, definir responsáveis pela análise dos indicadores e transformar os alertas em decisões de melhoria. Sem essa rotina institucional, o painel poderia se tornar apenas um repositório de sinais de possível dificuldade e avaliações, sem efeito concreto na experiência do cidadão.

Os limiares de clique e duração são parâmetros operacionais, sem calibração com dados rotulados. A análise qualitativa é de projeto; a síntese da simulação não pode ser reproduzida, pois os arquivos de execução e parâmetros completos não estão disponíveis. Há risco de falsos positivos e negativos: leitura cuidadosa, tecnologia assistiva ou tarefa complexa podem acionar regras sem dificuldade declarada, enquanto problemas reais podem ocorrer abaixo dos limites.

Há ainda um desafio ético e de privacidade. Mesmo sem solicitar CPF, nome, e-mail ou credenciais de login na interface, identificadores técnicos, URL, coordenadas de clique e padrões de interação podem permitir associações ou inferências sobre usuários. O tempo observado no estudo Figma/Useberry e a duração simulada na API pertencem a bases distintas. Por isso, qualquer implantação real deve aplicar rigorosamente os princípios da LGPD, especialmente minimização, finalidade, transparência, controle de acesso, retenção limitada e anonimização efetiva ([Brasil, 2018](#ref-brasil2018lgpd)).

A avaliação com participantes ocorreu no Figma/Useberry, separadamente da aplicação Python. Não verifica endpoints, persistência, acionamento ou integração da API. O relato do sorteio auxiliado por IA não documenta seu mecanismo; o popup fez parte dos dois fluxos sem registro individual de exposição. O convite no Figma podia decorrer de tempo, tela ou clique, mas seus parâmetros e os acionamentos individuais não estão documentados nas sínteses disponíveis. Se preservadas, as gravações de tela poderão auxiliar a reconstituir os momentos dos convites; elas ainda não foram examinadas para esse fim. O esforço não foi medido por instrumento específico, e os comentários disponíveis são pós-sessão. O intervalo observado foi limitado a dez minutos. Essas características restringem a interpretação das diferenças entre os quatro casos de cada grupo.

Não houve comparação empírica com ferramentas existentes; a Tabela 2 é um posicionamento documental. A inspeção heurística não registra severidade, data e avaliadores individualizados. As capturas da Lean Inception preservam termos e metas de concepção, não resultados alcançados.

Também não houve integração com portais governamentais reais. Essa decisão manteve o escopo compatível com o TCC e evitou dependências de autorização institucional, segurança, governança e privacidade. Assim, os resultados devem ser interpretados como demonstração técnica local e parcial, não como comprovação de viabilidade integrada ou de impacto em produção.

## 5.3 Trabalhos Futuros

Os trabalhos futuros devem avançar em quatro frentes. A primeira é testar a hipótese comparativa com amostra maior, participantes mais diversos e protocolo previamente definido. No fluxo A, o usuário recebe um formulário estático ao final; no fluxo B, o sistema usa sinais comportamentais para solicitar feedback contextual. As variáveis dependentes devem incluir taxa de resposta, taxa de conclusão, esforço percebido, qualidade e especificidade dos comentários, abandono ou interrupção provocada e percepção de adequação do momento da pergunta. Só depois dessa coleta será possível avaliar, com evidência mais consistente, se um fluxo apresenta vantagens no cenário estudado.

A segunda frente é a calibração técnica. Os limiares atuais de clique e tempo foram definidos para demonstrar o funcionamento do protótipo. Em uma evolução, o sistema deve permitir configuração por serviço, por página e por tipo de tarefa. Também deve registrar versão das regras, evitar alertas duplicados, separar eventos por organização, criar filtros por período e serviço, e apresentar métricas comparáveis no painel. Essa etapa aproxima o protótipo de uma solução mais robusta de engenharia de software, com regras auditáveis e manutenção mais segura.

A terceira frente é a preparação para piloto autorizado. Uma implantação real exigiria aviso de coleta, definição de base legal e finalidade, política de retenção, controle de acesso ao painel, chave de API, separação por órgão, monitoramento de disponibilidade e documentação de integração do script cliente. Também seria necessário validar se os indicadores gerados realmente apoiam a decisão administrativa, por exemplo, priorização de páginas confusas, revisão de linguagem, redução de etapas e reorganização de menus.

Uma quarta frente é a avaliação externa do artefato. A avaliação heurística interna/preliminar deve ser complementada por inspeção independente de especialistas em usabilidade, Engenharia de Software ou governo digital e por walkthrough com gestores públicos. Essa etapa deve permanecer separada do teste de usabilidade com cidadãos, pois responde a perguntas técnicas e gerenciais distintas.

## 5.4 Conclusão

O trabalho apresenta uma implementação local parcial e observações exploratórias de interface, que permitem delimitar uma proposta de avaliação contextual de serviços públicos digitais. A viabilidade do fluxo integrado e sua utilidade para cidadãos e gestores ainda exigem avaliação. Os resultados não demonstram que a proposta resolva o problema de relacionar contexto e avaliação com maior eficácia do que instrumentos existentes.

A implementação explicita como eventos e respostas podem ser organizados em um fluxo contextual. A avaliação exploratória com oito participantes examinou a interface no Figma e registrou conclusão, facilidade e impressões pós-sessão. Não verificou o backend, não comparou a especificidade dos comentários do formulário e não confirmou benefício do fluxo contextual. Seu alcance é formativo e limitado ao desenho avaliado, com as restrições de protocolo e registro descritas no trabalho.

O percurso do trabalho também mostra que a solução não nasce apenas de uma decisão técnica de implementação. Ela foi delimitada por fundamentos de governo digital, qualidade percebida, usabilidade, privacidade e Lean Inception, e por artefatos de produto que explicitaram personas, jornadas, escopo, features, sequenciamento e critérios de verificação. Isso torna a proposta mais defensável como trabalho de Engenharia de Software, pois conecta problema, método, protótipo e indicadores.

A contribuição investigativa é a formulação de hipóteses sobre o momento da coleta, acompanhada da distinção entre evidências comportamentais e declaradas. A contribuição tecnológica é um protótipo com regras explícitas, feedback estruturado e agregações administrativas. Ainda são necessários a rastreabilidade dos construtos, instrumentos de coleta adequados e testes independentes. A proposta oferece uma base de desenvolvimento e investigação; seus benefícios, sua calibração e sua adequação a um serviço público real permanecem questões em aberto.

# Referências

<a id="ref-brasil2011lei12527"></a>

Brasil. **Lei n. 12.527, de 18 de novembro de 2011: Regula o acesso a informações previsto na constituição federal**. Brasília: Brasil. 2011. [Disponível em](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm). Acesso em: 18 jun. 2026.


<a id="ref-brasil2017decreto9094"></a>

Brasil. **Decreto n. 9.094, de 17 de julho de 2017: Dispõe sobre a simplificação do atendimento prestado aos usuários dos serviços públicos e institui a carta de serviços ao usuário**. Brasília: Brasil. 2017a. [Disponível em](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/decreto/d9094.htm). Acesso em: 19 jun. 2026.


<a id="ref-brasil2017lei13460"></a>

Brasil. **Lei n. 13.460, de 26 de junho de 2017: Dispõe sobre participação, proteção e defesa dos direitos do usuário dos serviços públicos da administração pública**. Brasília: Brasil. 2017b. [Disponível em](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13460.htm). Acesso em: 20 jun. 2026.


<a id="ref-brasil2018lgpd"></a>

Brasil. **Lei n. 13.709, de 14 de agosto de 2018: Lei geral de proteção de dados pessoais (LGPD)**. Brasília: Brasil. 2018. [Disponível em](https://www.planalto.gov.br/ccivil_03/_Ato2015-2018/2018/Lei/L13709compilado.htm). Acesso em: 21 jun. 2026.


<a id="ref-brasil2021lei14129"></a>

Brasil. **Lei n. 14.129, de 29 de março de 2021: Dispõe sobre princípios, regras e instrumentos para o governo digital e para o aumento da eficiência pública**. Brasília: Brasil. 2021. [Disponível em](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14129.htm). Acesso em: 22 jun. 2026.


<a id="ref-brasil2022decreto11260"></a>

Brasil. **Decreto n. 11.260, de 22 de novembro de 2022: Dispõe sobre a elaboração e o encaminhamento da estratégia nacional de governo digital**. Brasília: Brasil. 2022. [Disponível em](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/decreto/D11260.htm). Acesso em: 23 jun. 2026.


<a id="ref-govbrFerramentaAvaliacao"></a>

Brasil. **Ferramenta de avaliação: Governo digital**. Brasília: Brasil. 2026. [Disponível em](https://www.gov.br/governodigital/pt-br/plataformas-e-servicos-digitais/ferramenta-de-avaliacao). Acesso em: 28 jun. 2026.


<a id="ref-brasilMgi2024ppaParticipativo"></a>

Brasil. Ministério da Gestão e da Inovação em Serviços Públicos. **Relatório de resultados do PPA participativo 2024-2027**. Brasília: Brasil. Ministério da Gestão e da Inovação em Serviços Públicos. 2024. [Disponível em](https://www.gov.br/planejamento/documentos-hospedados-para-gerar-qrcodes/relatorio-ppaparticipativo). Acesso em: 22 jun. 2026.


<a id="ref-brasil2022portaria548"></a>

Brasil. Secretaria de Governo Digital. **Portaria SGD/ME n. 548, de 24 de janeiro de 2022: Dispõe sobre a avaliação de satisfação dos usuários de serviços públicos e estabelece padrões de qualidade para serviços públicos digitais**. Brasília: Brasil. Secretaria de Governo Digital. 2022. [Disponível em](https://in.gov.br/en/web/dou/-/portaria-sgd/me-n-548-de-24-de-janeiro-de-2022-375784151). Acesso em: 25 jun. 2026.


<a id="ref-caroli2018leanInception"></a>

Caroli, Paulo. **Lean inception: Como alinhar pessoas e construir o produto certo**. São Paulo: Editora Caroli. 2018.


<a id="ref-cetic2025ticDomicilios2024"></a>

Comitê Gestor da Internet no Brasil. **Pesquisa sobre o uso das tecnologias de informação e comunicação nos domicílios brasileiros: TIC domicílios 2024**. São Paulo: Comitê Gestor da Internet no Brasil. 2025. [Disponível em](https://www.cgi.br/publicacao/tic-domicilios-2024/). Acesso em: 24 jun. 2026.


<a id="ref-cooper1999inmates"></a>

Cooper, Alan. **The inmates are running the asylum: Why high-tech products drive us crazy and how to restore the sanity**. Indianapolis: Sams Publishing. 1999.


<a id="ref-deloneMclean2003"></a>

DeLone, William H.; McLean, Ephraim R. **The DeLone and McLean model of information systems success: A ten-year update**. Journal of Management Information Systems. 2003. v. 19. n. 4. p. 9-30. DOI: [10.1080/07421222.2003.11045748](https://doi.org/10.1080/07421222.2003.11045748). [Disponível em](https://www.tandfonline.com/doi/abs/10.1080/07421222.2003.11045748). Acesso em: 25 jun. 2026.


<a id="ref-fowler2022leanInception"></a>

Fowler, Martin; Caroli, Paulo. **Lean inception**. 2022. [Disponível em](https://martinfowler.com/articles/lean-inception/). Acesso em: 26 jun. 2026.


<a id="ref-govuk2021completionRate"></a>

Government Digital Service. **Measuring completion rate**. London: Government Digital Service. 2021a. [Disponível em](https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate). Acesso em: 27 jun. 2026.


<a id="ref-govuk2021usingData"></a>

Government Digital Service. **Using performance data to improve your service: An introduction**. London: Government Digital Service. 2021b. [Disponível em](https://www.gov.uk/service-manual/measuring-success/using-data-to-improve-your-service-an-introduction). Acesso em: 28 jun. 2026.


<a id="ref-gronroos1984service"></a>

Grönroos, Christian. **A service quality model and its marketing implications**. European Journal of Marketing. 1984. v. 18. n. 4. p. 36-44.


<a id="ref-hektner2007experienceSampling"></a>

Hektner, Joel M.; Schmidt, Jennifer A.; Csikszentmihalyi, Mihaly. **Experience sampling method: Measuring the quality of everyday life**. Thousand Oaks: Sage Publications. 2007.


<a id="ref-hevner2004designscience"></a>

Hevner, Alan R.; March, Salvatore T.; Park, Jinsoo; Ram, Sudha. **Design science in information systems research**. MIS Quarterly. 2004. v. 28. n. 1. p. 75-105. [Disponível em](https://aisel.aisnet.org/misq/vol28/iss1/6/). Acesso em: 18 jun. 2026.


<a id="ref-hotjar2026"></a>

HOTJAR. **What is hotjar?**. 2026. [Disponível em](https://help.hotjar.com/hc/en-us/articles/36820019634961-What-is-Hotjar). Acesso em: 28 jun. 2026.


<a id="ref-iso9241112018"></a>

International Organization for Standardization. **ISO 9241-11:2018: Ergonomics of human-system interaction — part 11: Usability: Definitions and concepts**. Geneva: International Organization for Standardization. 2018. [Disponível em](https://www.iso.org/standard/63500.html). Acesso em: 19 jun. 2026.


<a id="ref-iso92412102019"></a>

International Organization for Standardization. **ISO 9241-210:2019: Ergonomics of human-system interaction — part 210: Human-centred design for interactive systems**. Geneva: International Organization for Standardization. 2019. [Disponível em](https://www.iso.org/standard/77520.html). Acesso em: 20 jun. 2026.


<a id="ref-kahneman1993peakEnd"></a>

Kahneman, Daniel; Fredrickson, Barbara L.; Schreiber, Charles A.; Redelmeier, Donald A. **When more pain is preferred to less: Adding a better end**. Psychological Science. 1993. v. 4. n. 6. p. 401-405. DOI: [10.1111/j.1467-9280.1993.tb00589.x](https://doi.org/10.1111/j.1467-9280.1993.tb00589.x). [Disponível em](https://doi.org/10.1111/j.1467-9280.1993.tb00589.x). Acesso em: 21 jun. 2026.


<a id="ref-kalbach2016mapping"></a>

Kalbach, Jim. **Mapping experiences: A complete guide to creating value through journeys, blueprints, and diagrams**. Sebastopol: O’Reilly Media. 2016.


<a id="ref-larson1983experienceSampling"></a>

Larson, Reed; Csikszentmihalyi, Mihaly. **The experience sampling method**. In: Reis, Harry T. (org.). Naturalistic approaches to studying social interaction. San Francisco: Jossey-Bass. 1983. p. 41-56.


<a id="ref-limaPereira2020modulo1"></a>

Lima, Oto Buregio; Pereira, Wander Cleber. **Avaliação da qualidade de serviços como base para gestão e melhoria de serviços públicos: Módulo 1: Visão geral sobre serviços e avaliação de serviços públicos**. Brasília: Escola Nacional de Administração Pública. 2020a.


<a id="ref-limaPereira2020modulo2"></a>

Lima, Oto Buregio; Pereira, Wander Cleber. **Avaliação da qualidade de serviços como base para gestão e melhoria de serviços públicos: Módulo 2: Histórico e evolução dos modelos de avaliação de serviço**. Brasília: Escola Nacional de Administração Pública. 2020b.


<a id="ref-limaPereira2020modulo3"></a>

Lima, Oto Buregio; Pereira, Wander Cleber. **Avaliação da qualidade de serviços como base para gestão e melhoria de serviços públicos: Módulo 3: Aplicação de ferramentas de avaliação a um serviço específico**. Brasília: Escola Nacional de Administração Pública. 2020c.


<a id="ref-limaPereira2020modulo4"></a>

Lima, Oto Buregio; Pereira, Wander Cleber. **Avaliação da qualidade de serviços como base para gestão e melhoria de serviços públicos: Módulo 4: Melhoria dos serviços públicos**. Brasília: Escola Nacional de Administração Pública. 2020d.


<a id="ref-manfreda2008webSurveys"></a>

Lozar Manfreda, Katja; Bosnjak, Michael; Berzelak, Jernej; Haas, Iris; Vehovar, Vasja. **Web surveys versus other survey modes: A meta-analysis comparing response rates**. International Journal of Market Research. 2008. v. 50. n. 1. p. 79-104. DOI: [10.1177/147078530805000107](https://doi.org/10.1177/147078530805000107). [Disponível em](https://journals.sagepub.com/doi/10.1177/147078530805000107).


<a id="ref-mark2008interruptedWork"></a>

Mark, Gloria; Gudith, Daniela; Klocke, Ulrich. **The cost of interrupted work: More speed and stress**. In: Proceedings of the SIGCHI conference on human factors in computing systems. New York: ACM. 2008. p. 107-110. DOI: [10.1145/1357054.1357072](https://doi.org/10.1145/1357054.1357072). [Disponível em](https://www.ics.uci.edu/~gmark/chi08-mark.pdf).


<a id="ref-microsoftClarity2026"></a>

MICROSOFT. **Microsoft clarity documentation**. 2026. [Disponível em](https://learn.microsoft.com/en-us/clarity/). Acesso em: 28 jun. 2026.


<a id="ref-nielsen1994heuristic"></a>

Nielsen, Jakob. **Heuristic evaluation**. In: Nielsen, Jakob; Mack, Robert L. (org.). Usability inspection methods. New York: John Wiley & Sons. 1994. p. 25-62. [Disponível em](https://dl.acm.org/doi/10.5555/189200.189209). Acesso em: 23 jun. 2026.


<a id="ref-oliver2014satisfaction"></a>

Oliver, Richard L. **Satisfaction: A behavioral perspective on the consumer**. New York: Routledge. 2014.


<a id="ref-parasuraman1988servqual"></a>

Parasuraman, A.; Zeithaml, Valarie A.; Berry, Leonard L. **SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality**. Journal of Retailing. 1988. v. 64. n. 1. p. 12-40.


<a id="ref-pedrosa2019qualidadeGovbr"></a>

Pedrosa, Glauco Vitor; Gomes, Marília Miranda Forte; Silva, Wander Cleber Pereira; Sousa Oliveira Melo Veras, Daniel; Iwama, Gabriela Yukari; Menezes, Vítor Gomes. **Qualidade gov.br: Proposta de um modelo brasileiro de qualidade de serviços públicos digitais**. Brasília: Universidade de Brasília, Information Technology Research; Application Center; Ministério da Economia, Secretaria de Governo Digital. 2019.


<a id="ref-reichheld2003nps"></a>

Reichheld, Frederick F. **The one number you need to grow**. Harvard Business Review. 2003. v. 81. n. 12. p. 46-54. [Disponível em](https://hbr.org/2003/12/the-one-number-you-need-to-grow). Acesso em: 24 jun. 2026.


<a id="ref-schwarz1999selfReports"></a>

Schwarz, Norbert. **Self-reports: How the questions shape the answers**. American Psychologist. 1999. v. 54. n. 2. p. 93-105. DOI: [10.1037/0003-066X.54.2.93](https://doi.org/10.1037/0003-066X.54.2.93). [Disponível em](https://dornsife.usc.edu/norbert-schwarz/wp-content/uploads/sites/231/2023/11/99_ap_schwarz_self-reports.pdf).


<a id="ref-shihFan2008responseRates"></a>

Shih, Tse-Hua; Fan, Xitao. **Comparing response rates from web and mail surveys: A meta-analysis**. Field Methods. 2008. v. 20. n. 3. p. 249-271. DOI: [10.1177/1525822X08317085](https://doi.org/10.1177/1525822X08317085). [Disponível em](https://journals.sagepub.com/doi/10.1177/1525822X08317085).


<a id="ref-silva2024atributosApi"></a>

Silva, Wander Cleber M. P. **Estudo exploratório dos atributos de avaliação de qualidade de serviços públicos digitais: Sumário executivo**. Brasília: Ministério da Gestão e da Inovação em Serviços Públicos, Secretaria de Governo Digital; Universidade de Brasília, Information Technology Research; Application Center. 2024.


<a id="ref-silva2019brasp"></a>

Silva, Wander Cleber Pereira; Gomes, Marília Miranda Forte; Pedrosa, Glauco Vitor; Andrade Soares, Vanessa; Iwama, Gabriela; Menezes, Vítor Gomes; Paiva Vaz, Daniele; Guedes, Débora Janini Campos; Costa Figueiredo, Rejane Maria. **Avaliação da qualidade em serviços públicos: Um modelo para serviços digitizados, presenciais e parcialmente digitizados (BRASP)**. Brasília: Universidade de Brasília, Faculdade de Ciências e Tecnologias em Engenharia; Ministério da Economia, Secretaria de Governo Digital. 2019.


<a id="ref-silva2022modeloUnificado"></a>

Silva, Wander Cleber Pereira; Menezes, Vítor Gomes. **Proposta de modelo unificado de avaliação de serviços públicos digitalizados**. Brasília: Universidade de Brasília, Information Technology Research; Application Center; Ministério da Economia, Secretaria de Governo Digital. 2022.


<a id="ref-Sommerville2011"></a>

Sommerville, Ian. **Software engineering**. 9. ed. Addison-Wesley, 2011.


<a id="ref-sweller1988cognitiveLoad"></a>

Sweller, John. **Cognitive load during problem solving: Effects on learning**. Cognitive Science. 1988. v. 12. n. 2. p. 257-285. DOI: [10.1207/s15516709cog1202_4](https://doi.org/10.1207/s15516709cog1202_4). [Disponível em](https://doi.org/10.1207/s15516709cog1202_4). Acesso em: 26 jun. 2026.


<a id="ref-useberryFigma"></a>

Useberry. **Figma integration: Test figma prototypes in useberry**. s.d.. [Disponível em](https://www.useberry.com/integrations/figma). Acesso em: 15 out. 2026.


# Apêndice A — Síntese da Lean Inception

A Lean Inception foi usada como protocolo metodológico para definir o MVP do sistema de avaliação contextual. A atividade reuniu internamente quatro perspectivas de discussão: Felipe, atendimento público; Lucas, gestão digital; Diassis, viabilidade técnica; e Bruno, experiência do usuário. Esses perfis orientaram o alinhamento do produto e não constituem validação externa do artefato.

## A.1 Agenda

- Kick-off e visão do produto;

- dinâmica É / Não É / Faz / Não Faz;

- objetivos e hipótese do MVP;

- personas de cidadão e gestor;

- jornada do cidadão no serviço digital;

- brainstorming de features contextuais;

- revisão técnica, de negócio e UX;

- sequenciador;

- Canvas MVP.

## A.2 Escopo Delimitado

O produto é uma solução de feedback contextual com identificadores técnicos e dados agregados, voltada à melhoria de serviços públicos digitais. Não é ouvidoria, chatbot, sistema de espionagem, ferramenta de identificação individual ou implantação governamental completa.

## A.3 MVP

O MVP planejado reuniu as ondas 1, 2 e 3, implementadas parcialmente:

1.  base técnica de coleta: sessão com identificador técnico, cliques instrumentados e duração simulada na API; formulário final comparativo apenas no desenho Figma;

2.  detecção e feedback contextual: regra simples, convite contextual, estrelas, atributos, NPS e comentário;

3.  painel básico: consulta de alertas e agregações de eventos e respostas; taxas e comparações entre fluxos foram previstas, mas não estão instrumentadas na API atual.

# Apêndice B — Fluxo Conceitual do sistema de avaliação contextual

## B.1 Fluxo de navegação

O desenho parte do acesso a uma página pública ou de serviço. Na implementação Python, o cliente agrupa cliques de elementos instrumentados por identificador técnico e envia os eventos à API. A duração é recebida por endpoint e demonstrada por envio simulado de 120 segundos, sem cronômetro automático. A API compara os valores recebidos com parâmetros por serviço. No estudo de interface, a medição automática de tempo e cliques foi realizada pelo Useberry, em tarefas no Figma, separadamente desse backend.

## B.2 Detecção e redirecionamento

Se os sinais estiverem dentro da faixa esperada, a navegação segue normalmente. Se houver excesso de cliques ou tempo, a API registra o acionamento de uma regra como evidência comportamental de possível dificuldade. Esse registro não equivale a qualidade percebida nem a diagnóstico automático. Em serviços comuns, a navegação pode continuar sem popup. Em serviços marcados como prioritários ou de alto tráfego, a API pode retornar uma ação para sugerir redirecionamento.

## B.3 Feedback e painel

Quando a contagem de cliques ou a duração informada atende às condições operacionais, a API pode retornar uma ação para disponibilizar o convite de feedback. O feedback contém:

- avaliação geral por estrelas;

- seleção de características do problema, como clareza, tempo, esforço, usabilidade, atendimento e eficácia;

- pergunta de NPS;

- comentário opcional.

Na implementação atual, o administrador consulta alertas e agregações básicas de eventos e respostas. A comparação entre fluxos, a identificação de recorrências por atributo e o acompanhamento de melhorias são capacidades previstas, sem implementação demonstrada neste painel.

# Apêndice C — Endpoints e Indicadores do Protótipo

## C.1 Endpoints

O protótipo local usa API HTTP e banco SQLite. Os endpoints principais são:

- `GET /health`: verifica disponibilidade;

- `GET /api/services`: lista serviços e regras;

- `POST /api/events/click`: registra clique;

- `POST /api/events/page-time`: recebe duração informada, demonstrada por envio simulado;

- `GET /feedback`: exibe formulário de feedback;

- `POST /api/feedback`: salva avaliação estruturada;

- `GET /api/admin/alerts`: lista alertas administrativos;

- `GET /api/admin/dashboard`: retorna dados agregados.

## C.2 Indicadores

A implementação Python disponibiliza os seguintes dados administrativos:

- total de alertas;
- total de cliques por serviço;
- identificadores de sessão distintos por serviço, sem equivalência a sessões com alertas;
- total de feedbacks por serviço;
- média de estrelas por serviço;
- média da pergunta auxiliar de recomendação de 0 a 10, denominada `average_nps` no código, sem cálculo do escore NPS.

Taxa de resposta dos fluxos, ranking de serviços por alertas, recorrência de atributos e comentários recentes são indicadores planejados. Não estão presentes na resposta atual do endpoint do painel.

# Apêndice D — Protocolo Proposto para Walkthrough Externo

Este apêndice apresenta um protocolo para avaliação externa por especialistas, complementar à avaliação heurística interna/preliminar e à avaliação exploratória com participantes. Trata-se de etapa recomendada para fortalecer o ciclo de Design Science Research, não de atividade já executada.

## D.1 Objetivo da avaliação

Avaliar, com pelo menos um especialista externo ao grupo de desenvolvimento, a clareza do fluxo, a pertinência dos gatilhos de feedback contextual, o risco de interrupção, a compreensão dos atributos e a utilidade inicial do painel administrativo.

## D.2 Perfil recomendado do avaliador

O avaliador pode ser:

- professor ou pesquisador com experiência em interação humano-computador, governo digital ou Engenharia de Software;

- profissional de UX, produto digital ou pesquisa com usuários;

- gestor público ou servidor envolvido com atendimento digital, melhoria de serviços ou avaliação de satisfação.

## D.3 Roteiro de execução

1.  apresentar o objetivo do protótipo e esclarecer que o artefato, não o avaliador, está sendo avaliado;

2.  solicitar uma tarefa de localização de serviço na página simulada;

3.  acionar um cenário de excesso de cliques ou tempo;

4.  observar a reação ao popup e ao convite de feedback contextual;

5.  solicitar o preenchimento do formulário;

6.  apresentar o painel e discutir a utilidade dos indicadores;

7.  registrar comentários, dúvidas, fricções e recomendações.

## D.4 Checklist de observação

<div class="center">

| **Item observado** | **Pergunta de avaliação** | **Registro esperado** |
|:---|:---|:---|
| Momento do convite | O feedback apareceu em um momento compreensível da jornada? | Adequado, parcialmente adequado ou inadequado. |
| Interrupção | O popup ou o feedback pareceu intrusivo? | Comentário do avaliador. |
| Clareza dos atributos | Os atributos são compreensíveis e distinguíveis? | Atributos confusos ou sobrepostos. |
| NPS adaptado | A pergunta de recomendação faz sentido no contexto público? | Aceita, rejeitada ou precisa de reformulação. |
| Falso positivo | O avaliador identificou situações em que tempo ou cliques não significam dificuldade? | Exemplos levantados. |
| Painel administrativo | Os indicadores ajudam a priorizar ações de melhoria? | Indicadores úteis e indicadores ausentes. |
| Privacidade | A coleta parece proporcional e minimizada? | Riscos percebidos. |

</div>

## D.5 Forma de análise

Os achados podem ser organizados em três grupos:

- ajustes críticos, quando o problema impede compreensão ou uso do fluxo;

- ajustes recomendados, quando a melhoria aumenta clareza, utilidade ou confiança;

- ajustes futuros, quando dependem de piloto real, integração institucional ou coleta com mais participantes.

## D.6 Resultado esperado

O walkthrough não comprovaria a hipótese. Acrescentaria avaliação independente, confrontando as decisões dos autores com uma leitura externa.

# Apêndice E — Descrição do TCLE Utilizado

## E.1 Descrição do TCLE

O estudo foi conduzido mediante Termo de Consentimento Livre e Esclarecido, com identificação institucional, dos pesquisadores e do orientador, objetivo, procedimentos, riscos, benefícios, sigilo, direito de desistência, armazenamento e assinatura. O Useberry registrou eventos de interação e gravação de tela, conforme previsto no TCLE. Não houve gravação de áudio ou vídeo de câmera dos participantes.

O TCLE foi apresentado antes de cada sessão. Os termos assinados foram arquivados pelos pesquisadores e mantidos separados da base anonimizada. A versão integral do documento permanece em arquivo digital sob guarda dos autores.

# Apêndice F — Questionário Pós-Sessão

## F.1 Perguntas

Após a tarefa, os participantes responderam às seguintes perguntas:

1.  Em uma escala de 1 a 5, como você avalia a facilidade de uso do portal?

2.  Você encontrou o que procurava? (Sim / Não / Parcialmente)

3.  Para o fluxo B: quando a pergunta de avaliação apareceu, o que você fez? (Respondi / Ignorei / Fechei sem ler / Não apareceu)

4.  Para o fluxo B: o momento em que a pergunta apareceu foi adequado? (Sim / Não / Mais ou menos)

5.  Algum comentário sobre sua experiência?

# Apêndice G — Registros Anonimizados da Avaliação com Participantes

Os registros apresentam as classificações de tarefa, métricas do estudo Figma/Useberry, respostas ao questionário pós-sessão e observações do moderador. No campo “Respondeu ao feedback”, Sim indica realização da avaliação no formulário final no fluxo A e aceite do convite seguido de realização da avaliação no fluxo B; Não indica que o critério do respectivo fluxo não foi atendido. Essa classificação não transforma os comentários pós-sessão em comentários do formulário. Para leitura, “N.A.” foi expandido para “Não se aplica” e a nota de facilidade explicita a escala de 1 a 5. Os comentários literais são respostas pós-sessão, não comentários do formulário de feedback. As observações são apresentadas separadamente e não constituem medida de especificidade. O conjunto apresentado não inclui a exportação primária do Useberry. As intervenções registradas em P05 e P07 devem ser consideradas na interpretação dos resultados.

## G.1 P01 — Fluxo A

Data: 28/06/2026. Perfil: Estudante FCTE — Engenharia de Software. Já usou GOV.BR: Sim. Concluiu: Sim. Tempo: 06:42. Cliques: 15. Convite apareceu: Não se aplica. Respondeu ao feedback: Sim. Facilidade: 4/5. Encontrou: Sim.

Comentário literal:

> Eu achei parecido com o gov.br e consegui entender o caminho, mas demorei um pouco para diferenciar consulta de declaração.

Observações do moderador: Leu a lista de serviços antes de clicar em Fazer minha declaração; concluiu sem pedir ajuda.

## G.2 P02 — Fluxo B

Data: 28/06/2026. Perfil: Cidadão — Assistente administrativo. Já usou GOV.BR: Sim. Concluiu: Sim. Tempo: 07:18. Cliques: 18. Convite apareceu: Sim. Respondeu ao feedback: Sim. Facilidade: 4/5. Encontrou: Sim.

Comentário literal:

> A pergunta apareceu quando eu estava parado no formulário. Achei bom porque deu para explicar minha dúvida na hora.

Observações do moderador: Hesitou no campo de serviço; respondeu ao convite contextual com comentário específico.

## G.3 P03 — Fluxo A

Data: 28/06/2026. Perfil: Cidadão — Autônoma. Já usou GOV.BR: Sim. Concluiu: Parcial. Tempo: 09:21. Cliques: 24. Convite apareceu: Não se aplica. Respondeu ao feedback: Não. Facilidade: 2/5. Encontrou: Parcialmente.

Comentário literal:

> Eu fui clicando, mas não tive certeza se estava fazendo a declaração ou só consultando uma informação.

Observações do moderador: Voltou duas vezes para a primeira tela; não respondeu ao formulário final.

## G.4 P04 — Fluxo B

Data: 28/06/2026. Perfil: Estudante FCTE — Engenharia de Software. Já usou GOV.BR: Sim. Concluiu: Sim. Tempo: 05:56. Cliques: 13. Convite apareceu: Não. Respondeu ao feedback: Não se aplica. Facilidade: 5/5. Encontrou: Sim.

Comentário literal:

> Foi tranquilo. Eu fui direto no botão principal e entendi que era um protótipo.

Observações do moderador: Não recebeu convite contextual porque avançou rapidamente até a confirmação.

## G.5 P05 — Fluxo A

Data: 28/06/2026. Perfil: Cidadão — Professora da educação básica. Já usou GOV.BR: Sim. Concluiu: Sim. Tempo: 08:04. Cliques: 20. Convite apareceu: Não se aplica. Respondeu ao feedback: Sim. Facilidade: 3/5. Encontrou: Sim.

Comentário literal:

> Consegui terminar, mas alguns nomes são muito parecidos. Eu esperava uma explicação maior antes de avançar.

Observações do moderador: Pediu confirmação verbal se o protótipo era seguro; moderador apenas reforçou que deveria agir como faria em casa.

## G.6 P06 — Fluxo B

Data: 28/06/2026. Perfil: Cidadão — Microempreendedor individual. Já usou GOV.BR: Sim. Concluiu: Não. Tempo: 10:00. Cliques: 29. Convite apareceu: Sim. Respondeu ao feedback: Não. Facilidade: 2/5. Encontrou: Não.

Comentário literal:

> Ignorei a pergunta porque queria tentar resolver primeiro, mas depois me perdi e não cheguei ao final.

Observações do moderador: Recebeu convite contextual aos 4 minutos, ignorou e estourou o tempo máximo.

## G.7 P07 — Fluxo A

Data: 28/06/2026. Perfil: Cidadão — Aposentado. Já usou GOV.BR: Não. Concluiu: Não. Tempo: 10:00. Cliques: 22. Convite apareceu: Não se aplica. Respondeu ao feedback: Não. Facilidade: 1/5. Encontrou: Não.

Comentário literal:

> Eu não entendi onde começava. Para mim parecia ter muita informação na tela.

Observações do moderador: Baixa familiaridade com Figma; recebeu demonstração inicial e teve dificuldade na primeira tela.

## G.8 P08 — Fluxo B

Data: 28/06/2026. Perfil: Cidadão — Analista financeiro. Já usou GOV.BR: Sim. Concluiu: Sim. Tempo: 06:49. Cliques: 16. Convite apareceu: Sim. Respondeu ao feedback: Sim. Facilidade: 4/5. Encontrou: Sim.

Comentário literal:

> O aviso no meio do caminho apareceu em um momento adequado. Eu só deixaria o texto mais curto.

Observações do moderador: Respondeu ao convite contextual; concluiu após retornar ao fluxo principal.
