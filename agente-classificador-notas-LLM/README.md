# Agente de Classificação de Notas à Imprensa do MRE

Pipeline em **quatro etapas**:

1. **Filtragem heurística** das notas à imprensa (seleção por tema de
   Governança Global Digital) — automática, via script.
2. **Validação por LLM** da filtragem — o modelo verifica **apenas** o JSON
   filtrado em busca de falsos positivos e gera o conjunto refinado de notas
   relevantes (não percorre todas as notas originais).
3. **Avaliação ordinal semântica (nota 1–5) por LLM** — o modelo relê os
   `paragrafos` e atribui nota segundo parâmetros definidos pelo usuário.
4. **Validação da Escala Ordinal por LLM** — o modelo reavalia as notas
   classificadas, verificando coerência com os parâmetros e identificando
   possíveis inconsistências.

## Estrutura
- `contextos/contexto01.md` — contexto de pesquisa (Governança Global Digital).
- `skill/executar_filtro.py` — filtragem heurística (etapa 1).
- `skill/skill_filtro.md` — documentação da filtragem heurística.
- `skill/validar_filtragem.py` — validação heurística **legada** (substituída pela etapa 2 por LLM).
- `prompts/prompt02_verificar_llm.md` — skill de **verificação da filtragem por LLM** (etapa 2).
- `prompts/prompt01_llm.md` — skill de **avaliação ordinal por LLM** (etapa 3).
- `prompts/prompt03_validar_escala.md` — skill de **validação da escala ordinal por LLM** (etapa 4).
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

### Etapa 2 — Validação por LLM
Siga `prompts/prompt02_verificar_llm.md`. O LLM lê o JSON filtrado mais recente
(`resultados/jsons-filtrados/json-filtragem-heuristico-[data].json`), reexamina os
`paragrafos` de cada nota incluída e remove falsos positivos. Gera em
`resultados/verificacoes/`:
- `validacao_llm-[data].md` — relatório
- `verificacao_llm-[data].json` — notas relevantes (entrada da etapa 3)

### Etapa 3 — Escala ordinal (LLM)
Peça ao agente para seguir `prompts/prompt01_llm.md`. Ele lerá os `paragrafos`
(usando preferencialmente o JSON validado em `resultados/verificacoes/`), perguntará
os parâmetros 1–5 e gerará em `resultados/`:
- `escala-ordinal_[modelo]-[data].csv`
- `escalas-ordinais/escala-ordinal-[modelo]-[data].json`

### Etapa 4 — Validação da Escala Ordinal (LLM)
Peça ao agente para seguir `prompts/prompt03_validar_escala.md`. Ele lerá o JSON
da escala ordinal, perguntará os parâmetros usados, verificará a coerência de cada
classificação e gerará em `resultados/verificacoes-ordinal/`:
- `validacao-escala-[modelo]-[data].json` — dados completos da validação
- `relatorio-validacao-escala-[modelo]-[data].md` — relatório legível
- `validacao-escala-[modelo]-[data].csv` — planilha com todas as notas avaliadas
