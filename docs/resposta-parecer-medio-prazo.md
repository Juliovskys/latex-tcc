# Tratamento do parecer independente de médio prazo

Registro da primeira rodada. A atualização posterior, com 19 testes e tratamento do segundo parecer, está em [resposta-segundo-parecer-medio-prazo.md](resposta-segundo-parecer-medio-prazo.md). Os números abaixo descrevem a execução daquela rodada.

O parecer recebido avaliou texto colado e declarou não ter acesso ao código, aos testes ou às correções integrais do professor. Seus apontamentos foram confrontados com os arquivos locais. O resultado abaixo documenta as alterações; não representa aprovação independente da nova redação.

| Ponto do parecer | Tratamento nesta rodada |
| --- | --- |
| 1 — Execução e voz de revisão | Seção 4.19 identifica execução automatizada local assistida por agente, em 15/10/2026, com horários, ambiente, saída e hashes dos arquivos testados. Não se atribui execução manual aos autores. |
| 2 — C6 e contrato | A versão local já tinha C6 corrigido. A limitação foi explicitada: novas entradas rejeitam os campos; registros históricos podem conservá-los. |
| 3 — Requisitos como etapa futura | Resíduo de 4.5 substituído por remissão aos Apêndices H/I. |
| 4 — Rastreabilidade genérica | Quadro 15 identifica componentes/rotas e remete a F01–F06/G01–G11. O Quadro 16 lista arquivos, classes e métodos reais; cobertura parcial é explicitada. |
| 5 — Relatório histórico versus testes atuais | Inspeção histórica sem relatório completo separada da execução automatizada atual com saída durável. |
| 6 — Origem do CES | Incluídos o livro de 2013 e a apresentação primária de Dixon/CEB de 2016, cujo slide 72 mostra CES 2.0. A referência de 2010 não é usada como origem da formulação atual; SurveyMonkey passa a apoio complementar. Metadados HBR completados. |
| 7 — CES durante a jornada | Risco de interpretar tarefa concluída explicitado em 2.7 e no piloto K.1. A redação aprovada não foi alterada sem avaliação de compreensão. |
| 8 — Elo de governo digital | e-GovQual acrescentado entre E-S-QUAL e os instrumentos brasileiros, com escopo, dimensões e limite de transferência. |
| 9 — Privacidade | Acrescentados art. 6º e art. 46, § 2º da LGPD, além de Cavoukian na versão revisada em 2011, originalmente publicada em 2009. A ficha australiana permanece complementar. |
| 10 — Figuras de concepção | Quatro arquivos originais inventariados em `acervo-lean-inception.md`, com remissão no Apêndice A. Sua redação histórica não é reproduzida como especificação atual nem apresentada como prova suficiente de execução da oficina. |
| 11 — Endpoints | Apêndice C.1 passa a remeter ao inventário único do Quadro 4 e aos contratos do protótipo. |
| 12 — Chamadas institucionais | Uniformizadas por siglas definidas; Useberry citado com a indicação de copirraite c2026. |
| 13 — Pontos duplos | Corrigidos nas referências, preservando iniciais. |
| 14 — Legislação | Incluídos DOU, local e datas; seção/página onde confirmadas; textos compilados distinguidos das publicações originais. Não foram inventados dados ainda não identificados. |
| 15 — Classificação das fontes | Rótulos autor-data uniformizados, incluindo as novas fontes. |
| 16 — Metadados | DOI de Hevner confirmado; Sommerville com Boston/Pearson; duplicação DOI/URL retirada. A WCAG permanece a atualização de 12/12/2024, sem confundir com a primeira publicação. |
| 17 — Repetições | Redundância da visão do produto e espaçamento revistos; distinções necessárias entre concepção, construção e avaliação preservadas. |
| 18 — Recorte ISO | Quadro 17 passa a indicar subcaracterísticas e prioridades, distinguindo avaliação imediata e planejada. |
| Ressalva sobre protocolos | Piloto de compreensão com meta de cinco cidadãos; cinco gestores de pelo menos dois contextos; quatro perfis especialistas. São metas propostas de planejamento, sem participantes recrutados. O estudo confirmatório exige premissas e cálculo amostral prévios, ainda não concluídos. |

## Conferência técnica

Os 17 casos passaram em 15 de outubro de 2026, em Windows 11, Python 3.12.14 e SQLite 3.53.1. A [saída completa](evidencias/verificacao-medio-prazo.txt) e os [metadados/hashes](evidencias/verificacao-medio-prazo.json) identificam o objeto testado. O commit-base é `dee5007275de3370a7652f5d8f5ac079e860ff50`, com alterações locais: não se apresenta esse commit como se já contivesse a revisão.

O catálogo de métodos é confrontado com o código por `scripts/verificar_manuscrito.py`. Passar esses casos não demonstra benefício, validade do CES, conformidade integral ou cobertura de todos os critérios. Não foram produzidos novos dados de participantes.

## Fontes e decisões verificadas

- e-GovQual: [artigo dos autores](https://doi.org/10.1016/j.giq.2011.08.011), 2012, 29(1), 98–109; não aplicado integralmente neste protótipo.
- CES: [apresentação de Dixon/CEB](https://csl.wpcarey.asu.edu/sites/g/files/litvpz1051/files/2023-10/CTS_Effortless-Experience_MattDixon_2016.pdf), slide 72; [metadados editoriais do livro de 2013](https://www.penguinrandomhouse.com/books/312730/the-effortless-experience-by-matthew-dixon/). Não se afirma ter validado ou reproduzido o estudo comercial.
- Privacy by Design: [documento de Cavoukian](https://www.sfu.ca/~palys/Cavoukian-2011-PrivacyByDesign-7FoundationalPrinciples.pdf) identifica revisão de janeiro de 2011 e publicação original em agosto de 2009. Cita-se a versão efetivamente consultada.
- O [endereço curto do IPC NSW](https://www.ipc.nsw.gov.au/fact-sheet-privacy-design) redireciona ao caminho `/resources/fact-sheet-privacy-design` já usado; o apontamento de URL incorreta não foi confirmado.
- LGPD: [texto oficial](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); ligação específica aos requisitos, sem declaração de conformidade jurídica.

## Limites mantidos

A nova redação ainda depende de avaliação dos autores e do orientador. O acervo da Lean Inception contém formulações que exigem reconciliação factual com os registros da equipe. Não se inventou uma ata ou cronologia para resolver isso. Amostra confirmatória, coleta humana, calibração e avaliações externas seguem futuras. Normalização visual, transposição ao LaTeX, PDF e CopySpider permanecem pendentes. Não houve commit ou publicação desta rodada.
