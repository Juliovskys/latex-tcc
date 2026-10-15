# Revisão editorial e normalização do médio prazo

Esta conferência começou pelo Markdown/BibTeX e foi complementada pela transposição ao LaTeX e pela inspeção visual do PDF compilado. O registro dessa etapa está ao final deste documento. A revisão não é certificação normativa institucional.

## Base consultada

Foram consideradas NBR 14724:2024, NBR 6023:2025, NBR 10520:2023, NBR 6024:2012, NBR 6027:2012 e NBR 6028:2021, juntamente com a orientação institucional da BCE/UnB. O material da [BCE sobre trabalhos acadêmicos](https://bce.unb.br/wp-content/uploads/2025/02/ABNT-ATUALIZADO-em-fevereiro-2025.pdf) antecede a revisão de referências de 2025; por isso, também foi consultado o [texto da NBR 6023:2025 disponibilizado pela biblioteca universitária FHO](https://www.fho.edu.br/assets/documentos/FHO_Biblioteca_Referencia_ABNT_6023_2025.pdf). A [BCE mantém atendimento e materiais de normalização](https://bce.unb.br/servicos/servicos-de-referencia/).

## Conferência realizada

- **Identificação:** dois autores e título do Trabalho 1 mantidos; banca e aprovação não são inventadas. O subtítulo é separado do título no Markdown para posterior composição institucional.
- **Resumo/Abstract:** versões coerentes com DSR, CES posterior ao estudo e ausência de superioridade demonstrada; palavras-chave separadas por ponto e vírgula e encerradas por ponto. O resumo permanece em parágrafo único.
- **Seções:** capítulos 1–5; DSR organizada nas seis atividades; apêndices A–L. Numeração progressiva e remissões revistas; sumário e listas paginados gerados no LaTeX.
- **Siglas:** lista em ordem alfabética, com inclusões usadas no texto e retirada de SQLite, que é nome do produto, não uma sigla desenvolvida nesta lista.
- **Quadros/tabelas:** conteúdo predominantemente textual classificado como quadro; dados numéricos da simulação e do estudo permanecem tabelas. Numeração separada: 19 quadros e duas tabelas. Cada um tem identificação, título, fonte e âncora; três figuras atuais e quatro registros históricos possuem identificação e fonte.
- **Figuras:** telas Python atuais separadas do estudo Figma; dados sintéticos identificados. Não se atribuem capturas produzidas nesta atualização ao autor das figuras históricas. Na composição final, a legenda identificadora fica acima da imagem e a fonte abaixo.
- **Citações/referências:** 57 chaves citadas, 57 entradas e 57 referências; ausência de destinos duplicados ou faltantes. Mantidos sufixos de Brasil 2017, GDS 2021 e Lima/Pereira 2020; entidades autoras distintas em 2022 não recebem sufixos artificiais. Preservados DOI, endereços, datas de acesso disponíveis, editores e dados de capítulos.
- **Referências:** ordem alfabética, sobrenomes e autores institucionais padronizados; destaque do título da obra ou periódico conforme o tipo. Legislação inclui veículo e data de publicação; seção e página aparecem onde verificadas. Texto compilado é distinguido da publicação original. DOI de Hevner conferido; endereço DOI duplicado removido; pontos duplos reparados. Normas, relatórios e páginas eletrônicas têm tratamento identificável. Sommerville permanece na 9ª edição de 2011, confirmada pelos autores; Boston e Pearson foram conferidos em registros bibliográficos institucionais, sem atribuir ISBN de outra edição. Locais não identificados permanecem sinalizados, sem inventar cidades.
- **Natureza das fontes:** classificação no método, sem linhas “Natureza:” dentro das referências. Fontes comerciais não são utilizadas como validação do CES ou de benefícios.
- **Data Useberry:** a página consultada não informa data específica de publicação, mas traz copirraite 2026. A referência registra **c2026**, com nota correspondente no BibTeX; não se inventa dia ou mês. O ano não identifica a data da coleta, que foi informada pelos autores. A chamada foi uniformizada como Useberry, c2026.
- **Dados históricos:** questionário e registros F/G mantidos, sem CES retroativo ou alteração dos relatos para favorecer a proposta. Correções de denominação dos instrumentos atuais não reescrevem a coleta histórica.

O verificador `scripts/verificar_manuscrito.py` confere correspondência bibliográfica, vínculos, sequência de tabelas/quadros, destinos de seções e existência de imagens. Ele auxilia a revisão, mas não avalia pertinência científica, similaridade textual ou apresentação visual.

## Conferência prevista para o PDF — histórico do planejamento

Após a avaliação do conteúdo: adaptar a sincronização para quadros e suas listas, ajustar o modelo institucional vigente, gerar elementos pré-textuais, sumário e listas, conferir margens, fontes, espaçamento, paginação, posição de legendas/fontes, quebras, acessibilidade do documento e referências renderizadas. Conferir novamente os sufixos autor-data após o processamento bibliográfico. Não reutilizar o PDF de curto prazo como se contivesse esta revisão.

O novo CopySpider deve incidir sobre o PDF efetivamente compilado dessa versão. Similaridade precisa ser analisada por contexto, fonte e atribuição; o relatório não é substituído por revisão de agente nem há pontuação antecipada nesta rodada.

A conferência após o parecer também uniformizou as chamadas institucionais (ISO, ISO/IEC, IPC NSW e W3C) e os rótulos autor-data na classificação das fontes. A WCAG citada permanece a Recomendação atualizada de 12 de dezembro de 2024; não se afirma que sua primeira publicação ocorreu nesse ano. O catálogo H.6 liga a matriz a 19 métodos reais, cuja existência e correspondência com os hashes da execução são conferidas pelo verificador.

Na segunda rodada, o catálogo passou a 19 testes e a bibliografia a 57 referências, com Fawcett (2006). Foram corrigidos o título da seção 2.4, a redundância de J.1, a nota de chave das rotas administrativas e os dados bibliográficos de Dixon/Cavoukian. O destino final do acervo histórico continua como decisão anterior à transposição.

Após o parecer sobre o pacote v2, foi removida a linha de natureza isolada da referência de Fawcett; a classificação está na seção 3.1, com citação. A nota do Quadro 4 vem depois da fonte. Essas correções editoriais devem ser preservadas no LaTeX e não antecipam a revisão visual do PDF.

Após o parecer sobre a v5, a seção 3.3.1 e o inventário do acervo passaram a usar “desenvolvido pelos autores” e “organizado pelo orientador”. O nome Julio Cesar Gomes de Souza Crispim permanece sem acento; o controle de revisão foi uniformizado. Não houve mudança de referências ou contagem bibliográfica.

## Conferência na transposição para LaTeX

A transposição autorizada incorporou 12 apêndices (incluindo o acervo histórico L), sete figuras, listas separadas de 19 quadros e duas tabelas, legendas/fontes e cabeçalhos de continuação. As 57 referências e suas citações usam chaves BibTeX; os sufixos de Brasil 2017, GDS 2021 e Lima/Pereira 2020 foram harmonizados com a ordem efetivamente gerada pelo estilo. Não se preservaram letras manuais divergentes do BibTeX. A compilação e a revisão visual são registradas em `docs/evidencias/compilacao-medio-prazo.json`; isso não representa certificação normativa institucional. O novo CopySpider permanece pendente.
