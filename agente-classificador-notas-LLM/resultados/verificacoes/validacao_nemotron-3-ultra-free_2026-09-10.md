# Relatório de Validação Semântica (LLM)

**Modelo:** nemotron-3-ultra-free  
**Data:** 2026-09-10  
**Arquivo de entrada:** json-filtragem-heuristico-2026-09-01.json

## Resumo Executivo

- **Total de notas avaliadas:** 178
- **Notas relevantes (mantidas):** 156
- **Falsos positivos (removidos):** 22 (12.4%)

## Falsos Positivos Identificados

| Título | Data | Motivo |
|--------|------|--------|
| Reino Unido sedia reunião de Diálogo Estratégico com o Brasil | 22/05/2014 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Documentos aprovados na I Reunião dos Ministros das Relações Exteriores do Foro CELAC-China - Pequim, 8 e 9 de janeiro de 2015 [inglês] | 12/01/2015 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Visita ao Brasil do Secretário Especial para a América Latina e Assuntos Consulares, Passaporte e Vistos da Índia – Comunicado Conjunto – Brasília, 20 e 21 de julho de 2015 | 21/07/2015 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Visita do Ministro das Relações Exteriores à Etiópia, ao Marrocos e à Tunísia – 8 a 11 de março de 2016 | 04/03/2016 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Intervenção do ministro das Relações Exteriores, José Serra, na reunião de chanceleres dos BRICS à margem da 71ª Assembleia Geral das Nações Unidas – Nova York, 20 de setembro de 2016 [Inglês] | 20/09/2016 | Menção digital incidental em nota sobre outro tema (comércio, energia, agenda bilateral geral) |
| Visita do Presidente da República ao Paraguai - Assunção, 3 de outubro de 2016 - Ato Assinado | 04/10/2016 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Visita do ministro Aloysio Nunes Ferreira aos Estados Unidos – Washington, 2 de junho de 2017 | 01/06/2017 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Atos assinados por ocasião da visita do presidente Michel Temer à China – Pequim, 31 de agosto a 3 de setembro de 2017 | 03/09/2017 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Reunião ministerial da OMC em Marraquexe | 08/10/2017 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| LI Cúpula de Chefes de Estado do MERCOSUL e Estados Associados e LI Reunião Ordinária do Conselho do Mercado Comum do MERCOSUL | 15/12/2017 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Reunião Informal de Líderes do BRICS à margem do G20 – Osaka, 28 de junho de 2019 | 26/06/2019 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Visita do Subsecretário para Crescimento Econômico, Energia e Meio Ambiente do Departamento de Estado dos EUA, Keith Krach, ao Brasil, de 9 a 11 de novembro de 2020 | 10/11/2020 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Segunda parte da Reunião Ministerial  do Conselho da OCDE | 07/10/2021 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| LIX Cúpula de Chefes de Estado do MERCOSUL e Estados Associados e LIX Reunião Ordinária do Conselho do Mercado Comum - Comunicado de Imprensa de Argentina, Brasil e Paraguai | 17/12/2021 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Discurso do Ministro das Relações Exteriores por ocasião da LXII Reunião Ordinária do Conselho do Mercado Comum (CMC) - Sessão com Estados Partes - Puerto Iguazú, 3 de julho de 2023 | 03/07/2023 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| XIX Reunião do Conselho de Ministros da ALADI | 18/08/2023 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Reunião de Chanceleres do BRICS à margem da 78ª Sessão da Assembleia Geral das Nações Unidas – Comunicado Conjunto – Nova York, 20 de setembro de 2023 | 20/09/2023 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| 11ª Reunião da Comissão Ministerial Trilateral do Fórum de Diálogo Índia-Brasil-África do Sul (IBAS) - Nova York, 22 de setembro de 2023 | 22/09/2023 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Declaração Ministerial da 47ª reunião anual do G77 - Nova York, 22 de setembro de 2023 | 23/09/2023 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Comunicado conjunto por ocasião da conclusão da visita do Presidente do Brasil à Arábia Saudita – Riade, 30 de novembro de 2023 | 01/12/2023 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Segunda reunião de ministros das Relações Exteriores do G20 – Chamado à Ação sobre a Reforma da Governança Global - Nova York, 25 de setembro | 25/09/2024 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |
| Participação do Presidente Luiz Inácio Lula da Silva na Reunião de Alto Nível sobre Democracia, em Santiago | 19/07/2025 | Calendário/agenda de evento sem posicionamento substantivo sobre governança digital |

## Padrões Identificados

- Maioria das notas relevantes trata de soberania digital, privacidade, proteção de dados e governança multilateral da internet
- Falsos positivos concentrados em notas de agenda bilateral geral, comércio tradicional, energia, agricultura onde 'digital' aparece apenas incidentalmente
- Notas sobre cooperação em ciência/tecnologia/educação sem foco em governança digital foram classificadas como FP

## Recomendações

- Refinar filtragem heurística para excluir notas de agenda bilateral sem conteúdo digital substantivo
- Palavras-chave como 'tecnologia', 'inovação', 'cooperação' sozinhas geram muitos falsos positivos
- Incluir termos mais específicos: 'governança da internet', 'soberania digital', 'proteção de dados', 'comércio digital'
