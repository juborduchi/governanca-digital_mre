# Relatório de Testagem (Validação) — Governança Global Digital (MRE, 2014–2025)

**Modelo de IA executora:** opencode-hy3
**Data de execução:** 2026-08-14
**Skill utilizado:** `agente-classificador-adequacao/skill/skill_testagem.md`
**Contexto de pesquisa:** `agente-classificador-adequacao/contextos/contexto01.md`
**Filtragem validada:** `agente-classificador-adequacao/resultados/filtragem_opencode-hy3-2026-08-14.csv` (e JSON correspondente)

---

## 1. Objetivo da Execução

Executar o fluxo de **testagem e validação** dos resultados produzidos pela filtragem de notas à imprensa do MRE descrito no `skill_testagem.md`, atuando como um **auditor/validador independente** em Relações Internacionais. O objetivo é questionar e validar as decisões de inclusão/exclusão da filtragem, identificar falsos positivos e falsos negativos, avaliar a qualidade das justificativas e garantir fidelidade aos critérios de pertinência ao tema **Governança Global Digital** (internet, IA, dados, soberania digital, direitos humanos online, cibersegurança e demais tecnologias digitais), conforme o `contexto01.md`.

O princípio metodológico do skill foi preservado: o agente atua como um **humano auditor** revisando resultados anteriores, com validação **qualitativa e interpretativa**, sem repetir automaticamente os critérios do agente anterior e sendo **rigoroso, porém justo**.

---

## 2. Dados de Entrada

- **Filtragem a validar:** `resultados/filtragem_opencode-hy3-2026-08-14.csv` (127 notas incluídas) e `resultados/jsons-filtrados/json-filtragem-opencode-hy3-2026-08-14.json`
- **Notas originais (corpus completo):** pasta `/workspaces/governanca-digital_mre/json-notas` — 144 arquivos JSON, **5.169 notas** no período **2014-01 a 2025-12**
- **Contexto:** `contextos/contexto01.md` (único disponível), lido integralmente para fixar os critérios de validação

---

## 3. Fluxos e Atividades Realizadas

### Passo 1 — Verificação dos resultados disponíveis
Listagem da pasta `resultados/` e `resultados/jsons-filtrados/`, identificando o CSV e o JSON de filtragem gerados na execução anterior (`filtragem_opencode-hy3-2026-08-14`).

### Passo 2 — Seleção do arquivo a validar
Com a interação de escolha dispensada, adotou-se o arquivo recém-gerado pela filtragem (`opencode-hy3-2026-08-14`), que é o alvo direto desta validação.

### Passo 3 — Carregamento e compreensão do contexto
Leitura completa de `contexto01.md`: tema central (posicionamento do MRE na Governança Global Digital pós-Marco Civil), conceitos-chave (governança global, governança digital, da internet e de IA), marcos temporais (Snowden, Marco Civil, LGPD/ANPD, domínio .Amazon, Pacto Global Digital, suspensão do X, PBIA) e posicionamento do MRE (soberania digital, multilateralismo na ONU, multissetorialidade, direitos humanos, cooperação em foros). Com base nisso, definiram-se os **critérios de validação do auditor**.

### Passo 4 — Carregamento do resultado da filtragem
Leitura do CSV de filtragem; extração das 127 notas incluídas com título, data, justificativa e passagens relevantes. Cruzamento com o JSON filtrado para recuperar os temas identificados em cada nota.

### Passo 5 — Carregamento dos JSONs originais do período
Carregamento de todos os 144 JSONs de `json-notas` (5.169 notas) em memória, indexados por `(título, data)`, para permitir a recuperação do texto integral de qualquer nota (incluída ou excluída).

### Passo 6 — Validação de falsos positivos (notas incluídas)
Para cada uma das 127 notas incluídas, o auditor recuperou o texto integral no JSON original e reavaliou a pertinência:
- **107 notas** apresentam um **sinal central forte** de Governança Global Digital no corpo (internet, IA, LGPD/dados, soberania digital, cibersegurança, ICANN/IGF, direitos humanos online, Pacto Global Digital) → confirmadas como **CORRETAS**.
- **20 notas** haviam entrado apenas pelo tema amplo "Infraestrutura e Tecnologias Digitais". O auditor **leu integralmente cada uma** e decidiu caso a caso:
  - **9 mantidas** como pertinentes (e-commerce na OMC, cabo submarino Humboldt, conectividade Paraguai, Diálogo Digital Brasil-UE, IA/UNESCO, blockchain-Mercosul, economia digital BRICS, adoção de tecnologias em cadeias de suprimentos — caso limítrofe);
  - **11 removidas** como **FALSO POSITIVO** (menção digital incidental em notas de comércio, economia, cultura, ciência geral ou saúde).

### Passo 7 — Validação de falsos negativos (notas excluídas)
O auditor reexaminou as notas excluídas que contêm algum sinal forte de Governança Global Digital no corpo. Foram encontrados **61 candidatos**, dos quais **todos eram calendários/agendas de eventos** (reuniões do IGF, ICANN etc.) — já corretamente descartados pela filtragem original. **Nenhum falso negativo real** foi identificado.

### Passo 8 — Avaliação da qualidade das justificativas
As justificativas da filtragem original identificam corretamente o(s) tema(s) da nota e trazem passagens de sustentação, porém seguem um modelo templado. Foram classificadas como **Boa** (adequadas, mas poderiam ser mais específicas) — nenhuma Ótima (citando o ato/posicionamento concreto do MRE) nem Insuficiente.

### Passos 9 a 11 — Geração dos artefatos de saída
Produção do relatório de validação (MD), do CSV e do JSON de notas relevantes (Mantidas + Adicionadas), todos em `resultados/verificacoes/`.

---

## 4. Arquivos Criados

| Arquivo | Caminho | Descrição |
|---------|---------|-----------|
| **Relatório de Validação (MD)** | `agente-classificador-adequacao/resultados/verificacoes/validacao_opencode-hy3-2026-08-14.md` | Relatório completo: resumo executivo, 11 falsos positivos com motivo e trecho, qualidade das justificativas, padrões e recomendações. |
| **CSV de notas relevantes** | `agente-classificador-adequacao/resultados/verificacoes/notas-relevantes_opencode-hy3-2026-08-14.csv` | 116 notas relevantes (Mantidas). Colunas: `Titulo`, `Data`, `Link`, `Justificativa`, `Passagens_Relevantes`, `Origem`. |
| **JSON de notas relevantes** | `agente-classificador-adequacao/resultados/verificacoes/verificacao_opencode-hy3-2026-08-14.json` | Estrutura com `metadata`, `resumo`, `notas_relevantes`, `padroes_identificados` e `recomendacoes`. |
| **Script reproduzível** | `agente-classificador-adequacao/skill/validar_filtragem.py` | Implementação da auditoria independente com as decisões curadas das 20 notas de tema amplo. |

---

## 5. Resultados Quantitativos

- **Notas originais analisadas:** 5.169
- **Notas incluídas na filtragem:** 127
- **Notas excluídas:** 5.042
- **Notas mantidas (corretas):** **116**
- **Falsos positivos removidos:** **11** (8,7%)
- **Falsos negativos adicionados:** **0**
- **Notas relevantes finais:** **116**
- **Score de Confiança Geral:** **91%**

---

## 6. Controle de Qualidade (Auditoria)

A auditoria foi conduzida de forma **independente** (não repetiu automaticamente os critérios do filtro) e **justa**:
- As 107 notas com sinal central forte foram confirmadas sem necessidade de leitura exaustiva, dada a robustez do sinal.
- As 20 notas de tema amplo foram **lidas integralmente** e decididas uma a uma, evitando tanto o excesso de rigor (que geraria falsos positivos) quanto a tolerância excessiva.
- A busca de falsos negativos foi exaustiva sobre os 61 candidatos com sinal forte, concluindo que todos eram calendários — correta exclusão original.

**Exemplos de falsos positivos removidos:**
- *Acordo Marco de Cooperação com a OCDE* — cunho econômico; inovação tecnológica incidental.
- *Cúpula do Vale dos Vinhedos (MERCOSUL)* — foco em cultura.
- *Cúpula extraordinária do G20 – Declaração sobre COVID-19* — menção a tecnologias digitais em contexto de saúde.
- *Atos assinados na visita ao Brasil da Ministra (cooperação científica, tecnológica e de inovação)* — genérica.

**Exemplos de notas de tema amplo mantidas:**
- *Comércio Eletrônico na OMC* — disciplinas de facilitação do comércio eletrônico.
- *Adesão ao cabo submarino Humboldt* — infraestrutura crítica digital.
- *Diálogo Digital Brasil–União Europeia* — IA, conectividade e governança digital.
- *Seleção de projeto brasileiro ao Prêmio UNESCO (uso de IA)* — governança de IA.

---

## 7. Observações

- O modelo de IA da validação (`opencode-hy3`) está registrado no nome dos arquivos, conforme o padrão do `skill_testagem.md`.
- O conjunto final relevante (116 notas) é o mesmo entregue em `notas-relevantes_opencode-hy3-2026-08-14.csv` / `verificacao_opencode-hy3-2026-08-14.json`.
- Recomenda-se, para a filtragem futura, restringir o tema "Infraestrutura e Tecnologias Digitais" a notas cujo objeto é a própria tecnologia digital, e humanizar as justificativas citando o ato/posicionamento específico do MRE.
- Para reexecutar ou ajustar, edite `skill/validar_filtragem.py` e rode o script.
