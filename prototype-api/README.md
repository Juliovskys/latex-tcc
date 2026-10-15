# Protótipo local de avaliação contextual

Demonstração em Python/SQLite para associar contexto de navegação a satisfação, atributos, facilidade percebida e comentário. O estudo histórico de oito participantes ocorreu no Figma/Useberry e não avaliou esta implementação com CES, configurações e ações.

## Executar

Requer Python 3.10 ou superior, somente biblioteca padrão. Ambiente verificado: Windows, Python 3.12.14, SQLite 3.53.1. Na raiz do repositório:

```powershell
$env:AVALIADOR_ADMIN_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
python prototype-api/server.py
```

A chave fica na variável de ambiente da sessão do terminal. Use seu valor no campo “Chave de administração” em `http://127.0.0.1:8080/`. A inicialização recusa ausência de chave. Não publique a chave nem a inclua em arquivos versionados. A interface mantém a chave apenas em memória; encerramento da página encerra esse acesso.

- `/`: painel administrativo com indicadores, ações, configurações e retenção.
- `/portal`: demonstração pública com opção de telemetria.
- `/servico/imposto-renda` e `/servico/servico-publico-generico`: páginas simuladas.
- `/feedback?session_id=demo&service_id=imposto-renda`: formulário voluntário.
- `/privacy`: aviso e limites da demonstração.

O arquivo padrão é `prototype-api/avaliador.db`. Para demonstração isolada, defina `AVALIADOR_DB` com um caminho novo. `AVALIADOR_HOST` (padrão `127.0.0.1`), `AVALIADOR_PORT` (8080) e `AVALIADOR_RETENTION_DAYS` (30; intervalo 1–3650) são configuráveis por ambiente. Não há preparação completa para exposição pública: faltam TLS, contas individuais, autorização por papel e revisão de segurança/institucional.

## Escolha e minimização

A página oferece autorizar ou continuar sem telemetria. O identificador técnico e a opção ficam no armazenamento da aba. Interromper bloqueia novos eventos da sessão. O formulário pode ser respondido sem autorizar eventos. A autorização local não define sozinha base legal LGPD.

Antes de enviar eventos, um cliente deve registrar a escolha:

```http
POST /api/session/permission
Content-Type: application/json
```

```json
{"session_id":"demo","allow":true,"notice_version":"transparencia-v1"}
```

Para interromper: `POST /api/session/withdraw` com `{"session_id":"demo"}`. Eventos sem autorização recebem 403. O contrato atual rejeita `user_id`, URL completa e coordenadas; identificadores técnicos não garantem anonimização. Comentários livres devem evitar dados pessoais. Não há envio de telemetria a serviço externo nesta implementação.

## Contratos públicos

Todas as escritas usam JSON, corpo de até 64 KiB e resposta JSON. Valores inválidos recebem 400; origem incompatível, quando informada, recebe 403. `/health` não expõe caminho do banco. Não há liberação CORS indiscriminada.

| Rota | Finalidade |
| --- | --- |
| `GET /health` | Disponibilidade e versão do aviso. |
| `GET /api/services` | Serviços e parâmetros operacionais. |
| `POST /api/session/permission` | Autorizar telemetria da sessão. |
| `POST /api/session/withdraw` | Interromper telemetria da sessão. |
| `POST /api/events/click` | Clique instrumentado após autorização. |
| `POST /api/events/page-time` | Duração informada após autorização. |
| `POST /api/feedback` | Avaliação voluntária. |

Clique mínimo:

```json
{"session_id":"demo","service_id":"imposto-renda","page_id":"servico-ir","page_type":"service"}
```

Duração mínima:

```json
{"session_id":"demo","service_id":"imposto-renda","page_id":"servico-ir","duration_seconds":120}
```

A duração deve ser finita, entre 0 e 86.400 segundos. **O cliente não tem cronômetro automático**: o controle de demonstração envia 120 segundos. A captura automática do estudo histórico foi feita pelo Useberry e pertence a outro artefato.

### Regras e configurações

Para limite L, alerta por clique ocorre em contagem > L. Na página inicial e no serviço prioritário, o convite ocorre em contagem >= L+2; no serviço genérico, > L. Duração aciona quando supera referência × multiplicador. São parâmetros operacionais, sem calibração científica.

Valores iniciais: página inicial e serviço genérico L=12/referência=60 s; Imposto de Renda L=10/referência=45 s; multiplicador=1,5. O primeiro alerta de cada tipo por sessão/serviço guarda a versão vigente. Não se cria outro alerta do mesmo tipo nessa sessão após mudar os parâmetros.

`governance.py` mantém histórico de configurações. Dados iniciais não sobrescrevem serviços existentes. Atualização exige `expected_version`; conflito retorna 409, sem perder a edição anterior. Configuração e histórico são persistidos na mesma transação. O histórico local não é trilha inviolável de auditoria.

### Satisfação e CES

```json
{"session_id":"demo","service_id":"imposto-renda","stars":2,"ces":4,"traits":["tempo_obtencao","usabilidade"],"comment":"Não encontrei o caminho para declarar."}
```

- Satisfação: “Qual é a sua satisfação com esta etapa do serviço?”, inteiro 1–5, de muito insatisfeito(a) a muito satisfeito(a), versão `satisfacao-etapa-v1`.
- CES: “Foi fácil realizar o que eu precisava nesta etapa do serviço”, versão `ces-facilidade-etapa-v1`.
- Categorias CES: 1 discordo totalmente; 2 discordo; 3 discordo parcialmente; 4 nem concordo nem discordo; 5 concordo parcialmente; 6 concordo; 7 concordo totalmente.
- CES opcional: inteiro 1–7, `null` ou campo omitido. Zero, texto numérico, booleanos e decimais são rejeitados. Ausência não é convertida em zero.
- Atributos permitidos: `clareza_informacoes`, `tempo_obtencao`, `esforco_alto`, `usabilidade`, `atendimento`, `eficacia`; confirmar rótulos da interface. Comentário opcional até 2.000 caracteres.

CES maior significa maior facilidade percebida da etapa. Não mede esforço de preencher o formulário, esforço objetivo ou efetividade real do serviço. A redação adaptada ainda exige avaliação com cidadãos.

## Contratos administrativos

Todas as rotas `/api/admin/*`, tanto leitura quanto escrita, exigem `Authorization: Bearer <chave>`. Ausência ou chave inválida recebe 401.

| Rota | Finalidade |
| --- | --- |
| `GET /api/admin/dashboard` | Indicadores e metadados dos itens. |
| `GET /api/admin/alerts` | Alertas e versão da configuração na ocorrência. |
| `GET /api/admin/configurations` | Serviços e histórico. |
| `POST /api/admin/configurations` | Alterar parâmetros com versão esperada. |
| `GET /api/admin/improvements` | Ações, retratos iniciais e acompanhamento. |
| `POST /api/admin/improvements` | Criar ação ou acrescentar acompanhamento. |
| `GET /api/admin/retention` | Prévia de descarte. |
| `POST /api/admin/retention` | Executar descarte correspondente à prévia. |

Configuração de exemplo (consulte a versão atual antes de enviar):

```json
{"service_id":"imposto-renda","expected_version":1,"click_threshold":10,"average_duration_seconds":45,"duration_multiplier":1.5,"reason":"Parâmetros operacionais da demonstração"}
```

Limites: cliques inteiros 1–10.000; referência inteira 1–86.400; fator numérico finito 1–10; justificativa 10–500 caracteres.

### Denominadores

O painel usa somente as versões atuais para `average_stars`/`average_ces`; sem resposta válida, devolve `null`. Informa `stars_responses`, `stars_other_versions`, `ces_responses`, `ces_missing`, `ces_other_versions` e `ces_distribution`. `ces_missing` é o total de feedbacks salvos sem CES e soma `ces_missing_current_contract` (versão de satisfação atual, que identifica o contrato que inclui CES) e `ces_missing_legacy_or_unknown` (versão anterior ou não identificada). Não se presume que os registros legados receberam o item. A versão de contrato não comprova exposição: nenhum desses contadores permite calcular taxa de não resposta ao convite. A distribuição é necessária para interpretar a média descritiva de categorias ordinais.

`session_metrics` apresenta contagem por serviço; os totais `sessions_with_clicks` e `sessions_with_alerts` usam sessões distintas na base. Somar linhas por serviço pode contar o mesmo identificador mais de uma vez. `attribute_metrics` apresenta frequência de atributos escolhidos. Não há taxa A/B, registro de exposição, ranking ou classificação automática de comentários.

### Dado → interpretação → ação → acompanhamento

Criar ação:

```json
{"service_id":"imposto-renda","evidence_type":"ces","insight":"Investigar orientação da etapa","improvement":"Revisar as instruções apresentadas","owner_role":"Equipe de conteúdo","due_date":"2026-12-01"}
```

Evidências permitidas: `ces`, `satisfacao`, `alertas`, `atributos`, `outro`. Interpretação e ação: 10–1.000 caracteres; papel: 2–80; prazo ISO opcional. A linha inicial guarda indicadores e seus denominadores no momento da criação.

Acrescentar acompanhamento:

```json
{"action_id":1,"status":"em_andamento","note":"Revisão de conteúdo iniciada pela equipe"}
```

Situações: `aberta`, `em_andamento`, `concluida`; nota 10–1.000 caracteres. Cada observação acrescenta retrato e histórico; o retrato inicial permanece. Esses retratos usam a base acumulada disponível, não janelas estatísticas equivalentes. Concluir ação não comprova efeito causal.

### Retenção

Primeiro consulte a prévia. A confirmação deve enviar `confirm: true`, o mesmo `cutoff` e o `preview_token` retornados. Se as contagens, identidades ou conteúdos previstos mudarem, recebe 409 e exige nova prévia. A prévia e a execução usam o mesmo critério de referências restantes.

O descarte remove eventos, alertas e feedbacks vencidos, sessões vencidas sem referências restantes e ações concluídas vencidas com seus históricos. Ações abertas/em acompanhamento e configurações permanecem para sua finalidade operacional; exigem política de revisão institucional. Não há execução agendada automática. Prazo padrão de 30 dias é demonstrativo, não prescrição legal.

**Backups, cópias de migração, TCLEs e gravações Useberry não são excluídos por essa rotina.** Guardá-los, restringir acesso e descartá-los depende de procedimento separado. A mudança do contrato não remove campos antigos automaticamente.

## Migração de bancos anteriores

Na primeira inicialização de uma base do esquema anterior, uma cópia `*.pre-ces-*.db` é criada junto ao arquivo antes da alteração. IDs, estrelas, atributos, comentários e datas são preservados na tabela ativa. O indicador retirado permanece somente na cópia histórica; o CES e sua versão ficam nulos nos registros antigos. Não há conversão de escalas nem atribuição retroativa de versão às estrelas antigas. A migração é idempotente.

As novas tabelas de configurações/ações e colunas de autorização são criadas sem sobrescrever parâmetros existentes. Sessões anteriores não recebem autorização de telemetria retroativa. Clientes antigos precisam adaptar o contrato; o campo retirado é rejeitado. Não publique bases ou cópias históricas.

## Verificação reproduzível

Na raiz:

```powershell
python -m unittest discover -s prototype-api -p 'test_*.py' -v
```

19 testes, bases temporárias e dados sintéticos. Cobrem escalas/ausências, migração, versões, agregações, configurações/conflitos/reinicialização, autorização/interrupção/minimização, acesso, ações e retenção. O resultado local não equivale a validação do CES, auditoria de segurança, teste de carga ou avaliação acessível abrangente. Requisitos, rastreabilidade e planos estão nos Apêndices H–K de `docs/tcc.md`.

## Evidência da execução

A execução automatizada assistida por agente de 15/10/2026 passou os 19 casos. A saída está em `docs/evidencias/verificacao-medio-prazo.txt`; o JSON correspondente registra ambiente, horários, comando, commit-base e hashes dos arquivos efetivamente testados. Não confundir commit-base com alterações locais ainda não commitadas. A matriz e o catálogo H.5/H.6 identificam os métodos, distinguindo cobertura técnica parcial de avaliação futura. Para produzir novo registro, execute `python scripts/registrar_verificacao.py` na raiz; os arquivos de evidência serão atualizados.

A confirmação de retenção é vinculada à prévia por um resumo SHA-256 das tabelas, identidades e conteúdos dos registros a eliminar, além do corte e das contagens. Uma substituição com a mesma contagem ou alteração de conteúdo invalida o token e exige nova prévia. O token não expõe os registros e não substitui auditoria independente ou controle de acesso ao SQLite.
