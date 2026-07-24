# Sugestões de Visualizações para Análise de Instabilidade Política

## Contexto da Pesquisa

**Tema:** Posicionamento do Ministério das Relações Exteriores (MRE) do Brasil em relação à Governança Global Digital (2014-2025)

**Período Analisado:** 24/10/2024 a 07/11/2024 (15 dias)

**Dados Disponíveis:** 637 notícias classificadas quanto à instabilidade política:
- SIM: 9 notícias (1,4%)
- POSSIVEL: 4 notícias (0,6%)
- NÃO: 624 notícias (98,0%)

---

## Sugestões de Visualizações

### 1. Timeline de Instabilidade Política
- **Tipo:** Gráfico de linha temporal
- **Dados:** Notícias classificadas como "SIM" e "POSSIVEL" ao longo dos 15 dias
- **Justificativa:** Permite visualizar a distribuição temporal dos eventos de instabilidade, identificando concentração em datas específicas (ex: período pós-eleitoral nos EUA em 05/11/2024)
- **Relevância para pesquisa:** Mostra o contexto político interno durante o período analisado

### 2. Mapa de Calor por Dia da Semana
- **Tipo:** Heatmap
- **Dados:** Quantidade de notícias por dia da semana e classificação
- **Justificativa:** Identifica padrões de publicação e concentração de eventos
- **Relevância:** Ajuda a entender a dinâmica de notícias políticas no período

### 3. Distribuição de Classificações
- **Tipo:** Gráfico de pizza ou barras
- **Dados:** Proporção SIM/POSSIVEL/NÃO
- **Justificativa:** Visão geral da predominância de instabilidade política
- **Relevância:** Quantifica o nível de instabilidade no período

### 4. Análise Temática das Notícias SIM/POSSIVEL
- **Tipo:** Lista temática ou nuvem de palavras (simplificada)
- **Dados:** Principais temas das notícias classificadas como instáveis
- **Justificativa:** Identifica quais temas específicos estão associados à instabilidade
- **Relevância:** Conecta temas específicos com o contexto de governança digital

### 5. Correlação com Eventos Internacionais
- **Tipo:** Linha do tempo comparativa
- **Dados:** Eventos de instabilidade no Brasil vs. eventos internacionais (ex: eleições EUA em 05/11/2024)
- **Justificativa:** Contextualiza a instabilidade brasileira em eventos globais
- **Relevância:** Diretamente ligada à governança global digital

### 6. Gráfico de Tendência com Janela Móvel
- **Tipo:** Gráfico de linha com média móvel
- **Dados:** Notícias de instabilidade ao longo do período
- **Justificativa:** Suaviza flutuações diárias e mostra tendência
- **Relevância:** Identifica se há escalada ou redução de tensões

### 7. Análise por Fonte/Origem
- **Tipo:** Gráfico de barras horizontais
- **Dados:** Distribuição de notícias por tema (política internacional, economia, etc.)
- **Justificativa:** Identifica quais áreas temáticas geram mais notícias de instabilidade
- **Relevância:** Conecta temas com o foco da pesquisa em governança digital

### 8. Dashboard Resumo Executivo
- **Tipo:** Painel com KPIs
- **Dados:** Total de notícias, % instáveis, tema mais frequente, dia com mais eventos
- **Justificativa:** Visão consolidada para tomada de decisão
- **Relevância:** Facilita a apresentação dos resultados

---

## Bibliotecas Python Sugeridas

| Biblioteca | Uso Principal | Justificativa |
|------------|---------------|---------------|
| **matplotlib** | Gráficos estáticos | Flexibilidade total para personalização |
| **seaborn** | Estatísticas visuais | Gráficos estatísticos bonitos com pouco código |
| **pandas** | Manipulação de dados | Processamento e análise dos dados CSV |
| **plotly** | Gráficos interativos | Visualizações interativas para exploração |
| **wordcloud** | Nuvens de palavras | Análise textual das notícias |
| **calmap** | Mapas de calor | Visualização temporal em formato calendário |

---

## Observações

1. **Foco em dados qualitativos:** As visualizações devem priorizar a compreensão do contexto político sobre estatísticas complexas
2. **Simplicidade:** Evitar visualizações muito complexas que possam confundir a interpretação
3. **Conexão com pesquisa:** Cada visualização deve estar claramente conectada ao objetivo de entender o posicionamento do MRE em governança digital
4. **Período específico:** Os dados cobrem apenas 15 dias, portanto visualizações temporais devem considerar essa limitação

---

## Arquivo de Dados para Visualização

- **Arquivo:** `analise_instabilidade_politica.csv`
- **Localização:** `agentes-ia/`
- **Formato:** CSV com colunas: data, titulo, classificacao, justificativa, link