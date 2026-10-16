# Transposição da versão final do conteúdo para LaTeX

Fonte editorial recebida: `TCC_Avaliacao_Contextual_Versao_Final_Markdown.md`, do pacote final aprovado no diálogo. A fonte de trabalho atual é `docs/tcc.md`; a bibliografia estruturada é `docs/referencias-tcc.bib`. A confirmação da redação da seção 3.3.1 e do Apêndice L por Fernando e pelo orientador foi informada por Julio e está registrada em `docs/fechamento-editorial-final.md`.

## Conversão e apresentação

- Citações convertidas para `\cite` e `\citeonline`; chamadas de três autores por extenso, conjunção própria nas chamadas narrativas e caixa mista nas chamadas entre parênteses.
- Nomes institucionais por extenso nas chamadas e entradas correspondentes, preservadas as siglas na lista de abreviaturas.
- Ordenação bibliográfica por autor, ano, título e subtítulo. Os sufixos são gerados pelo BibTeX; os campos de ano não foram adulterados para impor letras. Conferidos Lima e Pereira 2020a–d = módulos 1–4; Brasil 2017a/b = Decreto/Lei; Government Digital Service 2021a/b = Measuring/Using.
- Metadados já disponíveis de DOI passam a gerar endereço quando faltava URL. Incluídas as datas de conferência das quatro referências eletrônicas que não as tinham. A conferência de Shih e Fan foi bibliográfica, pelo registro Crossref, sem alegar nova leitura do artigo integral.
- Preservados os sobrescritos e convertidos os símbolos matemáticos. A compilação usa Tectonic, baseado em XeTeX; o projeto também identifica XeLaTeX como motor.
- Remissões a quadros, tabelas, figuras, seções e apêndices convertidas para rótulos e referências. Sumário e listas gerados pelo modelo, sem reproduzir no corpo as listas manuais do Markdown.
- Contador e lista próprios para quadros; cabeçalhos e legendas de continuação em quadros e tabelas multipágina; fontes convertidas para `\fonte`, dentro do último rodapé da tabela para impedir que fiquem isoladas na página seguinte.
- Modelo UnB/FCTE em A4, fonte principal de 12 pontos, margens superior/esquerda de 3 cm e inferior/direita de 2 cm, entrelinhas de 1,5 no corpo e fontes reduzidas nas exceções. Links preservados em preto.
- Ajustado o espaço adicional entre parágrafos dos apêndices. Os quatro campos do feedback em B.3 são apresentados em linha, com as mesmas palavras e ordem, para evitar uma página contendo apenas o fim desse apêndice.
- Preservada a indicação `c2026` de Useberry, correspondente ao copyright informado no manuscrito. Protegidas as grafias de nomes próprios e siglas nos títulos bibliográficos; substituídas as palavras-chave do modelo nos metadados pelas do Resumo.
- Uniformizadas em maiúsculas as entidades na lista de referências, mantendo a caixa mista nas chamadas. O Quadro 7 e a seção H.2 começam em página própria para manter os Quadros 7 e 14 inteiros, com fonte e cabeçalho.

## Localizadores e arquivos

Os caminhos apresentados no texto seguem o repositório: `docs/figuras/` e `docs/evidencias/`. Os links das evidências usam o commit permanente `d24af5d8ccfa088c7857983fe4d24b08af5337b0`, que contém os arquivos e o acervo já publicado. O commit-base da execução registrada é `935050f9ea7ffa443a1742ec956776762d756090`, conforme seu JSON. Esses identificadores não são apresentados como congelamento das novas fontes editoriais locais.

As três imagens atuais foram copiadas byte a byte do pacote final para arquivos `*-final.jpg`. Os quatro registros históricos permanecem no acervo original e não são reproduzidos no PDF. Os dados históricos dos participantes e os registros dos testes não foram recriados. O protótipo e seus arquivos testados permanecem com os hashes da execução já registrada; não houve nova execução de testes do protótipo nesta transposição.

## Conferência reproduzível

```powershell
.\scripts\compilar-tcc.ps1 -Python python -Pandoc pandoc -Tectonic tectonic
python scripts/verificar_manuscrito.py
python scripts/verificar_latex.py
```

O verificador confere 57 referências, 19 quadros, duas tabelas, três figuras e 12 apêndices; chaves entre Markdown, LaTeX e BBL; sufixos; numeração; remissões; listas; ausência de HTML residual e do indicador excluído; destinos internos do PDF; ausência de links locais inacessíveis; identidade do PDF e hashes das fontes. O resultado está em `docs/evidencias/compilacao-final.json`. Eventuais `Underfull` são avisos de distribuição do espaço e exigem conferência visual; glifos ausentes, destinos indefinidos e caixas que ultrapassem as margens impedem a aprovação automática.

O PDF definitivo tem 107 páginas. O pacote `output/latex/TCC_Avaliacao_Contextual_Fontes_LaTeX_Final.zip` contém 32 arquivos, incluindo a ficha, e foi compilado em pasta independente; o texto extraído de cada página coincide com o do PDF entregue. Os hashes do pacote e do PDF estão em `docs/evidencias/verificacao-pacote-latex-final.json`. O parecer independente do agente está em `docs/parecer-transposicao-final.md`.

## Fontes institucionais consultadas para a apresentação

- [Engenharia de Software/UnB: TCC](https://software.unb.br/tcc/), com acesso ao regulamento aplicável.
- [Resolução do Conselho da FGA n.º 0002/2022](https://sei.unb.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=8652554&id_orgao_publicacao=0): regulamento de TCC e adoção das normas técnicas.
- [BCE/UnB: serviços de referência e modelos](https://bce.unb.br/servicos/servicos-de-referencia/).
- [Biblioteca Central/Ufes: normalização](https://biblioteca.ufes.br/manuais-de-normalizacao), com guia atualizado de apresentação, citações e referências.

Essas fontes orientam a conferência de apresentação e não foram acrescentadas artificialmente ao referencial científico do TCC.

## Fechamento

A revisão visual e a revisão por agente incidem sobre as versões identificadas nos respectivos registros. A revisão por agente é uma conferência adicional e não substitui banca, revisão institucional, avaliação humana do protótipo ou parecer jurídico.

Em 16 de outubro de 2026, foi incorporada a ficha catalográfica fornecida por Julio no arquivo `file (1).pdf`. A página vetorial completa está em `latex/pretextuais/ficha-catalografica.pdf`; sua estrutura PDF foi normalizada para inclusão no LaTeX, com aparência comparada pixel a pixel com o arquivo recebido. Os campos dos membros convidados da banca e da data de aprovação ficam em branco, conforme a solicitação de fechamento; o orientador conhecido permanece identificado.

O relatório CopySpider recebido foi analisado: dez comparações com semelhança baixa, oito com agrupamento moderado, uma com agrupamento baixo e uma com agrupamento nulo. As marcações examinadas se concentram em referências, textos institucionais e duas enumerações conceituais atribuídas às fontes. Cinco candidatos tiveram falhas de download/conversão, e o trabalho separado de Wesley não consta entre os comparados. Trata-se de leitura do relatório fornecido pelo usuário, sem nova execução do CopySpider. O PDF a que ele se refere foi preservado em `output/pdf/historico/TCC_Avaliacao_Contextual_Final_CopySpider_2026-10-16.pdf`; a inclusão da ficha e a retirada dos preenchimentos provisórios da banca são posteriores à análise.
