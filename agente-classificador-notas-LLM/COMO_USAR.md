# Como usar o Agente de Classificação de Notas à Imprensa do MRE

Este agente processa as notas à imprensa do MRE (em `/workspaces/governanca-digital_mre/json-notas`)
para a pesquisa sobre **Governança Global Digital**. O fluxo tem **três etapas**:

1. **Filtragem heurística** — seleciona as notas pertinentes ao tema (script).
2. **Escala ordinal semântica (1–5)** — o LLM lê os `paragrafos` de cada nota e atribui nota segundo parâmetros que você define (skill para o modelo).
3. **Validação da Escala Ordinal (com Triangulação)** — o modelo cruza o JSON de escala ordinal com o JSON de filtragem heurística, verificando coerência com os parâmetros, metadados de filtragem e identificando possíveis inconsistências.

---

## Pré-requisitos
- Python 3 instalado.
- As notas de entrada em `/workspaces/governanca-digital_mre/json-notas`.
- O contexto de pesquisa em `contextos/contexto01.md`.

---

## Etapa 1 — Filtragem heurística

```bash
cd /workspaces/governanca-digital_mre/agente-classificador-notas-LLM
python3 skill/executar_filtro.py            # todos os anos disponíveis
python3 skill/executar_filtro.py 2014 2025  # intervalo de anos (inclusivo)
```

**Saídas** (em `resultados/`):
- `filtragem_heuristico-[data].csv` — colunas: Titulo, Data, Link, Justificativa, Passagens_Relevantes
- `jsons-filtrados/json-filtragem-heuristico-[data].json` — notas filtradas (com `paragrafos` e `analise_filtragem`)

---

## Etapa 2 — Escala ordinal semântica (LLM)

Esta etapa é executada pelo **modelo de linguagem** (o agente), não por script.
Peça para o agente seguir a skill:

> "Siga `prompts/prompt01_llm.md`"

O agente então:
1. Lista `resultados/filtragem-heuristica/` e pergunta qual JSON usar.
2. Pergunta os **parâmetros da escala 1–5**. Exemplo de eixo sugerido (pode ser substituído):
   - **1** — Soberania Digital: soberania do Estado, garantias democráticas, direitos fundamentais, multilateralismo, multissetorialismo
   - **2** — Predominantemente Soberanista: foco em soberania/direitos, com alguma abertura para inovação
   - **3** — Modelo Misto: equilíbrio entre soberania/direitos e desenvolvimento/inovação
   - **4** — Predominantemente Liberal: foco em inovação/mercado, com alguma regulação
   - **5** — Baixa Intervenção Estatal: inovação livre, autorregulação, lógica mercantil
3. **Lê os `paragrafos`** de cada nota e atribui uma nota de 1 a 5, com justificativa própria
   e até 3 passagens literais.
4. Gera (em `resultados/`):
   - `escala-ordinal_[modelo]-[data].csv` — Titulo, Link, Data, Nota_Escala, Descricao_Nota, Justificativa, Passagens_Relevantes
   - `escalas-ordinais/escala-ordinal-[modelo]-[data].json`

---

## Etapa 3 — Validação da Escala Ordinal (LLM, com Triangulação)

Esta etapa é executada pelo **modelo de linguagem** (o agente), não por script.
Peça para o agente seguir a skill:

> "Siga `prompts/prompt03_validar_escala.md`"

O agente então:
1. Lista `resultados/escalas-ordinais/` e pergunta qual JSON usar (escala ordinal).
2. Lista `resultados/filtragem-heuristica/` e pergunta qual JSON usar (filtragem heurística).
3. **Cruza** cada nota da escala ordinal com o registro correspondente no JSON de filtragem
   (por `titulo` + `data`), associando metadados como `classificado`, `categoria`, `autoria`.
4. Pergunta os **parâmetros da escala 1–5** que foram usados na classificação original.
5. **Lê os `paragrafos` integrais** do JSON de filtragem e verifica se a nota atribuída está
   coerente com o conteúdo, com os metadados de filtragem e com os parâmetros definidos.
6. **Detecta padrões**: notas da mesma classificação heurística recebendo notas sem distinção.
7. Identifica **inconsistências** (notas onde a classificação não condiz com o conteúdo).
8. Gera em `resultados/verificacoes-ordinal/`:
   - `validacao-escala-[modelo]-[data].json` — dados completos da validação (inclui `classificado_heuristico`)
   - `relatorio-validacao-escala-[modelo]-[data].md` — relatório legível
   - `validacao-escala-[modelo]-[data].csv` — planilha com todas as notas avaliadas

---

## Estrutura de arquivos

```
agente-classificador-notas-LLM/
├── README.md                      # visão geral do pipeline
├── COMO_USAR.md                   # este guia
├── contextos/
│   └── contexto01.md              # contexto de pesquisa (Governança Global Digital)
├── skill/
│   ├── executar_filtro.py         # Etapa 1 (filtragem heurística)
│   ├── skill_filtro.md            # documentação da Etapa 1
│   ├── validar_filtragem.py       # validação heurística (legada)
│   └── parametros_escala.exemplo.json  # exemplo de parâmetros 1–5
├── prompts/
│   ├── prompt01_llm.md                # Etapa 2 (escala ordinal por LLM)
│   └── prompt03_validar_escala.md     # Etapa 3 (validação da escala ordinal, com triangulação)
└── resultados/
    ├── filtragem_heuristico-[data].csv
    ├── jsons-filtrados/json-filtragem-heuristico-[data].json
    ├── filtragem-heuristica/json-filtragem-heuristico-[data].json
    ├── escalas-ordinais/              # saídas da Etapa 2
    └── verificacoes-ordinal/          # saídas da Etapa 3
```

---

## Fluxo resumido

```bash
# 1) Filtragem
python3 skill/executar_filtro.py 2014 2025

# 2) Escala ordinal (pedir ao agente/LLM)
#    "Siga prompts/prompt01_llm.md"

# 3) Validação da escala ordinal — com triangulação (pedir ao agente/LLM)
#    "Siga prompts/prompt03_validar_escala.md"
```

Pronto: de ~5.169 notas originais chega-se a um conjunto refinado e quantificado
qualitativamente na escala ordinal 1–5, com validação de coerência.
