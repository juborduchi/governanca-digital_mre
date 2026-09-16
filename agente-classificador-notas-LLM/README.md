# Agente de Classificação de Notas à Imprensa do MRE

Pipeline em **três etapas**:

1. **Filtragem heurística** das notas à imprensa (seleção por tema de
   Governança Global Digital) — automática, via script.
2. **Avaliação ordinal semântica (nota 1–5) por LLM** — o modelo relê os
   `paragrafos` e atribui nota segundo parâmetros definidos pelo usuário.
3. **Validação da Escala Ordinal por LLM (com Triangulação)** — o modelo
   cruza o JSON de escala ordinal (Etapa 2) com o JSON de filtragem heurística
   (Etapa 1), verificando coerência com os parâmetros, com os metadados de
   filtragem (`classificado`, `categoria`, `autoria`) e identificando possíveis
   inconsistências e padrões.

## Estrutura
- `contextos/contexto01.md` — contexto de pesquisa (Governança Global Digital).
- `skill/executar_filtro.py` — filtragem heurística (etapa 1).
- `skill/skill_filtro.md` — documentação da filtragem heurística.
- `skill/validar_filtragem.py` — validação heurística **legada**.
- `prompts/prompt01_llm.md` — skill de **avaliação ordinal por LLM** (etapa 2).
- `prompts/prompt03_validar_escala.md` — skill de **validação da escala ordinal por LLM, com triangulação** (etapa 3).
- `skill/parametros_escala.exemplo.json` — exemplo de parâmetros 1–5.
- `resultados/` — saídas de cada etapa.

## Como executar

### Etapa 1 — Filtragem heurística
```bash
python3 skill/executar_filtro.py            # todos os anos
python3 skill/executar_filtro.py 2014 2025  # intervalo de anos
```
Gera `resultados/filtragem_heuristico-[data].csv` e
`resultados/jsons-filtrados/json-filtragem-heuristico-[data].json`.

### Etapa 2 — Escala ordinal (LLM)
Peça ao agente para seguir `prompts/prompt01_llm.md`. Ele lerá os `paragrafos`
do JSON de filtragem heurística, perguntará os parâmetros 1–5 e gerará em
`resultados/`:
- `escala-ordinal_[modelo]-[data].csv`
- `escalas-ordinais/escala-ordinal-[modelo]-[data].json`

### Etapa 3 — Validação da Escala Ordinal (LLM, com Triangulação)
Peça ao agente para seguir `prompts/prompt03_validar_escala.md`. Ele lerá o JSON
da escala ordinal **e** o JSON de filtragem heurística correspondente, cruzando
metadados (`classificado`, `categoria`, `autoria`) com a nota atribuída. Perguntará
os parâmetros usados, verificará a coerência de cada classificação e gerará em
`resultados/verificacoes-ordinal/`:
- `validacao-escala-[modelo]-[data].json` — dados completos da validação
- `relatorio-validacao-escala-[modelo]-[data].md` — relatório legível
- `validacao-escala-[modelo]-[data].csv` — planilha com todas as notas avaliadas
