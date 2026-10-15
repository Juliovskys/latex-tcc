# Transposição do médio prazo para LaTeX

Julio autorizou a transposição e o commit na branch `docs/tcc-medio-prazo`. Foi utilizado o arquivo local consolidado de `docs/tcc.md`, com a redação corrigida da seção 3.3.1 e a exclusão do abandono da escolha do gatilho em K.1.1. Mensagens coladas de versões anteriores não foram usadas como fonte.

## Resultado

- LaTeX e BibTeX sincronizados com o Markdown.
- PDF com 112 páginas físicas, 57 referências, 19 quadros, duas tabelas, sete figuras e 12 apêndices.
- Apêndice L com os quatro registros históricos de Fernando, sem alteração das imagens, com contextualização sobre o instrumento e as alegações anteriores.
- Listas separadas de quadros, tabelas e figuras; lista de apêndices com páginas e vínculos; sumário paginado.
- Identificação acima das imagens e fontes abaixo; quadros multipágina com cabeçalhos e indicação de continuação.
- Rótulos, remissões, citações e referências resolvidos. O localizador “slide 72” de Dixon foi preservado.
- Sufixos de ano harmonizados com a saída bibliográfica; a derivação `latex/abntex2-alf-tcc.bst` preserva os avisos de licença e identifica sua origem e modificação. Não foram introduzidas letras no campo de ano do BibTeX para forçar ordenação.

O arquivo `output/pdf/TCC_Avaliacao_Contextual_Medio_Prazo.pdf` é o PDF desta etapa. PDFs e intermediários continuam fora do controle de versão conforme a regra do repositório; as fontes e os registros de verificação são versionados.

## Conferência

O PDF completo foi renderizado para inspeção visual, com contatos de todas as páginas e ampliações das páginas de listas, referências, quadros extensos e registros históricos. Foram corrigidos o afastamento entre títulos e imagens históricas, excessos de largura nos quadros/sumário e destinos duplicados das figuras. O log final não contém referências indefinidas, glifos ausentes ou caixas excedendo as margens. Permanecem avisos não críticos de espaçamento em caixas (`Underfull`), conferidos visualmente.

`scripts/verificar_latex.py` confere chaves entre Markdown/LaTeX/BBL, rótulos, numeração, listas, sufixos nas referências, bibliografia copiada, identidade do PDF entregue e hashes das fontes. `docs/evidencias/compilacao-medio-prazo.json` registra o resultado e o commit das fontes; a comparação com o Git desconsidera apenas a diferença LF/CRLF nos arquivos de texto. O SHA-256 do PDF identifica o artefato local.

Os Apêndices F/G e os quatro PNGs históricos foram comparados com o pacote v6 e preservados. Nenhuma nova coleta ou resultado empírico foi acrescentado. O teste de interface histórico continua separado das verificações técnicas da API.

As verificações técnicas da versão congelada são registradas em `docs/evidencias/verificacao-medio-prazo.txt` e `.json`. O registro anterior foi preservado com o sufixo `pre-congelamento`; a execução Linux descrita pelos avaliadores permanece evidência externa.

## Reprodução

Com Python, Pandoc e Tectonic disponíveis, na raiz do projeto:

```powershell
.\scripts\compilar-tcc.ps1 -Python python -Pandoc pandoc -Tectonic tectonic
python scripts/verificar_manuscrito.py
python scripts/verificar_latex.py
python scripts/registrar_verificacao.py
```

As dependências adicionais de conferência do PDF incluem `pypdf`; não são necessárias à execução do protótipo e de seus testes, que usam a biblioteca padrão. A conferência automática não substitui inspeção visual quando o conteúdo ou a diagramação mudarem.

## Continuidade

O novo CopySpider deve ser executado sobre este PDF e interpretado com o orientador, considerando a concepção compartilhada com o trabalho de Wesley. A confirmação recomendada de Fernando/orientador sobre a redação permanece no checklist, sem aprovação presumida. A transposição e a revisão visual não são certificação normativa institucional nem execução dos estudos de longo prazo.
