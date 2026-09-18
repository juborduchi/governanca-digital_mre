# Prompt para Geração de Fluxograma – Agente de Classificação de Notas

Gere um fluxograma/organograma detalhado do pipeline de classificação de notas a imprensa do MRE (Itamaraty) para Governança Global Digital. O pipeline tem 3 estágios:

---

## ESTÁGIO 1 – Filtragem Heurística (script Python, sem LLM)

- **Entrada:** ~5.169 notas a imprensa em JSON (período 2014–2025)
- O script `executar_filtro.py` realiza:
  - Filtragem por ano (parâmetro opcional)
  - Correspondência de vocabulário em 9 categorias temáticas:
    1. Governança da Internet
    2. Inteligência Artificial
    3. Proteção de Dados e Privacidade
    4. Soberania Digital
    5. Direitos Humanos Online
    6. Cibersegurança
    7. Infraestrutura e Tecnologias Digitais
    8. Economia e Comércio Digital
    9. Multilateralismo e Fóruns de Governança Digital
  - Descarte qualitativo de agendas/calendários
  - Rejeição de notas curtas (≤2 parágrafos e <200 caracteres)
  - Filtro de ruído: termos genéricos sozinhos não contam
  - Verificação de co-ocorrência: termos fracos precisam de "sinal digital" no mesmo parágrafo
  - Geração de justificativa textual
- **Saída:** 178 notas filtradas em CSV e JSON

---

## ESTÁGIO 2 – Classificação por Escala Ordinal (LLM interativo via prompt)

- **Entrada:** JSON filtrado do Estágio 1
- O usuário define parâmetros de uma escala 1–5:
  - **1** = Soberania Digital (soberania estatal, democracia, direitos fundamentais, multilateralismo, multistakeholderismo)
  - **2** = Predominantemente Soberanista (foco em soberania/direitos, alguma abertura à inovação)
  - **3** = Modelo Misto (equilíbrio entre soberania/direitos e desenvolvimento/inovação)
  - **4** = Predominantemente Liberal (foco em inovação/abertura de mercado, alguma regulação estatal)
  - **5** = Baixa Intervenção Estatal (inovação livre, autorregulação, lógica de mercado)
- A LLM lê os parágrafos completos de cada nota (não apenas títulos)
- Para cada nota: atribui nota 1–5, escreve justificativa (2–3 frases), seleciona até 3 passagens relevantes
- **Princípios:** pontuação por significado (não contagem de palavras), sem justificativas de template, temperature=0
- **Saída:** 178 notas classificadas em CSV e JSON

---

## ESTÁGIO 3 – Validação com Triangulação (LLM interativa via prompt)

- **Entrada:** JSON da escala ordinal (Estágio 2) + JSON da filtragem heurística (Estágio 1)
- A LLM atua como auditora:
  - Cruzamento (triangulação) entre os dois JSONs por título/data
  - Validação de cada nota: compara a atribuição com o conteúdo + metadados (classificação heurística, categoria, autoria, país)
  - Verificação de coerência com a classificação heurística
  - Detecção de padrões e inconsistências
  - Viés conservador em casos limítrofes
- **Saída:** 3 arquivos — JSON validado, relatório Markdown, CSV (separador ponto-e-vírgula, UTF-8 BOM)

---

## Opcional: Visualização (Jupyter notebooks)

- Gráfico de barras da distribuição de notas
- Evolução temporal (média mensal/anual)
- Barras empilhadas por ano/mês
- Boxplot e histograma

---

## Requisitos do fluxograma

**Gere a imagem do fluxograma diretamente aqui no chat.** Não use Mermaid, SVG, código, ou texto. Crie uma imagem visual (diagrama) usando a ferramenta de geração de imagem disponível.

1. Mostrar a sequência dos 3 estágios com setas de cima para baixo (ou da esquerda para a direita)
2. Indicar entradas e saídas de cada estágio
3. Destacar que o **Estágio 1 é automático** (script Python) e os **Estágios 2 e 3 são interativos** (LLM + usuário)
4. Mostrar os tipos de arquivo de entrada/saída (JSON, CSV)
5. Incluir os principais mecanismos de cada estágio (filtragem por vocabulário, escala ordinal, triangulação)
6. Incluir legenda com os 5 valores da escala ordinal
7. Usar cores ou formas distintas para diferenciar: entrada (losango), processamento (retângulo), saída (losango), decisão/humano (diamante)
8. Fundo claro, fonte legível, estilo profissional
