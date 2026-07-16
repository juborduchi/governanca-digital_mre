# Plano de Implementação - Analisador de Governança Global Digital MRE

Este plano descreve o desenvolvimento de uma aplicação em Python para analisar notas à imprensa do Ministério das Relações Exteriores (MRE) do Brasil, focando em Governança Global Digital.

## Visão Geral

A aplicação lerá arquivos JSON que contêm as notas de imprensa do MRE estruturadas por ano e mês. Ela identificará os anos disponíveis, solicitará um intervalo de análise ao usuário e usará a **API do Gemini** para analisar o contexto de cada nota dentro do intervalo. A API do Gemini fará a filtragem contextual e, **apenas se a nota for relevante**, fará a classificação de alinhamento político (atribuindo uma nota de 1 a 5) **utilizando única e exclusivamente o conteúdo dos parágrafos da nota**.

Ao final, o programa gerará uma planilha (Excel ou CSV) contendo os dados das notas relevantes.

## Onde a API do Gemini será usada?

A API do Gemini será chamada de dentro do próprio script Python. O script lerá cada nota de imprensa dos arquivos JSON locais e enviará apenas o texto dos parágrafos consolidados para a API do Gemini. A API analisará o texto e retornará um JSON estruturado indicando se a nota é relevante e, se sim, a nota atribuída e a justificativa.

## Tecnologias Propostas

- **Python 3.13+**
- **Google GenAI SDK (`google-genai`)**: Para chamadas estruturadas ao Gemini 2.5 Flash.
- **Pydantic**: Para definir o esquema de resposta estruturada do Gemini.
- **python-dotenv**: Para gerenciar a chave de API (`GEMINI_API_KEY`) via arquivo `.env`.
- **pandas** e **openpyxl**: Para salvar os resultados diretamente em formato Excel (`.xlsx`) ou CSV de forma limpa.
- **tqdm**: Para exibir uma barra de progresso visual durante a análise.

## Fluxo do Sistema

```mermaid
graph TD
    A[Início do Programa] --> B[Escaneia diretório json-notas/]
    B --> C[Identifica anos disponíveis]
    C --> D[Solicita intervalo ao usuário]
    D --> E[Carrega arquivos JSON no intervalo]
    E --> F[Para CADA nota: Extrai apenas os PARÁGRAFOS]
    F --> G[Envia os parágrafos para a API do Gemini]
    G --> H{Gemini: É relevante ao tema?}
    H -- Sim --> I[Gemini: Atribui Nota de 1 a 5 e Justificativa]
    I --> J[Script: Adiciona dados à lista de resultados]
    H -- Não --> K[Script: Descarta a nota irrelevante]
    J --> L[Salva progresso incrementalmente]
    K --> L
    L --> M[Gera planilha Excel final]
    M --> N[Fim]
```

## Detalhes de Implementação

### 1. Preparação do Ambiente
- Instalar as dependências: `google-genai`, `python-dotenv`, `pandas`, `openpyxl`, `tqdm`.
- Configurar o arquivo `.env` com a variável `GEMINI_API_KEY`.

### 2. Leitura dos Arquivos
- Mapear os arquivos JSON do diretório `json-notas/`.
- Identificar os anos únicos para exibição inicial e seleção do intervalo.
- Carregar as notas do período selecionado. Para cada nota:
  - Extrair o `titulo`, `link` e `data` (usados apenas para identificação na planilha final).
  - Extrair a lista de `paragrafos` (usados para a análise).

### 3. Filtragem Contextual e Pontuação via Gemini (Baseada apenas nos Parágrafos)
O Gemini analisará o contexto completo de cada nota utilizando **apenas os parágrafos consolidados** da nota à imprensa.
O processo de decisão do Gemini será estruturado da seguinte forma:
1. **Verificação de Relevância**: A nota aborda os conceitos de Governança Global Digital, Governança da IA ou Governança da Internet?
2. **Atribuição de Nota (Apenas se Relevante)**:
   - **Nota 1 (Soberania Digital)**: Foco na soberania digital do Estado, garantias democráticas, direitos fundamentais, abordagens multilaterais e multissetoriais.
   - **Nota 3 (Modelo Misto)**: Equilíbrio entre soberania/direitos e desenvolvimento/inovação (não puramente mercantil).
   - **Nota 5 (Baixa Intervenção Estatal)**: Foco em inovação livre, autorregulação e baixa intervenção estatal.
3. **Justificativa**: Explicação do posicionamento identificado nos parágrafos.

O Gemini responderá usando **Structured Outputs** no seguinte formato JSON:
```json
{
  "relevante": true,
  "nota": 3,
  "justificativa": "A nota menciona..."
}
```

### 4. Geração do Relatório (Tabela Excel)
O programa acumulará os resultados em um arquivo Excel (`relatorio_governanca_digital.xlsx`) ou CSV com as seguintes colunas:
1. **Data**: A data de publicação da nota à imprensa.
2. **Título**: O título da nota à imprensa (para identificação).
3. **Link**: Link de acesso original (para consulta).
4. **Parágrafos**: O texto consolidado dos parágrafos (usado na análise).
5. **Nota Atribuída**: O valor de 1 a 5 atribuído pelo Gemini.
6. **Justificativa**: A explicação do Gemini para a classificação e pontuação baseada nos parágrafos.

### 5. Resiliência e Execução Incremental
- Tratamento automático de erros com recuo exponencial (*exponential backoff*).
- O progresso será salvo de forma incremental para continuar de onde parou em caso de interrupção.

## Plano de Verificação

### Testes Manuais
1. Executar o script `analisador.py`.
2. Verificar a exibição dos anos disponíveis no terminal.
3. Informar um intervalo curto para teste (ex: 2026-2026).
4. Acompanhar a barra de progresso e as chamadas ao Gemini.
5. Inspecionar o arquivo `relatorio_governanca_digital.xlsx` gerado para certificar-se de que os dados estão estruturados de acordo com as colunas solicitadas (incluindo a Data da nota), que a análise foi baseada nos parágrafos e que as notas irrelevantes foram descartadas.
