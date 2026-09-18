# Relatório de Validação da Escala Ordinal

**Modelo validador:** muse-spark-1.3-contributor-free (temperature=0)
**Data:** 2026-09-18
**Arquivo de escala ordinal:** escala-ordinal-muse-spark-1.3-contributor-free-2026-09-17.json
**Arquivo de filtragem heurística:** json-filtragem-heuristico-2026-09-10.json
**Contexto:** contexto01.md

**Parâmetros confirmados pelo usuário:**
- 1: Soberania Digital - Soberania digital do Estado, garantias democráticas, direitos fundamentais, multilateralismo, multissetorialismo
- 2: Predominantemente Soberanista - Foco principal na soberania e direitos, com alguma abertura para inovação
- 3: Modelo Misto - Equilíbrio entre soberania/direitos e desenvolvimento/inovação (não puramente mercantil)
- 4: Predominantemente Liberal - Foco principal na inovação e abertura de mercado, com alguma regulação estatal
- 5: Baixa Intervenção Estatal - Inovação livre, autorregulação, lógica mercantil

## Resumo Executivo

- Total de notas avaliadas: **178**
- Notas coerentes: **178** (100.0%)
- Notas inconsistentes: **0** (0.0%)
- Notas alteradas: **0**

Validação com triangulação (escala ordinal × filtragem heurística + leitura integral dos `paragrafos`). Viés conservador aplicado em casos limítrofes.

## Distribuição das Notas

| Nota | Antes da Validação | Depois da Validação |
|------|-------------------|--------------------|
| 1 | 22 (12.4%) | 22 (12.4%) |
| 2 | 59 (33.1%) | 59 (33.1%) |
| 3 | 63 (35.4%) | 63 (35.4%) |
| 4 | 32 (18.0%) | 32 (18.0%) |
| 5 | 2 (1.1%) | 2 (1.1%) |

## Padrões Identificados

### noticias institucionais (único classificado, n=178)
- Distribuição: {1: 22, 2: 59, 3: 63, 4: 32, 5: 2}
- Nota mais comum: 3
- Granularidade preservada: mesmo `classificado` gera 5 níveis distintos conforme conteúdo dos parágrafos — sem falha de granularidade.

### Casos limítrofes revisados e mantidos
- VII Cúpula Brasil-UE 20/04/2014 (nota 3): vocabulário liberal intenso compensado por nuvem/cabo/privacidade — equilíbrio misto confirmado.
- G20 Roma 02/11/2021 e Riade 22/11/2020 (nota 3): fluxos livres + privacidade/segurança em equilíbrio explícito.
- Paraguai 04/10/2016 (nota 2): fibra óptica estatal para inclusão, não liberalização.
- Moscou BRICS 17/11/2020 e Pequim 13/05/2025 (nota 2): cooperação digital subordinada a multilateralismo/soberania.
- Osaka 29/06/2019 e Pacote EUA 19/10/2020 (nota 5): lógica mercantil pura sem salvaguardas — extremos corretos.

## Inconsistências

Nenhuma inconsistência identificada. `notas_coerentes + notas_inconsistentes = 178` conferido.

## Recomendações

- Manter a escala sem alterações.
- Refinar futuramente a fronteira 2 vs 3 para menções passageiras a privacidade em notas protocolares.
- Auditoria reprodutível: JSONs de entrada e saída preservados.

## Reprodutibilidade

- `temperature=0`; modelo+versão e data nos arquivos.
- JSONs de entrada e saída mantidos para auditoria.
