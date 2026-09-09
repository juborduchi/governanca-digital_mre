# Como usar o Agente de Classificação de Notas à Imprensa do MRE

Este agente processa as notas à imprensa do MRE (em `/workspaces/governanca-digital_mre/json-notas`)
para a pesquisa sobre **Governança Global Digital**. O fluxo tem **três etapas**:

1. **Filtragem heurística** — seleciona as notas pertinentes ao tema (script).
2. **Validação por LLM** — o modelo reexamina o JSON filtrado e remove falsos positivos
   (não percorre todas as notas originais).
3. **Escala ordinal semântica (1–5)** — o LLM lê os `paragrafos` de cada nota e atribui nota segundo parâmetros que você define (skill para o modelo).

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

## Etapa 2 — Validação por LLM

Esta etapa é executada pelo **modelo de linguagem** (o agente), não por script.
Peça para o agente seguir a skill:

> "Siga `prompts/prompt02_verificar_llm.md`"

O LLM então:
1. Lista `resultados/jsons-filtrados/` e usa o **`json-filtragem-heuristico-[data].json`** mais recente.
2. **Lê os `paragrafos`** de cada nota **já filtrada** — não percorre as notas originais.
3. Detecta **falsos positivos** (menção digital incidental em nota de comércio/economia/
   cultura/ciência, calendários/agendas sem posicionamento, duplicadas).
4. Gera em `resultados/verificacoes/`:
   - `validacao_llm-[data].md` — relatório
   - `verificacao_llm-[data].json` — notas relevantes (**entrada da Etapa 3**)

> Nota: o antigo script heurístico `skill/validar_filtragem.py` fica como referência
> legada; a validação ativa passa a ser semântica, por LLM.

---

## Etapa 3 — Escala ordinal semântica (LLM)

Esta etapa é executada pelo **modelo de linguagem** (o agente), não por script.
Peça para o agente seguir a skill:

> "Siga `prompts/prompt01_llm.md`"

O agente então:
1. Lista `resultados/verificacoes/` e `resultados/jsons-filtrados/` e pergunta qual JSON usar
   (use preferencialmente `verificacao_llm-*.json` da Etapa 2).
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
│   ├── validar_filtragem.py       # Etapa 2 heurística (legada)
│   └── parametros_escala.exemplo.json  # exemplo de parâmetros 1–5
├── prompts/
│   ├── prompt02_verificar_llm.md      # Etapa 2 (verificação da filtragem por LLM)
│   └── prompt01_llm.md                # Etapa 3 (escala ordinal por LLM)
└── resultados/
    ├── filtragem_heuristico-[data].csv
    ├── jsons-filtrados/json-filtragem-heuristico-[data].json
    └── verificacoes/                  # saídas da Etapa 2
```

---

## Fluxo resumido

```bash
# 1) Filtragem
python3 skill/executar_filtro.py 2014 2025

# 2) Validação (pedir ao agente/LLM)
#    "Siga prompts/prompt02_verificar_llm.md"

# 3) Escala ordinal (pedir ao agente/LLM)
#    "Siga prompts/prompt01_llm.md"
```

Pronto: de ~5.169 notas originais chega-se a um conjunto refinado e quantificado
qualitativamente na escala ordinal 1–5.
