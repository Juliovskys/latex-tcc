# Resposta ao parecer sobre o pacote v2 de médio prazo

O parecer recebido considera a versão aprovável e relata 19 testes aprovados em Linux. Essa execução é evidência externa do avaliador, não uma execução dos autores ou deste agente. Esta rodada modifica apenas documentos; o código, os testes e suas evidências locais anteriores permanecem identificados pelos mesmos hashes.

| Ponto | Tratamento | Situação |
| --- | --- | --- |
| 1 — Linha isolada na referência Fawcett | Removida a linha “Natureza: literatura científica.” da lista de referências. | Corrigido. |
| 2 — Classificação de Fawcett na seção 3.1 | Incluído o artigo como literatura científica sobre matriz de confusão, com citação vinculada à referência existente. | Corrigido; sem nova entrada bibliográfica. |
| 3 — Retornos e abandono em K.1.1 | Definidos operacionalmente e incluídos no plano TV10 e na matriz por episódio. Retorno é transição de página distinta para página já visitada na mesma etapa; recarga da página corrente não conta. Abandono exige encerramento voluntário com desistência explicitamente indicada antes do sucesso da tarefa. | Plano detalhado; instrumentação e execução continuam futuras. |
| 4 — Nota do Quadro 4 | Fonte posicionada imediatamente após o quadro; nota sobre chave administrativa vem depois. | Corrigido no Markdown; preservar a ordem na transposição. |
| 5 — Versão do contrato deduzida da satisfação | Mantido o contrato atual, com a limitação já documentada. | Campo próprio de versão do formulário é evolução futura; nenhuma mudança de código nesta rodada. |
| 6 — Redação sobre Dixon | Mantida a distinção entre seis opções visíveis naquele slide e sete categorias da adaptação local. | Não se define o CES 2.0, em geral, como escala de seis pontos. |
| 7 — Fechamento | Preservadas as pendências de revisão dos autores/orientador, commit/tag, destino do acervo, participação de Wesley, LaTeX e CopySpider. | Sem commit, transposição ou resultado empírico novo nesta rodada. |

## Delimitação da calibração

Retornos recebem a grade inicial R em {1, 2, 3}; abandono é condição binária confirmada. Os quatro sinais — cliques, duração, retornos e abandono — serão avaliados separadamente e em combinações previamente declaradas, na mesma unidade de episódio e contra a referência de dificuldade colhida independentemente. Mantêm-se VP/FP/VN/FN, métricas e separação por participante entre ajuste e teste.

Abandono só fica disponível no encerramento e será analisado retrospectivamente. Não é apresentado como gatilho capaz de antecipar a desistência. Ausência de fim, desconexão, inatividade ou limite de tempo não são automaticamente abandono. Falta de registro ou confirmação gera condição indeterminada, com denominadores e exclusões explícitos; comparações entre candidatos usam episódios classificáveis em comum.

## Verificação

O verificador do manuscrito foi executado nesta rodada: 57 referências, 19 quadros, duas tabelas e 11 apêndices, com vínculos, figuras, catálogo de testes e hashes da evidência local consistentes. Os Apêndices F/G foram comparados com a versão anterior e preservados.

Não se repetiu a suíte funcional: nenhum dos cinco arquivos de implementação/teste identificados na evidência foi alterado. O registro local existente continua documentando seus 19 testes aprovados em Windows. A revisão documental não acrescenta validação com pessoas ou aprovação de normalização/PDF/similaridade.
