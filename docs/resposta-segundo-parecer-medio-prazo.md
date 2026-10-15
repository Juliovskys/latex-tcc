# Resposta ao segundo parecer de médio prazo

Rodada de 15/10/2026. Documento de acompanhamento da revisão em `docs/tcc.md`; não substitui os resultados do estudo nem a avaliação dos autores e do orientador. Não houve nova coleta com participantes, sincronização com LaTeX/PDF ou commit desta rodada.

| Ponto do parecer | Tratamento nesta rodada | Evidência ou limite |
| --- | --- | --- |
| 1 — Plano do item 15 | Acrescentados TV10, protocolo K.1.1 e rastreabilidade. | Episódio por sessão/serviço/etapa; referência declarada independente, inclusive sem alerta; VP/FP/VN/FN; sensibilidade, especificidade e valores preditivos; grade de limiares e separação de participantes entre ajuste e teste. Plano elaborado; coleta, instrumentação e execução pendentes. A classificação anterior que deixava também o plano apenas para longo prazo foi corrigida. |
| 2 — Ausências de CES | Separados registros do contrato atual daqueles legados ou de origem desconhecida. | API e painel expõem `ces_missing_current_contract` e `ces_missing_legacy_or_unknown`. `ces_missing` permanece como total compatível. A versão da pergunta de satisfação identifica o contrato, não comprova exposição ao item. Não há taxa de não resposta. F07 verifica a separação; F05 verifica os legados migrados. |
| 3 — Confirmação do descarte | A prévia passa a incluir resumo das identidades e dos conteúdos dos registros a eliminar. | Token vinculado também a corte e contagens; transação preservada. G12 verifica substituição com mesma contagem e alteração de conteúdo com mesmo ID: ambas exigem nova prévia. Não se declara histórico inviolável ou auditoria independente. |
| 4 — Coordenadas em G04 | Acrescentados envios explícitos com x, com y e com ambos. | Rejeição HTTP 400 verificada; o caso mantém os demais cenários de autorização, interrupção e minimização. |
| 5 — Versão congelada | Continua pendente da avaliação dos autores. | Evidência atual identifica commit-base, alterações locais e hashes dos cinco arquivos testados. Após aprovação: commit/tag estável e nova execução vinculada à versão. O relato do avaliador sobre Linux é evidência externa, não uma execução local nossa. |
| 6 — Fontes CES/e-GovQual | Conferidos os trechos pertinentes, com origem e limites documentados. | [Registro das fontes](evidencias/fontes-primarias-verificadas.md). e-GovQual: Tabela 12, p. 107, e discussão confirmam 21 itens em cópia de terceiros, cruzada com metadados primários. Dixon: slide 72 inspecionado visualmente; possui seis opções visíveis. As sete categorias são assumidas explicitamente como adaptação deste projeto. |
| 7 — Acervo no PDF | Mantido como decisão de fechamento com o orientador. | O vínculo local é apoio à revisão em Markdown. Antes da transposição: decidir reprodução dos registros históricos em anexo com nota ou referência permanente a commit do repositório. Nenhuma referência permanente fictícia foi criada. |
| 8 — Participação de Wesley | Pendência explicitada e preservada. | Conciliar com os registros da equipe e com o orientador; não inferir contagem, participação ou aprovação que os dados disponíveis não documentam. |
| 9 — Seção 2.4 | Título inclui governo eletrônico e e-GovQual; autores explicitados na frase sobre validação. | A validação de Papadomichelaki e Mentzas não é transferida ao CES ou ao protótipo. |
| 10 — J.1 | Eliminada a repetição e mantido o papel complementar da IPC NSW. | A fundamentação LGPD permanece no parágrafo específico; a fonte complementar continua citada. |
| 11 — Quadro 4 | Acrescentada nota sobre todo o prefixo `/api/admin/`. | Todas essas rotas exigem chave; a nota deixa de sugerir proteção exclusiva do dashboard. |
| 12 — Referências | Corrigidos local/editora do livro e descrição da cópia de Cavoukian. | Markdown/BibTeX coerentes. Fontes da conferência no registro bibliográfico desta rodada. |
| 13 — Link do portal | Identificado como “Gestão (atalho da demonstração)”. | Rótulo conferido no navegador local; a chave administrativa continua exigida. |
| 14 — Popup | Seção 4.10 explicita controle no cliente, por `sessionStorage`. | Limpar o armazenamento permite nova exibição; não se atribui ao servidor garantia global de exibição única. |

## Verificação desta rodada

A suíte passou **19 testes locais**, sete de satisfação/CES e doze de governança, em Windows 11, Python 3.12.14 e SQLite 3.53.1, com dados sintéticos e bases temporárias. Os arquivos [de saída](evidencias/verificacao-medio-prazo.txt) e [de metadados](evidencias/verificacao-medio-prazo.json) registram a execução, os horários, o ambiente e os hashes. F07 e G12 são novos; G04 foi ampliado. O catálogo H.6 e a matriz foram atualizados.

O painel e o atalho do portal foram conferidos no navegador. As capturas atuais estão em `docs/figuras/`. O verificador editorial confere 57 referências, 19 quadros, duas tabelas e 11 apêndices, além dos vínculos e da existência dos métodos de teste citados. Os Apêndices F/G históricos foram preservados.

## Antes de congelar e transpor

1. Avaliação pessoal dos autores e conciliação com o orientador sobre Wesley, destino do acervo e questões éticas/guarda já registradas.
2. Congelamento autorizado em commit/tag, nova execução e preservação das evidências vinculadas à versão; conservar também as evidências anteriores.
3. Transposição ao LaTeX e conferência visual completa; então novo CopySpider e avaliação contextual do relatório.

Os planos de calibração, avaliação com cidadãos, gestores e especialistas, segurança e acessibilidade não são apresentados como estudos executados. A revisão está pronta para nova leitura dos autores; não é aprovação definitiva ou declaração de conformidade integral.
