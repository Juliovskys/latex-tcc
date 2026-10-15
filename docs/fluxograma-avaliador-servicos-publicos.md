# Fluxo do protótipo atual

Este fluxo descreve a aplicação Python, não as sessões históricas Figma/Useberry. Duração é informada à API, com envio simulado na demonstração; não há cronômetro automático. Indicadores não comprovam dificuldade ou impacto. O painel e os controles têm alcance local.

```mermaid
flowchart TD
    A["Cidadão acessa página simulada"] --> P{"Autoriza telemetria nesta aba?"}
    P -- Não --> V["Navegar sem telemetria; feedback voluntário disponível"]
    P -- Sim --> B["Cliques instrumentados e duração informada; contexto mínimo"]
    B --> C["API verifica autorização e regra vigente por serviço"]
    C --> E{"Regra de acionamento satisfeita?"}
    E -- Não --> B
    E -- Sim --> G["Alerta: indício comportamental com versão da configuração"]
    G --> H["Sugestão de redirecionamento quando aplicável"]
    G --> I["Convite opcional conforme condição específica"]
    I --> J{"Deseja avaliar?"}
    J -- Não --> V
    J -- Sim --> K["Satisfação; atributos; CES opcional 1–7; comentário opcional"]
    V -- Se deseja avaliar --> K
    K --> L["API valida e armazena resposta e versões dos itens"]
    L --> M["Painel com chave: indicadores, denominadores, ausências e distribuição"]
    M --> N["Interpretação contextual: hipótese a investigar"]
    N --> O["Ação, papel responsável, prazo e retrato inicial"]
    O --> Q["Acompanhamento: situação, nota e novo retrato; sem inferência causal"]
    R["Gestão: parâmetros, justificativa e nova versão"] --> C
    S["Privacidade: interromper coleta"] --> V
    T["Gestão: retenção com prévia e execução manual"] --> M
```

Requisitos e critérios estão nos Apêndices H–K de [tcc.md](tcc.md). A versão `.tex` deste fluxograma é histórica e não acompanha automaticamente o Markdown; será reconciliada na transposição aprovada ao LaTeX.
