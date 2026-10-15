# Controle da revisão do TCC em Markdown

## Objetivo desta rodada

Trabalhar no conteúdo de [tcc.md](tcc.md), começando exclusivamente pelo curto prazo, conforme a escolha dos autores nesta conversa. O arquivo reúne resumo, abstract, cinco capítulos, referências e sete apêndices. As imagens continuam vinculadas aos arquivos existentes do projeto. [referencias-tcc.bib](referencias-tcc.bib) preserva as chaves usadas no manuscrito e as entradas recuperadas, para a futura transposição ao LaTeX.

O Markdown é a fonte editorial do conteúdo. Após aprovação do curto prazo pelo usuário, o LaTeX passou a ser sincronizado a partir dele por `scripts/sincronizar_tcc.py`, com cópia da bibliografia complementar. O protótipo não foi alterado. Não editar simultaneamente o mesmo conteúdo nas duas versões sem reconciliar as mudanças. A nomenclatura, as referências e as telas com NPS ainda descrevem o protótipo desta etapa; sua retirada pertence à rodada de médio prazo e não foi executada.

## Mudanças desta rodada

- Recuperação da fundamentação científica sobre autorrelato, taxas de resposta, coleta situada e interrupção: Schwarz; Shih e Fan; Lozar Manfreda et al.; Larson e Csikszentmihalyi; Hektner et al.; Mark, Gudith e Klocke.
- Retirada de Delighted e SurveyMonkey do argumento científico sobre taxas de resposta. As referências comerciais de Hotjar e Microsoft Clarity continuam restritas à caracterização documental de funcionalidades.
- Explicitação de que ESM é uma aproximação conceitual do mecanismo, sem declarar execução integral desse método no estudo.
- Ajuste das afirmações de benefício do convite contextual: hipótese a testar, sem superioridade comprovada nem validação da utilidade gerencial.
- Recuperação dos comentários literais e das observações de P01–P08 publicados no PDF original. Nenhuma nova entrevista ou teste foi realizado. Quebras e hifenização de fim de linha do PDF foram normalizadas.
- Registro do pedido de confirmação sobre segurança em P05, da orientação verbal do moderador para agir como em casa e da demonstração inicial em P07, evitando afirmar ausência absoluta de intervenção.
- Substituição da impossibilidade absoluta de comparação estatística pela ressalva sobre fragilidade das conclusões comparativas.
- Omissão da declaração de aprovação e dos nomes provisórios da banca nesta versão de conteúdo. Esses dados serão preenchidos conforme a situação acadêmica real na transposição ao modelo institucional.
- Preservação das 13 tabelas e seis figuras existentes; inclusão de CES e ESM na lista de siglas; correção de “três frentes” para “quatro frentes” nos trabalhos futuros.

## Situação do curto prazo

| Item | Situação nesta rodada | Evidência ou dependência |
| --- | --- | --- |
| 1 — Autores e título | Atendido no conteúdo | Júlio e Fernando; título do Trabalho 1. |
| 5 — Construto → indicador → dado | Pendente por dependência | Elaborar após definição e operacionalização do CES. A Tabela 8 atual não substitui esse artefato. |
| 16 — Telemetria versus percepção | Revisado | Distinção mantida nos capítulos e na conclusão; gatilho não equivale a dificuldade confirmada. |
| 20 — Avaliação exploratória controlada | Revisado | Estudo de interface Figma/Useberry separado da implementação Python/API; sem validação em serviço real. |
| 21 — Cautela com a amostra | Revisado | Resultados descritivos; retiradas as conclusões sobre especificidade dos comentários do formulário. |
| 22 — Hipótese e variáveis | Formulação revista; operacionalização pendente | H1/H2 direcionais e medidas ausentes explicitadas; instrumentos e execução comparativa futura ainda pendentes. |
| 23 — Heurística interna/preliminar | Atendido na nomenclatura | Inspeção dos autores não equivale a parecer independente. |
| 25 — Contribuição científica e tecnológica | Alegação delimitada | Hipóteses e implementação descritas sem modelo de mensuração validado, auditoria comprovada ou simulação reprodutível. |
| 27 — Natureza das fontes | Revisado | Classificação individual das fontes e limites de uso de relatórios, material didático, literatura profissional e documentação comercial. |

“Revisado” significa alteração editorial realizada. Não significa aprovação dos autores, do orientador ou de uma banca. O item 5 impede declarar todo o conjunto de curto prazo concluído.

## Próximas rodadas, ainda não executadas

| Itens | Trabalho necessário |
| --- | --- |
| 2 e 7 | Reescrever o Trabalho 1 sem NPS; definir CES; atualizar formulário, dados, API, painel, documentação e imagens; distinguir dados históricos de coleta futura. |
| 5 | Construir a tabela construto → indicador → dado depois da decisão sobre CES. |
| 6 e 8 | Ampliar E-S-QUAL/E-RecS-QUAL e diferenciar software, interação, qualidade percebida e efetividade do serviço. |
| 9 | Reestruturar o percurso metodológico pelas etapas da DSR, com Lean Inception como técnica de concepção. Registrar fielmente a cronologia executada. |
| 10 e 11 | Especificar requisitos, regras de negócio, histórias/casos de uso, critérios de aceitação e matriz necessidade → requisito → componente → teste/evidência. |
| 12 | Selecionar características da ISO/IEC 25010:2023 e vinculá-las às evidências previstas. |
| 13 | Elaborar plano de verificação e validação; separar planejamento de testes efetivamente executados. |
| 14 e 15 | Gerir e versionar parâmetros; planejar e executar calibração com dados rotulados. Os limites atuais não são cientificamente validados. |
| 17 e 18 | Formalizar requisitos verificáveis de privacidade e acessibilidade; executar as avaliações cabíveis na etapa empírica. |
| 19 | Preparar protocolos distintos para cidadãos, gestores e especialistas; recrutar e avaliar posteriormente. |
| 22 e 23 | Executar estudo comparativo e avaliação heurística externa com protocolo adequado. A revisão de um agente de texto não cumpre essas avaliações empíricas. |
| 24 | Definir dado → insight → ação → acompanhamento e refletir essa cadeia no painel. |
| 26 | Revisar referências, metadados, normalização ABNT e modelo institucional após estabilização do conteúdo. |

Itens 3 e 4 e a orientação inversa destinada ao trabalho de Wesley continuam fora do escopo. As menções do professor a “TCC 2” nos itens de continuidade são tratadas como etapa futura deste artefato, sem incorporar a fundamentação do trabalho separado de Wesley.

## Pontos factuais para conferência dos autores

- Confirmar a situação acadêmica e a data real de aprovação antes de preencher a folha correspondente. A versão anterior declara 27/06/2026, enquanto a coleta relatada ocorreu em 28/06/2026.
- Confirmar se os registros originais de P01–P08 e suas transcrições estão fiéis aos documentos sob guarda dos autores. O trabalho nesta rodada recupera o que consta no PDF fornecido; não autentica a coleta.
- O usuário confirmou que a avaliação dos oito participantes ocorreu no Figma, instrumentada pelo Useberry, com cliques e tempos automáticos. O texto separa essa avaliação da implementação Python/API. Não foi demonstrada execução da API por esses participantes.
- O Apêndice E descreve o TCLE, mas não reproduz seu modelo integral. Não publicar termos assinados nem inventar conteúdo do documento ausente. Conferir se o modelo sem dados pessoais deverá integrar a entrega final.
- Conferir metadados herdados da bibliografia, incluindo edição/ano de Sommerville, documentos institucionais, atos normativos e datas de acesso. A recuperação de seis fontes não representa auditoria completa das demais referências.

## Evidências das fontes recuperadas

As afirmações acrescentadas foram limitadas ao alcance das fontes. Não se atribui às meta-análises de modos de pesquisa comprovação de vantagem do convite contextual.

- [Schwarz — texto do autor disponibilizado pela USC](https://dornsife.usc.edu/norbert-schwarz/wp-content/uploads/sites/231/2023/11/99_ap_schwarz_self-reports.pdf).
- [Shih e Fan — página da publicação](https://journals.sagepub.com/doi/10.1177/1525822X08317085).
- [Lozar Manfreda et al. — página da publicação](https://journals.sagepub.com/doi/10.1177/147078530805000107).
- [Hektner, Schmidt e Csikszentmihalyi — editora](https://us2.sagepub.com/en-us/nam/experience-sampling-method/book228179). O ano 2007 segue a edição referenciada no original; a página comercial informa lançamento em setembro de 2006. Conferir a folha de rosto da edição consultada na normalização final.
- [Larson e Csikszentmihalyi — registro institucional da republicação](https://experts.illinois.edu/en/publications/the-experience-sampling-method/). A referência de 1983 foi recuperada do PDF original; não confundir seus metadados com os da republicação de 2014.
- [Mark, Gudith e Klocke — texto disponibilizado pela autora](https://www.ics.uci.edu/~gmark/chi08-mark.pdf).

## Sequência de avaliação e entrega

1. Revisão editorial desta rodada em Markdown.
2. Revisão independente de um agente, com parecer registrado e correções pertinentes incorporadas. Essa revisão é textual e não substitui especialistas do estudo.
3. Avaliação pessoal dos autores e decisão de avançar à próxima rodada.
4. Repetição desse ciclo para as pendências de médio prazo e planejamento de longo prazo, sem criar resultados empíricos fictícios.
5. Nova análise CopySpider da versão consolidada e conferência das coincidências em contexto. O relatório já fornecido corresponde ao PDF anterior e não certifica esta revisão.
6. Após aprovação do conteúdo, transposição para LaTeX, conferência das referências, normalização, compilação e inspeção visual.
7. Revisão final dos autores sobre o PDF e registro das alterações em um branch `codex/…`, com commit solicitado nesta conversa para essa etapa futura.

## Avaliações desta versão

- Revisão editorial: retoques finais 1–6 do parecer recebido aplicados. Critérios de resposta separados entre A e B, gravação limitada à tela e eventos confirmada pelo usuário, e afirmações de viabilidade e baixo esforço ajustadas. Os valores exatos dos gatilhos e os registros individuais continuam sem detalhamento.
- Revisão independente de agente: segunda rodada reconferida; seu parecer não certifica o fechamento da terceira rodada ou resolve os detalhes experimentais ainda ausentes.
- CopySpider da versão revisada: pendente.
- Avaliação pessoal dos autores: parecer recebido considera o grupo obrigatório resolvido e condiciona a aprovação editorial aos retoques 1–6, agora aplicados; a versão final atualizada está disponível para conferência.
- Aprovação do orientador: não presumida.
- Conversão final para LaTeX e commit: aguardam as etapas acima.

## Conferência de integridade desta rodada

A primeira conferência local encontrou os cinco capítulos, sete apêndices, 13 tabelas numeradas, seis figuras vinculadas a arquivos existentes, oito comentários literais e 44 referências citadas. A segunda rodada acrescentou a documentação comercial do Useberry e exige nova conferência de integridade. Essas verificações não representam execução de testes do protótipo nem auditoria completa das fontes.

## Segunda rodada — crítica externa e esclarecimentos dos autores

A revisão crítica recebida pelo usuário comparou o PDF original ao Markdown colado em outra conversa; não teve acesso aos arquivos locais, ao controle de revisão ou à bibliografia de trabalho. Seus achados foram conferidos aqui sem adotar suas conclusões automaticamente. O parecer inicial foi excessivamente favorável quanto à suficiência dos dados para algumas alegações, e esta rodada corrige o alcance dessas interpretações.

### Informações confirmadas pelo usuário nesta conversa

- Os oito participantes usaram Figma; cliques e tempos foram registrados automaticamente pelo Useberry.
- A distribuição entre A e B foi feita por sorteio auxiliado por IA. Não foram fornecidos ferramenta, comando, semente ou trilha de execução; o texto não afirma aleatorização auditada.
- O popup de redirecionamento fez parte dos dois fluxos. Os registros transcritos não discriminam sua exibição ou aceitação por participante.
- Os comentários literais vieram do questionário pós-sessão, não do formulário contextual.
- Felipe, Lucas, Diassis e Bruno foram participantes reais da discussão. Seus vínculos e qualificações não foram ampliados por inferência; Lucas da discussão é distinto da persona Lucas Almeida.
- Os registros da simulação de 1.000 sessões não estão mais disponíveis. Não houve nova execução nem reconstrução artificial dos resultados.

### Alterações incorporadas

- Resumo, abstract, metodologia, resultados e conclusão separam avaliação de interface no Figma/Useberry de implementação Python/API.
- Foram retiradas as conclusões de maior especificidade dos comentários do formulário: esse corpus não foi apresentado, e os comentários disponíveis são pós-sessão.
- H1 e H2 foram formuladas direcionalmente para estudo futuro. A situação de cada variável está descrita, incluindo ausência de medida específica de esforço e de rubrica aplicada aos comentários.
- Os critérios C1–C7 da seção 3.5 correspondem à Tabela 10. Esforço foi marcado como não medido; utilidade gerencial, anonimização e benefícios não são tratados como comprovados.
- O parâmetro armazenado 12 aciona no 13º clique; o parâmetro 10 aciona no 11º. No contexto inicial, o convite por clique começa no 14º. O texto distingue parâmetro, primeiro acionamento e convite, sem atribuir os totais do Figma às regras da API.
- A inspeção do cliente Python mostrou envio de duração por botão de simulação, sem cronômetro automático nesse cliente. Essa limitação está descrita, sem alterar o protótipo.
- O campo administrativo `silent` foi explicitado. Renomear um alerta no texto não implementa transparência, retenção ou controle de acesso; esses requisitos continuam pendentes.
- A nova inspeção independente detectou três divergências adicionais e elas foram corrigidas: painel atribuído além do código, comparação A/B declarada implementada e anonimato absoluto. O painel atual não calcula escore NPS nem agrega atributos ou comentários, e a API não persiste grupo, exposição ou conclusão de tarefa. Identificadores técnicos e ausência de nome/CPF na interface não comprovam anonimização.
- A simulação foi identificada como relato anterior não reproduzido. O caminho histórico do script é mencionado como indisponível, sem criar link para arquivo inexistente nem afirmar reprodutibilidade.
- Os denominadores, a conclusão parcial de P03 e a inclusão dos encerramentos aos dez minutos foram explicados. A média de cliques do A foi apresentada como 20,25, evitando ambiguidade de arredondamento.
- Datas de acesso expressamente presentes no PDF original foram recuperadas; DOI, editores e dados de publicação voltaram à apresentação das referências quando disponíveis na bibliografia. Isso não autentica datas de consulta nem encerra a revisão ABNT.
- Fontes foram classificadas individualmente na lista de referências, incluindo relatórios técnicos, material didático e literatura profissional. Useberry é documentação comercial, não evidência científica de eficácia.
- As Figuras 1–4 foram inspecionadas: preservam o nome histórico do protótipo, metas e alegações de concepção. Foram acrescentadas fontes e ressalvas nas legendas, sem alterar retrospectivamente o artefato. Nenhum nome de Wesley foi identificado nessas quatro imagens. O TCLE integral continua indisponível para essa conferência.

### Pontos que continuam abertos

- Operacionalização completa de H1/H2, CES e tabela de construtos — itens 5, 7 e parte futura do 22.
- Reconstrução do procedimento de sorteio e dos eventos individuais de exposição no Figma, se os autores dispuserem de documentação.
- Instrumentação dos convites no Figma: a configuração exata que explica P04 sem convite e P06 com convite aos quatro minutos não está documentada nos registros transcritos. A implementação Python atual não pode ser usada para preencher essa lacuna.
- Fonte primária do Useberry, corpus de respostas do formulário, respostas completas à pergunta de adequação do momento e registros técnicos da inspeção interna não foram apresentados nesta rodada.
- Metadados de Sommerville e demais referências herdadas continuam sujeitos à conferência bibliográfica final. O ano/edição não foi corrigido por suposição.
- A simulação não deve fundamentar a escolha de limiares enquanto não houver recuperação dos arquivos ou uma nova execução explicitamente documentada.

O item 1 diz respeito a autores e título do trabalho. Não exige, por si só, apagar o nome histórico do produto das evidências de concepção. A terminologia corrente foi uniformizada para “sistema de avaliação contextual”, preservando as imagens como documentos daquela etapa.

### Conferência estrutural da segunda rodada

Foram mantidos cinco capítulos, sete apêndices, 13 tabelas numeradas, seis figuras existentes e oito comentários literais. As 45 referências citadas têm entradas na bibliografia, classificação de natureza e destinos internos. C1–C7 têm correspondência entre a seção 3.5 e a Tabela 10. As médias e contagens dos participantes foram preservadas, exceto a explicitação de 20,25 cliques no fluxo A para evitar convenção implícita de arredondamento. O parecer anterior foi reaberto após a crítica externa. Os três últimos ajustes foram incorporados e reconferidos pelo agente, que registrou parecer favorável ao fechamento editorial desta rodada. As pendências factuais, empíricas e de médio prazo acima permanecem.

## Terceira rodada — voz autoral e coerência entre componentes

O novo parecer foi recebido no arquivo anexado `fc889c66-7b9f-44aa-9bc1-d0eb5b523437/Texto colado.txt`. A prioridade desta rodada é resolver afirmações que excedem a implementação e a avaliação descritas, sem antecipar requisitos de médio prazo ou criar dados ausentes.

### Correções textuais incorporadas

- Remoção da voz de parecer externo no manuscrito: “conforme confirmação dos autores”, “código consultado”, “nesta revisão”, “documento original” e a nota de trabalho de abertura das referências.
- Separação dos dois componentes do artefato na seção 3.1 e na Tabela 2: implementação local Python versus interfaces Figma. Cada componente tem procedimento de avaliação distinto.
- Alinhamento de introdução, referencial, metodologia, resultados, conclusão e apêndices com a ausência de cronômetro automático no cliente Python, as agregações básicas do painel e a interpretação auxiliar não validada da pergunta de recomendação.
- O planejamento das ondas 1–3 não é apresentado como entrega integral. Regras por serviço estão implementadas, apesar de previstas inicialmente na onda 4; comparação A/B, ranking e taxa de resposta não estão instrumentados no backend.
- H1/H2 permanecem formuladas apenas na seção 3.5, com remissão na introdução. As demais variáveis foram identificadas como secundárias; H2 considera somente respondentes, com risco de seleção explicitado.
- O problema de pesquisa foi harmonizado e a tradução do percurso bibliográfico/normativo foi alinhada no abstract.
- Correção da frase duplicada sobre identificadores e esclarecimento de que `x` e `y` são coordenadas do clique na tela, não geolocalização. O formulário não pede credenciais de login, mas o backend admite `user_id` opcional.
- A semântica dos rótulos da simulação foi marcada como desconhecida: não se equipara o cenário “13 cliques” ao parâmetro 12 do código nem se inventa o comparador da análise perdida.
- Ajustes pequenos de apresentação: siglas em ordem, retirada de ABNT da lista por ausência no texto e fontes das Tabelas 3 e 7 próximas às tabelas, no padrão “Fonte:”. Isso não equivale a revisão ABNT completa.
- As fontes das figuras passaram a identificar o acervo de concepção/desenvolvimento do projeto, sem atribuir produção exclusiva aos dois autores atuais. As Figuras 5 e 6 são da implementação Python; não substituem capturas das interfaces A/B avaliadas.

### Informações ainda necessárias para a descrição do estudo

1. **Gatilho no Figma:** evento e configuração que faziam o convite aparecer no B. Não deduzir tempo, tela, clique ou intervenção do moderador a partir dos dados agregados. P04 e P06 não podem ser explicados pelas regras do Python.
2. **Definição de resposta:** qual ação contou como “respondeu ao feedback” em A e B e onde foi registrada. Não presumir digitação de comentário no Figma ou confundir a resposta pós-sessão com envio do formulário.
3. **Evidência visual:** capturas ou registro das telas A/B e do convite efetivamente usados. Não criar imagens novas para representá-las como capturas históricas.

As perguntas foram respondidas no nível dos tipos de evento e do critério de resposta, conforme atualização abaixo. A descrição foi incorporada sem inventar parâmetros ou registros individuais. A condição experimental ficou mais delimitada, mas não integralmente reconstituível pelos materiais apresentados.

### Autoria, ética e documentação — conferência com os autores/orientador

- Quem moderou as sessões; participação de Wesley na coleta ou na Lean Inception; pesquisadores nomeados no TCLE; autoria das imagens e modo de reconhecer a origem compartilhada. O uso de “acervo da etapa conjunta” é uma atribuição geral, não resolve a identificação de créditos nem implica aprovação do orientador sobre a nota final.
- Conferir o TCLE integral: menção ao Useberry, ao registro de interações por terceiro e ao significado de “ausência de gravação”. Sem acesso ao documento não se conclui cobertura, conformidade ou irregularidade.
- Conferir com o orientador a necessidade e situação de tramitação ética aplicável. Não presumir aprovação, dispensa ou enquadramento normativo com base apenas neste texto.
- Verificar possibilidade de exportação dos dados primários do Useberry e das respostas às perguntas 3 e 4 do questionário. Ausência de apresentação não equivale a prova de que não foram coletadas.

### Normalização mantida para a etapa própria

As classificações “Natureza” permanecem provisoriamente nas referências para rastreabilidade editorial; sua apresentação final deve ser transferida a quadro metodológico ou apêndice. A edição efetivamente consultada de Sommerville continua a exigir confirmação; não foram alterados ano ou edição por suposição. Esses pontos, assim como a revisão completa de ABNT e do modelo institucional, pertencem ao item 26.

### Conferência dirigida da terceira rodada

O agente conferiu apenas voz autoral e coerência das capacidades já conhecidas. Três resíduos foram encontrados e corrigidos: gatilho descrito como dificuldade confirmada no Apêndice B.3, justificativas antigas de percepção/comparação global para NPS nas Tabelas 9 e 13 e a expressão “ampliação solicitada” na seção 5.1. A conferência confirmou a distinção entre componentes e o MVP parcial. Não houve aprovação global da rodada, pois o mecanismo do convite e a definição operacional de resposta continuam dependentes das informações dos autores. As medidas da Tabela 12 foram explicitadas como classificações registradas, com essa limitação.

### Atualização factual após resposta do usuário

- **Convite no Figma:** tempo decorrido, entrada em uma tela ou clique podiam fazer o convite aparecer. A resposta não especifica valores, telas, alvos de clique, combinação de condições ou gatilho de cada participante. O manuscrito registra os três tipos sem associá-los às regras do Python nem explicar retrospectivamente P04/P06.
- **Critério de resposta em A e B:** aceitar o convite e realizar a avaliação sobre o ocorrido. Não se presume envio de formulário para API, comentário digitado, botão específico ou obrigatoriedade de todos os campos. Os comentários literais continuam identificados como pós-sessão.
- **Coordenação:** Julio e Fernando coordenaram as sessões. A resposta não individualiza quem moderou cada sessão nem identifica outros pesquisadores eventualmente nomeados no TCLE.
- **Wesley:** participou da Lean Inception voltada ao tema de seu trabalho. Não foi confirmada participação na coleta desta avaliação. Não converter essa ausência de confirmação em afirmação de que participou ou não participou da coleta.
- **Figuras:** Fernando produziu as figuras; os créditos das seis imagens foram atualizados com seu nome. A nota genérica de origem compartilhada foi substituída pela autoria confirmada e pela descrição da etapa de concepção. A forma final de reconhecer o desmembramento do trabalho pode ser conferida com o orientador.
- **TCLE:** o usuário confirmou menção ao Useberry e à gravação de interações. Foi retirada a afirmação ampla de “ausência de gravação”. A confirmação não distingue captura de tela, áudio, vídeo e eventos; não se infere ativação de recursos específicos, conteúdo integral do consentimento, cobertura jurídica ou aprovação ética.

Permanecem pendentes o acesso às telas A/B e exportações primárias, os parâmetros exatos dos acionamentos, a identidade dos pesquisadores nomeados no TCLE e a conferência ética/documental com o orientador. São lacunas registradas, sem criação de evidências ou de novas coletas.

## Retoques finais após parecer favorável ao grupo obrigatório

Foram aplicados os seis ajustes finais solicitados, sem modificar os valores dos resultados:

1. A seção 5.2 passou a caracterizar os resultados como demonstração técnica local parcial, sem alegar viabilidade do fluxo integrado.
2. O usuário confirmou gravação apenas de tela e eventos de interação no Useberry. A informação foi escrita diretamente no Apêndice E e harmonizada nas seções 3.6 e 4.14; não houve áudio ou vídeo de câmera dos participantes. Isso não substitui a conferência do TCLE integral e do enquadramento ético com o orientador.
3. A seção 4.14 passou a mencionar quem não realizou a avaliação, sem supor envio de formulário.
4. O critério de resposta foi corrigido em todos os locais relacionados: A corresponde a realizar a avaliação no formulário final; B corresponde a aceitar o convite e realizar a avaliação. A Tabela 12 passou a usar o rótulo comum “Realizou a avaliação / participantes”, preservando 2/4 em cada grupo.
5. A seção 4.1 passou a descrever feedback curto, sem declarar baixo esforço medido.
6. Foi acrescentada a vírgula no resumo, separando a ressalva sobre o sorteio da presença do popup nos dois fluxos.

O parecer recebido considera os problemas obrigatórios resolvidos e permite aprovação editorial do curto prazo após esses retoques. Isso não encerra a tabela de construtos dependente do CES, os requisitos de médio prazo, a normalização, a revisão dos metadados de Sommerville, a conferência de autoria/ética/TCLE, a preservação dos dados do Useberry ou a nova análise CopySpider. Não foi iniciada sincronização com LaTeX nem realizado commit nesta etapa.

A recuperação opcional das configurações e capturas históricas do Figma continua registrada. Não foram inventados intervalos de tempo, telas ou cliques específicos para preencher essa lacuna.

### Conferência da cópia e redação final dos seis trechos

Após o usuário relatar que a cópia avaliada ainda continha trechos antigos, o arquivo local foi relido. As seis alterações da rodada anterior estavam presentes. A redação foi então alinhada às substituições exatas enviadas pelo usuário, incluindo “local e parcial”, “viabilidade integrada”, “avaliação na interface”, a descrição de A/B e “e com popup”. No Apêndice E foi mantida a modalidade confirmada: eventos e gravação de tela, sem áudio ou vídeo de câmera dos participantes. Os trechos finais serão entregues diretamente na conversa para permitir conferência sem depender de outra cópia do manuscrito. Tabela 12, seção 4.14 e Apêndice G mantêm o critério específico de cada fluxo.


## Aprovação do curto prazo e sincronização com LaTeX — 15/10/2026

O usuário aprovou o conteúdo de curto prazo após conferir os seis retoques e os critérios A/B. Essa aprovação é editorial e não corresponde a aprovação da banca, validação empírica adicional ou encerramento dos itens de médio prazo.

- O usuário confirmou consulta à **9ª edição de Sommerville, de 2011**. A chave foi atualizada para `Sommerville2011`, assim como todas as citações e as duas bibliografias; o ISBN herdado da edição anterior foi retirado, sem substituição por identificador presumido.
- O Abstract recebeu a vírgula e a expressão “and with”, alinhando a condição do sorteio com a presença do popup nos dois fluxos.
- A seção 5.2 distingue ausência de configuração registrada nas sínteses de impossibilidade de reconstrução: gravações preservadas poderão auxiliar uma conferência posterior, que ainda não foi realizada.
- A classificação individual das 45 fontes passou da anotação “Natureza:” nas referências para listas por categoria na seção 3.1, com remissões bibliográficas. Essa mudança de apresentação não equivale a revisão completa de ABNT.
- O conteúdo foi sincronizado em dez arquivos editáveis, além da cópia do BibTeX para `latex/bibliografia.bib`. O Markdown permanece a fonte editorial. A rotina de sincronização conserva rótulos, remissões, autores das figuras, dados, tabelas e critérios do estudo.
- A capa institucional foi convertida de EPS para PNG a partir de seus pixels indexados originais, sem redesenho. A folha de aprovação deixou de declarar “Trabalho aprovado” e a data não confirmada de 27/06/2026; passou a indicar submissão à avaliação e data a definir. Os nomes dos membros da banca continuam a definir.
- O agente realizou conferência dirigida de fidelidade: 13 tabelas, seis figuras, sete apêndices e 45 referências, sem perda de parágrafos ou células. Identificou apenas a perda de sobrescrito em números de leis; a conversão foi corrigida para preservar `\textsuperscript`.
- A conferência automática das fontes confirmou: 45 chaves citadas e presentes, nenhuma entrada não citada, nenhum rótulo duplicado, nenhuma remissão interna ausente e bibliografias idênticas.

Permanecem para conferência com o orientador a redação sobre Wesley na Lean Inception, o enquadramento ético/CEP e a guarda dos TCLEs, gravações e dados do Useberry. Não houve alteração no protótipo, substituição de NPS por CES, início das revisões de médio prazo ou commit. A tabela construto → indicador → dado segue dependente da decisão sobre CES.


### Resultado da compilação e conferência visual

Foi gerado `output/pdf/TCC_Avaliacao_Contextual_Curto_Prazo.pdf`, com 79 páginas físicas, pelo modelo institucional existente. A conferência visual percorreu as 79 miniaturas e ampliou páginas de tabelas e referências. Ajustaram-se a posição do texto na capa, a proximidade das figuras com suas seções e a quebra de linha em Figma/Useberry. A última compilação não apresenta estouro de margens, caracteres ausentes, remissões ou citações indefinidas, nem avisos bibliográficos. Permanecem avisos de espaçamento em parágrafos da ficha catalográfica do modelo, sem texto cortado na inspeção visual. A revisão institucional/ABNT integral continua no item 26.

Foram conferidos no PDF os sufixos 2017a/b, 2020a/b/c/d e 2021a/b e a referência “Software Engineering. 9. ed. [...] Addison-Wesley, 2011”. Os arquivos intermediários e as imagens de conferência ficam em `tmp/pdfs/`, fora do controle de versão. `scripts/compilar-tcc.ps1` reúne sincronização, compilação e cópia do PDF final.

**CopySpider:** o novo relatório não foi gerado. A instalação local é uma aplicação gráfica; os controles disponíveis nesta sessão não permitem operar sua interface nativa. O PDF final está pronto para ser analisado nela. O relatório antigo continua associado à versão anterior e não valida este PDF. Não se atribui qualquer percentual ou aprovação de similaridade à versão compilada agora.

SHA-256 do PDF conferido: `8f7b15ef586314afe848e41a5e350e11dff498f84af9d111d7a9bd43cbfce822`.

Até a conclusão da compilação, não havia sido feito commit, publicação ou início das modificações de médio prazo.

### Versionamento do curto prazo — 15/10/2026

O usuário autorizou o commit em uma branch específica antes da conclusão do novo relatório CopySpider. A revisão de curto prazo fica registrada na branch `codex/tcc-curto-prazo`, com o Markdown aprovado, as bibliografias, as fontes LaTeX sincronizadas, a capa e as rotinas de sincronização/compilação. O PDF compilado e os intermediários permanecem como arquivos locais, conforme as regras de exclusão do repositório.

O novo relatório CopySpider continua pendente e será analisado posteriormente. Esse registro não representa aprovação de similaridade, aprovação da banca ou conclusão das revisões de médio prazo. Não foi solicitada publicação da branch no repositório remoto.
