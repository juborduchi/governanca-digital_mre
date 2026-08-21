# Agente de Classificação de Notas à Imprensa do MRE

Pipeline em **três etapas**:

1. **Filtragem heurística** das notas à imprensa (seleção por tema de
   Governança Global Digital) — automática, via script.
2. **Validação heurística** da filtragem — script que re-screena possíveis
   falsos positivos e gera o conjunto refinado de notas relevantes.
3. **Avaliação ordinal semântica (nota 1–5) por LLM** — o modelo relê os
   `paragrafos` e atribui nota segundo parâmetros definidos pelo usuário.

## Estrutura
- `contextos/contexto01.md` — contexto de pesquisa (Governança Global Digital).
- `skill/executar_filtro.py` — filtragem heurística (etapa 1).
- `skill/skill_filtro.md` — documentação da filtragem heurística.
- `skill/validar_filtragem.py` — validação heurística da filtragem (etapa 2).
- `prompts/prompt01_llm.md` — skill de **avaliação ordinal por LLM** (etapa 3).
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

### Etapa 2 — Validação heurística
```bash
python3 skill/validar_filtragem.py
```
Re-screena as notas incluídas apenas pelo tema amplo "Infraestrutura e Tecnologias
Digitais" e gera em `resultados/verificacoes/`:
- `validacao_heuristico-[data].md` — relatório
- `notas-relevantes_heuristico-[data].csv` — notas relevantes
- `verificacao_heuristico-[data].json` — notas relevantes (entrada da etapa 3)

### Etapa 3 — Escala ordinal (LLM)
Peça ao agente para seguir `prompts/prompt01_llm.md`. Ele lerá os `paragrafos`
(usando preferencialmente o JSON validado em `resultados/verificacoes/`), perguntará
os parâmetros 1–5 e gerará em `resultados/`:
- `escala-ordinal_[modelo]-[data].csv`
- `escalas-ordinais/escala-ordinal-[modelo]-[data].json`
