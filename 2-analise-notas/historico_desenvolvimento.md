# Histórico de Desenvolvimento: Analisador de Governança Global Digital

Este documento registra a evolução, os desafios e as decisões técnicas tomadas durante o desenvolvimento da automação para analisar as notas à imprensa do MRE brasileiro.

## 1. O Objetivo Inicial
O objetivo do projeto era automatizar a leitura e análise de mais de 6.000 notas à imprensa publicadas pelo MRE entre 1997 e 2026. A automação deveria:
- Ler os textos em arquivos JSON.
- Identificar se a nota abordava "Governança Global Digital", "Governança da Inteligência Artificial" ou "Governança da Internet".
- Classificar a postura do MRE em uma escala de 1 a 5 (do foco total em Soberania Digital até o foco em Baixa Intervenção Estatal).
- Exportar os resultados consolidados para uma planilha Excel.

## 2. Primeiras Decisões de Design
- **Filtro de Relevância:** Durante o desenvolvimento, chegamos à conclusão de que pedir ao modelo para dar nota em tudo geraria "alucinações" ou pontuações sem sentido para notas sobre temas aleatórios. Decidimos implementar um sistema de "dois passos estruturados": o modelo primeiro responde `relevante: true/false`. Somente se a resposta for verdadeira, ele atribui a nota (1 a 5) e elabora a justificativa.
- **Extração Focada:** Para evitar informações desnecessárias e melhorar a qualidade da leitura pela Inteligência Artificial, o script foi ajustado para extrair e enviar **apenas os parágrafos de texto puro** das notas.
- **Formatação do Relatório:** A pedido seu, adicionamos a coluna com a "Data" da nota na planilha Excel para facilitar o cruzamento cronológico da pesquisa.

## 3. O Desafio da Autenticação e do Ambiente
No início do projeto, esbarramos no fato de a sua conta Google ser **universitária (Google Workspace)**. Isso bloqueava completamente a criação de projetos na plataforma de nuvem do Google (Google Cloud / AI Studio).
- **A Solução:** Você gerou com sucesso uma chave de API utilizando uma conta Google pessoal (que não tinha os bloqueios institucionais).
- Preparamos o ambiente de programação criando um arquivo `.env` para armazenar a chave da API com segurança (sem deixá-la visível no código).
- Configuramos também um ambiente virtual (`.venv`) contendo as bibliotecas necessárias: `google-genai` (SDK oficial e mais recente do Gemini), `pandas` e `openpyxl` (para manipulação de dados e Excel), e `pydantic` (tecnologia de Structured Outputs que força o Gemini a responder no formato exato que precisamos).

## 4. O Desafio dos Limites da API e Quedas
Ao iniciarmos o processamento das notas do ano de 2026, a camada gratuita do Google começou a bloquear as requisições, alegando que estávamos muito rápidos (Erros 429 - Rate Limit).
- **Evolução: Salvamento Incremental:** Para não perder o trabalho — e não gastar a cota gratuita à toa — sempre que a API derrubasse a conexão, implementei um sistema de persistência no arquivo `progresso_analise.json`. O script passou a registrar os IDs de todas as notas que já avaliou. Assim, em qualquer interrupção, ele retoma exatamente de onde parou, pulando os textos antigos.
- **Evolução: Espera Dinâmica:** Adicionei uma lógica inteligente de recuo para que o script pausasse a execução automaticamente (Backoff) e esperasse os segundos exigidos pela API antes de tentar enviar a mesma nota de novo.

## 5. A Busca pelo Modelo Ideal
O maior "chefão" que enfrentamos foi descobrir quais modelos do Google não impunham limites drásticos à sua conta pessoal nova. Durante a execução, testamos vários "cérebros" do Gemini ao vivo e em tempo real:
1. **`gemini-2.5-flash`**: Modelo inicial potente. Processou as primeiras 29 notas, mas paralisou ao esgotar a cota rigorosa de uso da camada gratuita para aquele modelo (um limite baixíssimo de apenas 20 requisições por dia).
2. **`gemini-1.5-flash`**: Tentativa de retorno ao modelo antigo que permitia 1.500 envios/dia, mas descobrimos que ele estava indisponível no novo SDK (Erro 404).
3. **`gemini-2.0-flash`**: Testamos o modelo base mais novo, mas o Google bloqueou totalmente (Cota zero) contas recentes de usarem esse modelo gratuitamente (Erro 429).
4. **`gemini-2.5-flash-lite`**: Modelo restrito apenas para contas pagas ou legadas (Erro 404).
5. **A Solução Encontrada:** Ao mudar o código final para o **`gemini-flash-lite-latest`**, destravamos a cota! Ele aceitou processar as centenas de notas sem as limitações severas de conta nova.

## 6. Superando o Congestionamento Global
Com o modelo final definido, o Google nos apresentou um último desafio: o **Erro 503 (Serviço Indisponível)**. Isso indicava que o modelo Lite gratuito que escolhemos estava com demanda altíssima nos servidores mundiais.
- **Modificação Final:** Ajustei o código na mosca para tratar o Erro 503 com a mesma paciência do erro de cota. Em vez de abortar o programa por conta de congestionamento do servidor, o script passou a cruzar os braços, esperar 65 segundos na fila, e refazer o pedido até ser aceito.

## 7. Refinamento da Análise e da Planilha
Após a primeira rodada bem-sucedida, identificamos oportunidades de melhoria na qualidade da análise e na estrutura dos dados exportados. Foram implementadas três mudanças:

### 7.1. Ampliação dos Temas Filtrados — Governança de Dados
O escopo temático foi expandido. Originalmente, a IA filtrava notas relacionadas a três governanças: **Global Digital**, **da Inteligência Artificial** e **da Internet**. Com o refinamento, adicionamos a **Governança de Dados** como quarto eixo temático, cobrindo questões como fluxos transfronteiriços de dados, privacidade, soberania sobre dados e regulamentações como a LGPD.

### 7.2. Nova Coluna "Ano" na Planilha
Para facilitar a análise temporal e a criação de gráficos por ano, adicionamos uma coluna **"Ano"** extraída automaticamente da data de cada nota. A coluna "Data" original foi mantida para preservar a informação completa.

### 7.3. Separação das Justificativas em Duas Colunas
Na versão original, havia uma única coluna "Justificativa" que misturava a explicação da relevância com a fundamentação da nota. No refinamento, essa coluna foi desmembrada em:
- **Justificativa da Relevância**: Explica por que a IA considerou a nota relevante aos temas de governança digital.
- **Justificativa da Nota (Evidências)**: Identifica e cita **passagens específicas e trechos literais** do texto original da nota que comprovam e fundamentam a pontuação de 1 a 5 atribuída.

Essa separação foi motivada pela necessidade acadêmica de distinguir a decisão de filtragem (é ou não relevante?) da decisão de classificação (qual nota de 1 a 5?), garantindo que cada uma tenha sua fundamentação própria rastreável.

### 7.4. Impacto nos Resultados
Ao reprocessar as 143 notas de 2026 com as mudanças, o total de notas relevantes permaneceu em **20**, mas a distribuição das notas se alterou ligeiramente (de 8 notas com pontuação 1 para 10, e a única nota 4 foi reclassificada). Isso ocorre porque a mudança na estrutura do prompt (obrigando a IA a citar trechos literais) faz o modelo refletir de forma mais aprofundada, podendo alterar classificações de notas que estavam "na fronteira" entre duas pontuações.

## 8. Criação do Plano de Implementação Online
Além do script local que automatiza a análise em massa via API, foi criado um documento chamado **`implementacao_online.md`**. Esse arquivo é um plano autossuficiente que pode ser colado diretamente em qualquer chat de IA (ChatGPT, Gemini, Claude, etc.) para que a IA execute a mesma análise manualmente, sem necessidade de rodar código. O documento contém:
- A persona do analista (pesquisador sênior de Relações Internacionais).
- As definições conceituais dos quatro eixos de governança.
- A escala completa de 1 a 5.
- O formato de saída esperado (tabela padronizada).
- As regras de rigor analítico (citar trechos literais, não forçar relevância, etc.).

Isso permite que a pesquisadora replique ou valide a análise em outros ambientes sem depender do script Python.

## 9. Conclusão Final
Após essas dezenas de modificações estruturais para lidar com a imprevisibilidade da API gratuita, e os refinamentos de qualidade analítica e de dados, o script tornou-se extremamente robusto. Ele fluiu de forma orgânica, driblou as panes de rede, contornou os limites de cota impeditivos e leu as **143 notas do ano de 2026 sem intervenção humana**, separando impecavelmente as 20 relevantes e ignorando o ruído das 123 inúteis para a pesquisa. A planilha final agora conta com 8 colunas estruturadas (Ano, Data, Título, Link, Parágrafos, Nota Atribuída, Justificativa da Relevância e Justificativa da Nota com Evidências), prontas para análise acadêmica.
