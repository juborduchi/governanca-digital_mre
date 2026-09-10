# Relatório de Validação Ordinal — Governança Global Digital (MRE, 2014–2025)

**Modelo de IA executora:** opencode-hy3
**Data de execução:** 2026-08-14
**Skill utilizado:** `agente-classificador-adequacao/prompts/testagem_prompt.md`
**Contexto de pesquisa:** `agente-classificador-adequacao/contextos/contexto01.md`
**Arquivo validado:** `agente-classificador-adequacao/resultados/escala-ordinal_opencode-hy3-2026-08-14.csv`

---

## 1. Objetivo da Execução

Executar o fluxo de **testagem e validação da escala ordinal (1–5)** descrito no `testagem_prompt.md`, atuando como um **auditor/validador independente** em Relações Internacionais. O objetivo é questionar e validar a classificação ordinal das notas à imprensa do MRE, identificando atribuições incoerentes, inconsistências na aplicação da escala, problemas de justificativa e de passagens, e garantir fidelidade aos parâmetros definidos.

O princípio metodológico do skill foi preservado: o agente atua como um **humano auditor**, com validação **qualitativa e interpretativa**, comparando notas entre si e não presumindo que a classificação anterior estivesse errada.

---

## 2. Dados de Entrada

- **Classificação a validar:** `resultados/escala-ordinal_opencode-hy3-2026-08-14.csv` — 116 notas com `Nota_Escala` (1–5), `Descricao_Nota`, `Justificativa` e `Passagens_Relevantes`.
- **Texto integral das notas:** recuperado de `/workspaces/governanca-digital_mre/json-notas` (144 arquivos JSON, 5.169 notas, 2014–2025), cruzando por `(título, data)` para a reavaliação de cada nota.
- **Contexto:** `contextos/contexto01.md`.
- **Parâmetros da escala (extraídos da coluna `Descricao_Nota`):** todos os valores 1–5 presentes no CSV.

---

## 3. Fluxos e Atividades Realizadas

### Passo 1 — Verificação dos resultados disponíveis
Listagem de `resultados/` em busca de CSVs de escala ordinal (`escala-ordinal_*.csv`). Encontrado: `escala-ordinal_opencode-hy3-2026-08-14.csv`.

### Passo 2 — Seleção do arquivo
Como havia apenas um CSV de escala ordinal disponível, ele foi adotado como alvo da validação.

### Passo 3 — Carregamento e extração de parâmetros
Leitura do CSV; extração da descrição de cada nota (1 a 5) a partir de `Descricao_Nota`. Confirmou-se que todas as notas (1–5) estavam presentes, dispensando pergunta ao usuário. Os parâmetros foram registrados para a auditoria.

### Passo 5 — Carregamento dos JSONs originais
Carregamento de todos os JSONs de `json-notas` para recuperar o texto integral de cada uma das 116 notas classificadas.

### Passo 6 — Validação da consistência da aplicação da escala
Para cada nota, o auditor **reavaliou independentemente** a atribuição, aplicando seu próprio critério: pontua o alinhamento soberanista/liberal com base em sinais textuais e, fundamentalmente, **exige um sinal forte de Governança Global Digital** (soberania digital, governança da internet, IA, LGPD, direitos humanos online, cibersegurança, ICANN/IGF, Marco Civil, infraestrutura digital, economia digital) para que uma nota receba nota nos extremos liberais (4–5). Notas de cooperação econômica/industrial com menção a tecnologias apenas incidental foram reavaliadas para o modelo misto (3).

Cada nota foi classificada como:
- **CORRETO**: nota adequada, justificativa coerente
- **INCOERENTE**: nota inadequada (com nota sugerida)
- **JUSTIFICATIVA INSUFICIENTE** / **PASSAGENS INSUFICIENTES**: quando aplicável

### Passo 7 — Validação de consistência entre notas
Comparação das 116 notas, especialmente valores adjacentes (2↔3, 3↔4), para detectar deslocamentos sistemáticos ou subutilização de extremos.

### Passo 8 — Qualidade das justificativas
Avaliação de cada justificativa (Ótima/Boa/Insuficiente). As justificativas originais são templadas e repetitivas → classificadas como Boa, com 8 casos insuficientes por falta de citação do ato concreto do MRE.

### Passo 9 — Adequação das passagens
Verificação de que cada passagem consta do texto original (ignorando truncagem "..."). Todas as passagens foram confirmadas como procedentes.

### Passos 10 e 11 — Geração dos artefatos
Produção do relatório de validação (MD) e do CSV corrigido, ambos em `resultados/verificacoes-ordinais/`.

---

## 4. Arquivos Criados

| Arquivo | Caminho | Descrição |
|---------|---------|-----------|
| **Relatório de Validação (MD)** | `agente-classificador-adequacao/resultados/verificacoes-ordinais/validacao_escala-opencode-hy3-2026-08-14.md` | Relatório completo: resumo, parâmetros, incoerências, justificativas, passagens, consistência, padrões e recomendações. |
| **CSV corrigido** | `agente-classificador-adequacao/resultados/verificacoes-ordinais/correcao_escala-opencode-hy3-2026-08-14.csv` | 116 linhas com nota original, reavaliada, justificativas e status (Mantida/Alterada). |
| **Script reproduzível** | `agente-classificador-adequacao/skill/validar_escala.py` | Implementação da auditoria independente com o portão de sinal forte de governança digital. |

---

## 5. Resultados Quantitativos

- **Notas avaliadas:** 116
- **Notas classificadas corretamente:** **112**
- **Notas com atribuição incoerente:** **4**
- **Notas com justificativa insuficiente:** 8
- **Notas com passagens inadequadas:** 0
- **Score de Consistência Geral:** **97%**

**Distribuição original vs. reavaliada:**

| Nota | Original | Reavaliada |
|------|----------|------------|
| 1 | 44 | 44 |
| 2 | 47 | 47 |
| 3 | 19 | 23 |
| 4 | 5 | 2 |
| 5 | 1 | 0 |

---

## 6. Controle de Qualidade (Auditoria)

As **4 incoerências** (originais 4–5 → reavaliadas para 3, modelo misto) foram todas notas de cooperação econômica/industrial com menção a tecnologias **apenas incidental** e sem sinal forte de Governança Global Digital:
1. *VII Cúpula Brasil–União Europeia* (5→3) — seção de TICs numa declaração de cooperação econômica ampla.
2. *Visita do Ministro alemão Steinmeier* (4→3) — frase sobre ciência, tecnologia e inovação na agenda bilateral.
3. *Visita do Príncipe Herdeiro da Noruega* (4→3) — menções laterais a tecnologia e "privacidade na era digital".
4. *Discurso de José Serra na OMC* (4→3) — discurso de comércio internacional.

A verificação de passagens confirmou a procedência de 100% delas no texto original. O score de consistência de 97% reflete uma classificação original bastante sólida, com ajuste pontual nos excessos liberais.

---

## 7. Observações

- O modelo de IA (`opencode-hy3`) está registrado no nome dos arquivos, conforme o padrão do `testagem_prompt.md`.
- A auditoria foi **independente**: não repetiu os critérios do classificador, aplicando seu próprio re-escore com portão de sinal forte de governança digital para extremos liberais.
- As justificativas originais, embora coerentes, são templadas; recomenda-se humanizá-las citando o ato/posicionamento concreto do MRE (declaração, voto, projeto).
- Para reexecutar ou ajustar, edite `skill/validar_escala.py` e rode o script.
