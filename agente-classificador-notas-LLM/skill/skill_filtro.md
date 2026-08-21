# skill_filtro.md — Filtro Heurístico de Notas à Imprensa do MRE

## Identidade
Filtro automático (sem LLM nesta etapa) para a pesquisa sobre **Governança
Global Digital** (contexto em `contextos/contexto01.md`). O objetivo é selecionar
as notas à imprensa do MRE que guardem relação direta e substantiva com o tema.

## Como funciona
O script `skill/executar_filtro.py` faz:

1. **Pré-seleção por vocabulário substantivo** de governança digital (internet,
   IA, dados, soberania digital, direitos online, cibersegurança, infraestrutura
   digital, foros multissetoriais), com variantes de grafia.
2. **Critério qualitativo leve**: exige conexão direta no corpo do texto; termos
   fracos (ex.: "privacidade") só contam se houver sinal digital no mesmo parágrafo.
3. **Descarte de calendários/agendas** (lista de termos + notas muito curtas).
4. Geração de **justificativa em linguagem natural** referenciando os temas
   identificados e trechos da nota.

> Esta etapa é heurística (palavras-chave). A **avaliação ordinal (nota 1–5)**
> é feita separadamente, por LLM, em `prompts/prompt01_llm.md`.

## Execução
```bash
python3 skill/executar_filtro.py            # todos os anos
python3 skill/executar_filtro.py 2014 2025  # intervalo inclusivo
```

## Saídas (em `resultados/`)
- `filtragem_heuristico-[data].csv` — colunas: Titulo, Data, Link, Justificativa, Passagens_Relevantes
- `jsons-filtrados/json-filtragem-heuristico-[data].json` — notas filtradas, no
  formato `_default`, com bloco `analise_filtragem` (temas, justificativa, passagens).

Este JSON filtrado é a **entrada** da etapa ordinal semântica.
