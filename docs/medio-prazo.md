# Consolidação do médio prazo

**Versão para avaliação em Markdown.** Branch `docs/tcc-medio-prazo`. O texto, o BibTeX, o protótipo e o LaTeX foram atualizados; o PDF da revisão de médio prazo foi compilado. Não houve nova coleta com pessoas. Esta revisão ainda depende da leitura dos autores e do orientador e de novo CopySpider sobre o PDF compilado.

## Atendimento aos pedidos do professor

A referência é o texto integral de correções fornecido pelos autores. A orientação inversa do item 2 e o item 3 pertencem ao trabalho de Wesley e não integram este escopo.

| Item | Entrega nesta consolidação | Situação e evidência |
| --- | --- | --- |
| 2 — Reescrita e retirada do indicador anterior | Manuscrito, formulário, agregações e documentação ativa passam a satisfação, atributos e CES. | Implementado. Menções técnicas restantes limitam-se à detecção/rejeição do contrato antigo e à migração com cópia histórica; não são instrumento ativo. Figuras antigas de produto saíram do manuscrito atual. |
| 5 — Construto → indicador → dado | Quadro 3 distingue satisfação, qualidade percebida, facilidade, comportamento, conclusão e comentário, incluindo origem e limites. | Elaborado depois da decisão sobre CES; não é modelo de mensuração validado. |
| 6 — Qualidade eletrônica | Seção 2.4: E-S-QUAL/E-RecS-QUAL, dimensões, escopo e limites; progressão para serviços públicos e BRASP. | Referencial ampliado com e-GovQual em 2012; não se afirma aplicação integral das escalas. |
| 7 — CES | Pergunta e escala aprovadas pelos autores; CES 2.0 fundamentado também em fonte primária de Dixon; orientação, versões, ausência, média e distribuição. | Implementado e verificado tecnicamente; compreensão/validade com cidadãos pendentes. |
| 8 — Serviço digital | Seção 2.1.1: software, interação, percepção e resultado efetivo. | Distinção incorporada; conclusão no Figma não comprova resultado real. |
| 9 — DSR | Capítulo 3 organizado em problema, objetivos/requisitos, design/desenvolvimento, demonstração, avaliação e comunicação. | Lean Inception situada na concepção. Formalização posterior ao estudo histórico explicitada. |
| 10 — Requisitos | Apêndice H: 12 RF, 12 RNF, 10 regras, seis histórias e critérios de aceitação. | Especificado; estados de implementação e critérios futuros identificados. |
| 11 — Rastreabilidade do software | Quadro 15: necessidade → requisitos → componente → critério → evidência. | Elaborada com rotas, módulos e identificadores dos 19 testes no catálogo H.6; separada da matriz conceitual do Quadro 3. |
| 12 — ISO/IEC 25010:2023 | Apêndice I: oito características pertinentes, justificativas, requisitos e evidências; delimitação de safety. | Modelo adotado como referência; não há certificação ou avaliação integral. |
| 13 — Plano V&V | Dez frentes no Apêndice I: funcional, API, recuperação, desempenho, segurança, cidadãos, acessibilidade, gestores, especialistas e calibração. | Plano redigido. Subconjunto técnico local executado; execução ampla continua no longo prazo. |
| 14 — Limiares configuráveis | Edição administrativa, justificativa, versão esperada, histórico, conflito 409 e preservação na reinicialização. | Implementado e testado; alertas guardam versão. Parâmetros seguem sem calibração científica. |
| 15 — Plano de calibração | TV10 e K.1.1: episódio, cliques, duração, retornos e abandono confirmado; referência declarada independente, variação dos limiares, VP/FP/VN/FN, métricas e separação por participante entre ajuste e teste. | Plano elaborado nesta rodada; instrumentação, base rotulada e execução continuam pendentes no longo prazo. |
| 17 — Privacy by Design/LGPD | Requisitos e Apêndice J; escolha/interrupção, minimização, aviso, chave e descarte manual com prévia. | Parte implementada e testada. Base legal, guarda de cópias, identidades individuais e implantação externa dependem de preparação institucional. |
| 18 — Acessibilidade | Requisitos, critérios WCAG 2.2 e plano; rótulos, agrupamentos, estados, foco e ajuste de formulário estreito. | Plano formalizado e ajustes locais realizados; avaliação abrangente e conformidade não declaradas. |
| 19 — Três perspectivas | Apêndice K com protocolos separados de cidadãos, gestores e especialistas independentes. | Planejado; recrutamento e execução não realizados nesta revisão. |
| 24 — Papel do painel | Dado → interpretação → ação/responsável/prazo → acompanhamento, com retrato inicial e histórico. | Implementado e conferido em base sintética. Utilidade real e efeito de melhorias não avaliados. |
| 26 — Normalização | Revisão editorial de siglas, palavras-chave, referências, remissões, fontes, figuras, quadros e tabelas; relatório próprio. | Conteúdo revisado. Paginação, sumário/listas, margens e tipografia exigem conferência no futuro PDF. Não é aprovação ABNT integral antecipada. |

## Decisão sobre CES e satisfação

CES opcional: **“Foi fácil realizar o que eu precisava nesta etapa do serviço”**, concordância 1–7; maior resposta indica maior facilidade percebida da etapa. Versão `ces-facilidade-etapa-v1`. Não mede esforço de preencher o formulário, esforço objetivo ou efetividade real. Ausências permanecem nulas; média sem resposta válida fica indisponível; distribuição e denominador acompanham o resumo. Não há ponto de corte universal.

Satisfação: **“Qual é a sua satisfação com esta etapa do serviço?”**, cinco categorias de muito insatisfeito(a) a muito satisfeito(a), versão `satisfacao-etapa-v1`. Notas anteriores ficam preservadas, sem receber retrospectivamente essa versão. Os dois itens são posteriores ao estudo de junho e ainda requerem avaliação com cidadãos.

## Verificações e limites

- **19 testes automatizados passaram**, em Windows, Python 3.12.14 e SQLite 3.53.1, com bases temporárias e dados sintéticos. Comando reproduzível em `prototype-api/README.md`.
- Saída e metadados da execução atual estão em `docs/evidencias/verificacao-medio-prazo.txt` e `.json`.
- Conferência no navegador: envio de satisfação/CES, atualização dos indicadores, criação/acompanhamento de ação, configuração versão 2, escolha/interrupção de telemetria e dispensa dos avisos. O formulário também foi conferido em 320 pixels de largura; isso não é auditoria de acessibilidade.
- Revisão de agente em leitura: inconsistências de sessão canônica e linguagem diagnóstica foram corrigidas; fechamento do convite foi acrescentado. O parecer não certifica segurança ou acessibilidade e não equivale a especialista humano.
- Verificação editorial reproduzível em `scripts/verificar_manuscrito.py`: 57 referências, 19 quadros, duas tabelas e 12 apêndices; chaves, destinos e imagens conferidos. Os Apêndices F/G preservam o estudo histórico.
- Bases e capturas de demonstração não acrescentam resultados aos oito casos Figma/Useberry. Nenhum CES foi atribuído retroativamente, e a simulação antiga permanece identificada como não reproduzida.

## Avaliação e etapas seguintes

1. Avaliação pessoal dos autores e revisão de conteúdo pelo orientador, usando `docs/tcc.md` e este quadro de atendimento.
2. Ajustes decorrentes dessa avaliação e nova conferência independente, se necessária.
3. Sincronização com LaTeX, com ambientes/lista de quadros, legendas, sumário, paginação e referências do modelo institucional; revisão visual do PDF completo.
4. Novo CopySpider sobre o PDF dessa versão e análise contextual dos trechos sinalizados.
5. Commit/push da versão aprovada, quando solicitado pelos autores.

Continuam no longo prazo: calibração com base rotulada (item 15), execução ampla de V&V, acessibilidade e três perspectivas, teste das hipóteses (22) e heurística externa (23). Assuntos com o orientador: destino do acervo histórico, enquadramento ético/CEP, TCLE, exportação e guarda de dados/gravações Useberry. A participação parcial de Wesley foi esclarecida pelos autores e registrada na seção 3.3.1 e no Apêndice A.4. Não há declaração de aprovação ética ou de impacto em produção.

## Ajustes após o parecer independente

Consulte [resposta-parecer-medio-prazo.md](resposta-parecer-medio-prazo.md). Foram acrescentados e-GovQual, fonte primária do CES 2.0, princípios de Cavoukian, artigos específicos da LGPD, rastreabilidade até métodos de teste, evidência durável da execução, recorte de subcaracterísticas ISO e roteiros/metas exploratórias dos protocolos. O estudo confirmatório ainda exige definir premissas e calcular sua amostra antes de executar. O acervo visual histórico tem inventário separado; suas expressões antigas não descrevem o instrumento atual.

## Ajustes após o segundo parecer

Consulte [resposta-segundo-parecer-medio-prazo.md](resposta-segundo-parecer-medio-prazo.md). Foram acrescentados o plano TV10, a separação de ausências CES por contrato, a vinculação do descarte ao conteúdo/identidade dos registros e os casos F07/G12. G04 agora envia explicitamente coordenadas x/y inválidas. A execução atual passou 19 testes. A fonte de Dixon foi conferida visualmente: seis opções visíveis; as sete categorias deste projeto permanecem uma decisão local. O congelamento em commit/tag, o destino final do acervo e a conciliação da participação de Wesley continuam pendentes de revisão dos autores/orientador.

## Ajustes após a avaliação do pacote v2

Consulte [resposta-parecer-v2-medio-prazo.md](resposta-parecer-v2-medio-prazo.md). Foram corrigidas a referência e a classificação de Fawcett e a posição da nota do Quadro 4. K.1.1 e TV10 agora incluem definições operacionais de retornos e abandono confirmado, com métricas por episódio e tratamento de dados indeterminados. Abandono será analisado retrospectivamente, não como gatilho antecipado. Esta rodada é documental: os cinco arquivos de implementação/testes conservam os hashes da execução local de 19 casos. Não houve nova execução funcional, coleta ou mudança de código.

## Ajuste após a avaliação do pacote v3

O parecer considera a v3 aprovável, sem pendência obrigatória. A [resposta ao parecer v3](resposta-parecer-v3-medio-prazo.md) registra o ajuste recomendado: somente cliques, duração e retornos entram na seleção do gatilho; abandono confirmado permanece em matriz própria de associação retrospectiva. A instrumentação e a execução continuam planejadas. Não houve alteração de código ou nova execução funcional. As pendências de fechamento permanecem.

## Esclarecimento dos autores sobre a concepção compartilhada

Julio esclareceu que o orientador organizou o tema amplo em dois recortes: um desenvolvido por Julio e Fernando e outro por Wesley. Parte das atividades de concepção e a origem dos artefatos foram compartilhadas. Wesley participou parcialmente, sem participar de toda a Lean Inception, e não integrou a discussão com Felipe, Lucas, Diassis e Bruno. Fernando produziu as figuras. A seção 3.3.1, o Apêndice A.4 e o inventário do acervo foram harmonizados com essas informações, substituindo a afirmação de que a colaboração de Wesley se restringira ao tema de seu próprio trabalho.

A pendência factual sobre essa participação foi esclarecida. Não se atribui ao orientador aprovação desta nova redação. A autoria deste TCC permanece de Julio e Fernando. O parecer favorável sobre a v4 é anterior a esse esclarecimento; a nova redação deve integrar a avaliação pessoal dos autores e a leitura pelo orientador. Não houve alteração de código, teste, figura histórica ou dados dos participantes. O destino do acervo no PDF permanece uma decisão de fechamento.

## Ajustes após o parecer sobre a v5 e checklist de fechamento

A [resposta ao parecer v5](resposta-parecer-v5-medio-prazo.md) registra a uniformização de Julio e a retirada da redundância na seção 3.3.1 e no inventário do acervo. A informação sobre a colaboração parcial veio de Julio. O esclarecimento factual foi incorporado; a confirmação da redação por Fernando e pelo orientador permanece recomendada antes do congelamento.

- [ ] Obter e registrar a confirmação de Fernando e do orientador sobre a redação da divisão dos recortes e da concepção parcialmente compartilhada. Não há confirmação deles registrada nesta revisão.
- [x] Destino dos registros visuais históricos: incluídos no Apêndice L, com contextualização, conforme a autorização de Julio para a transposição.
- [ ] Após aprovação dos autores, congelar a versão em commit/tag autorizado e executar novamente as verificações com evidência vinculada à versão.
- [x] Transpor o conteúdo aprovado para LaTeX e revisar visualmente o PDF completo.
- [ ] Gerar novo CopySpider e interpretar os trechos sinalizados com o orientador, considerando a origem compartilhada dos artefatos com o trabalho de Wesley. Se houver uma versão identificável desse trabalho, conferir o conteúdo pertinente e os dados bibliográficos antes de inserir eventual citação na seção 3.3.1. Não foi criada referência sem esses dados, nem estimado percentual de similaridade.

Esta rodada modifica apenas documentos. Não equivale a confirmação de Fernando ou do orientador, nem altera o alcance da evidência local de 19 testes ou do estudo histórico com oito participantes.

## Transposição autorizada para LaTeX

Julio autorizou a transposição e o commit na branch `docs/tcc-medio-prazo`. O conteúdo consolidado do arquivo local foi usado como fonte. Os quatro registros históricos de autoria de Fernando foram incluídos no Apêndice L, com nota de contextualização e imagens preservadas. O manuscrito passa a 12 apêndices e sete figuras; mantém 19 quadros, duas tabelas e 57 referências. As confirmações de Fernando/orientador não foram presumidas, e o novo CopySpider continua pendente.

O sincronizador preserva as listas/counters de quadros e tabelas, legendas/fontes, referências e remissões, e harmoniza os sufixos de ano exibidos com a saída do BibTeX. A derivação local do estilo bibliográfico mantém os mesmos sufixos nas citações e na lista de referências, com origem e licença preservadas. Os registros históricos F/G e as imagens originais não foram alterados. A conferência da compilação está em `docs/evidencias/compilacao-medio-prazo.json`.
