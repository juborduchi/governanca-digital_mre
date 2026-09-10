# Validação Semântica da Filtragem Heurística — Verificação por LLM

**Data de execução:** 2026-09-01  
**Modelo:** llm  
**Arquivo de entrada:** `resultados/jsons-filtrados/json-filtragem-heuristico-2026-09-01.json`  
**Contexto:** `contextos/contexto01.md`

---

## Resumo Executivo

| Métrica | Valor |
|---------|-------|
| Total de notas avaliadas | 178 |
| Notas relevantes (mantidas) | 64 |
| Falsos positivos (removidos) | 114 |
| Percentual removido | 64.0% |

**Critério de classificação:** Falso positivo = nota cujo objeto central NÃO é tema digital de Governança Global Digital (o digital é incidente/menção lateral; ou é calendário/agenda sem posicionamento substantivo; ou é duplicada).

---

## Padrões Identificados

1. **Comunicados bilaterais amplos:** Muitas notas filtradas são comunicados que mencionam governança digital como item lateral em agenda de múltiplos temas, sem posicionamento substantivo do MRE.
2. **Atos assinados em visitas de Estado:** Notas com múltiplos acordos assinados em visitas bilaterais, onde o digital não é o foco.
3. **Rodadas negociadoras de ALC:** Menções a comércio eletrônico como capítulo em negociação, sem posicionamento sobre governança digital.
4. **Cúpulas do MERCOSUL:** Comunicados sobre integração regional sem conteúdo digital relevante.
5. **Participações em reuniões multilaterais:** Filtradas por menções pontuais a temas digitais.

---

## Lista de Falsos Positivos (114 notas)

| # | ID | Título | Data | Motivo |
|---|-----|--------|------|--------|
| 1 | 7 | Reino Unido sedia reunião de Diálogo Estratégico com o Brasil | 22/05/2014 | Diálogo Estratégico amplo; cibersegurança mencionada como item lateral sem posicionamento substantiv... |
| 2 | 11 | Visita ao Brasil do Primeiro-Ministro do Japão, Shinzo Abe – Comunicado Conjunto... | 07/08/2014 | Comunicado bilateral Brasil-Japão amplo; sem seção dedicada a governança digital. |
| 3 | 12 | Documentos aprovados na XLVI Cúpula de Chefes de Estado do MERCOSUL e Estados As... | 07/08/2014 | Documentos da Cúpula MERCOSUL sobre integração regional; sem conteúdo sobre governança digital. |
| 4 | 13 | Discurso proferido pela Presidenta da República, Dilma Rousseff, na abertura do ... | 08/10/2014 | Discurso na AGNU sobre temas gerais de política externa; sem menção substantiva a governança digital... |
| 5 | 14 | Documentos aprovados na XLVII Cúpula de Chefes de Estado do MERCOSUL e Estados A... | 18/12/2014 | Documentos da Cúpula MERCOSUL sobre integração e energia; sem conteúdo sobre governança digital. |
| 6 | 15 | Discurso de Sua Excelência o Senhor Embaixador Mauro Luiz Iecker Vieira, por oca... | 02/01/2015 | Discurso de posse do Ministro; sem menção a temas de governança digital. |
| 7 | 16 | Documentos aprovados na I Reunião dos Ministros das Relações Exteriores do Foro ... | 12/01/2015 | Documentos do Foro CELAC-China sobre cooperação Sul-Sul; sem conteúdo sobre governança digital. |
| 8 | 17 | Visita ao Brasil do Ministro do Exterior da República Federal da Alemanha, Frank... | 12/02/2015 | Visita para preparação de Consultas Intergovernamentais; sem conteúdo sobre governança digital. |
| 9 | 20 | Acordo Marco de Cooperação com a OCDE | 08/04/2015 | Acordo marco de cooperação com a OCDE em geral; sem foco em governança digital. |
| 10 | 21 | 13º Congresso de Prevenção do Crime e Justiça Criminal - Doha, 12 a 19 de abril ... | 16/04/2015 | Congresso sobre prevenção do crime e justiça criminal; sem foco em crimes cibernéticos. |
| 11 | 22 | Acordo Comercial Expandido Brasil-México – Cidade do México, 26 de maio de 2015 | 26/05/2015 | Acordo comercial Brasil-México sobre comércio de bens; sem foco em comércio eletrônico. |
| 12 | 23 | Ata da Quarta Reunião da Comissão Sino-Brasileira de Alto Nível de Concertação e... | 26/06/2015 | Ata da COSBAN com múltiplos temas; sem seção dedicada a governança digital. |
| 13 | 24 | Atos assinados por ocasião da visita da Presidenta Dilma Rousseff aos Estados Un... | 30/06/2015 | Atos de visita Brasil-EUA sobre previdência e DH; sem conteúdo sobre governança digital. |
| 14 | 25 | Comunicado Conjunto da Presidenta Dilma Rousseff e do Presidente Barack Obama – ... | 30/06/2015 | Comunicado bilateral amplo Brasil-EUA; sem seção dedicada a governança digital. |
| 15 | 28 | Comunicado Conjunto das Presidentas e dos Presidentes dos Estados Partes do MERC... | 18/07/2015 | Comunicado do MERCOSUL sobre integração regional; sem conteúdo sobre governança digital. |
| 16 | 29 | Visita ao Brasil do Secretário Especial para a América Latina e Assuntos Consula... | 21/07/2015 | Visita sobre assuntos consulares e passaportes; sem conteúdo sobre governança digital. |
| 17 | 31 | Visita ao Brasil de Sua Alteza Real o Príncipe Herdeiro da Noruega – Brasília, 1... | 13/11/2015 | Visita de cortesia do Príncipe Herdeiro da Noruega; sem conteúdo sobre governança digital. |
| 18 | 32 | Negociação Brasil-México para ampliação e aprofundamento do ACE-53 – Troca de Li... | 19/12/2015 | Negociação comercial Brasil-México sobre comércio de bens; sem foco em comércio eletrônico. |
| 19 | 33 | Resultados da X Conferência Ministerial da Organização Mundial do Comércio – Nai... | 19/12/2015 | Conferência Ministerial da OMC sobre comércio agrícola; sem foco em comércio eletrônico. |
| 20 | 34 | Visita do Ministro das Relações Exteriores à Etiópia, ao Marrocos e à Tunísia – ... | 04/03/2016 | Visita ministerial a três países africanos; sem conteúdo sobre governança digital. |
| 21 | 35 | XII Reunião de Ministros das Relações Exteriores dos Países Membros da OTCA - El... | 20/05/2016 | Declaração da OTCA sobre cooperação amazônica; sem conteúdo sobre governança digital. |
| 22 | 36 | V Cúpula do Fórum de Diálogo Índia, Brasil e África do Sul (IBAS) – Declaração d... | 30/05/2016 | Declaração do IBAS sobre cooperação Sul-Sul; sem conteúdo sobre governança digital. |
| 23 | 37 | Discurso do Ministro José Serra durante a Reunião Ministerial da Organização Mun... | 02/06/2016 | Discurso sobre comércio internacional e OMC em geral; sem foco em comércio eletrônico. |
| 24 | 38 | Comunicado dos Líderes do G20 – Cúpula de Hangzhou – 4-5 de setembro de 2016 | 08/09/2016 | Comunicado do G20 Hangzhou; sem seção dedicada a governança digital. |
| 25 | 39 | Intervenção do ministro das Relações Exteriores, José Serra, na reunião de chanc... | 20/09/2016 | Intervenção em reunião de chanceleres do BRICS; sem foco em governança digital. |
| 26 | 40 | Visita do Presidente da República ao Paraguai - Assunção, 3 de outubro de 2016 -... | 04/10/2016 | Ato assinado sobre conectividade; sem posicionamento substantivo sobre governança digital. |
| 27 | 41 | Visita do Presidente da República à Índia – Goa, 17 de outubro de 2016 – Comunic... | 17/10/2016 | Comunicado bilateral Brasil-Índia; sem seção dedicada a governança digital. |
| 28 | 42 | Declaração conjunta do presidente da República Federativa do Brasil e do primeir... | 01/11/2016 | Declaração bilateral Brasil-Portugal; sem conteúdo sobre governança digital. |
| 29 | 44 | Declaração conjunta aprovada por ocasião da VI Cúpula Brasil–União Europeia - Br... | 01/06/2017 | Declaração da VI Cúpula Brasil-UE de 2013; sem seção dedicada a governança digital. |
| 30 | 45 | Visita do ministro Aloysio Nunes Ferreira aos Estados Unidos – Washington, 2 de ... | 01/06/2017 | Visita bilateral para reunião de trabalho; sem conteúdo sobre governança digital. |
| 31 | 46 | Itamaraty apoia empreendedorismo brasileiro no exterior | 06/07/2017 | Nota sobre guias de empreendedorismo; sem conteúdo sobre governança digital. |
| 32 | 48 | Declaração de Hamburgo dos Líderes do G20 sobre a Luta contra o Terrorismo | 08/07/2017 | Declaração sobre luta contra o terrorismo; sem conteúdo sobre governança digital. |
| 33 | 49 | Documentos finais da XXII Reunião Ordinária do Conselho de Ministros da Comunida... | 20/07/2017 | Documentos da CPLP; sem conteúdo sobre governança digital. |
| 34 | 50 | V Cúpula Brasil-União Europeia – Declaração Conjunta e Plano de Ação Conjunta – ... | 04/08/2017 | Declaração da V Cúpula Brasil-UE de 2011; sem seção dedicada a governança digital. |
| 35 | 51 | Atos assinados por ocasião da visita ao Brasil da Ministra das Relações Exterior... | 15/08/2017 | Atos de cooperação técnica Brasil-Colômbia; sem conteúdo sobre governança digital. |
| 36 | 52 | Atos assinados por ocasião da visita do presidente Michel Temer à China – Pequim... | 03/09/2017 | Atos de visita bilateral Brasil-China sobre vistos; sem conteúdo sobre governança digital. |
| 37 | 54 | Reunião ministerial da OMC em Marraquexe | 08/10/2017 | Reunião ministerial da OMC sobre negociações gerais; sem foco em comércio eletrônico. |
| 38 | 55 | Visita do Ministro Aloysio Nunes Ferreira à Itália – Comunicado Conjunto | 13/11/2017 | Comunicado bilateral Brasil-Itália; sem conteúdo sobre governança digital. |
| 39 | 56 | Atos assinados por ocasião da visita do Presidente do Estado Plurinacional da Bo... | 05/12/2017 | Atos de cooperação Brasil-Bolívia; sem conteúdo sobre governança digital. |
| 40 | 57 | LI Cúpula de Chefes de Estado do MERCOSUL e Estados Associados e LI Reunião Ordi... | 15/12/2017 | Nota sobre realização de Cúpula do MERCOSUL; sem conteúdo sobre governança digital. |
| 41 | 58 | Acordo entre a República Federativa do Brasil e o estado de Israel de Previdênci... | 27/02/2018 | Acordo de previdência social Brasil-Israel; sem conteúdo sobre governança digital. |
| 42 | 60 | Lançamento das negociações de um Acordo de Comércio entre   o Mercosul e a Repúb... | 25/05/2018 | Lançamento de negociações MERCOSUL-Coreia; sem foco em governança digital. |
| 43 | 61 | I Rodada Negociadora do Acordo de Livre Comércio  Brasil-Chile – Brasília, 6 a 8... | 08/06/2018 | Rodada negociadora ALC Brasil-Chile; sem posicionamento substantivo sobre governança digital. |
| 44 | 62 | Comunicado Conjunto dos Presidentes dos Estados Partes do MERCOSUL e Bolívia – A... | 18/06/2018 | Comunicado do MERCOSUL sobre integração regional; sem conteúdo sobre governança digital. |
| 45 | 65 | II Rodada Negociadora do Acordo de Livre Comércio Brasil-Chile – Santiago, 7 a 1... | 13/08/2018 | Segunda rodada negociadora ALC Brasil-Chile; sem foco em governança digital. |
| 46 | 66 | III Rodada de Negociações do Acordo de Livre Comércio Brasil-Chile – Brasilia, 1... | 14/09/2018 | Terceira rodada negociadora ALC Brasil-Chile; sem foco em governança digital. |
| 47 | 67 | Acordo de Livre Comércio Brasil-Chile [Declaração à imprensa] | 21/11/2018 | Declaração sobre conclusão do ALC Brasil-Chile; sem posicionamento sobre governança digital. |
| 48 | 72 | Reunião Informal de Líderes do BRICS à margem do G20 – Osaka, 28 de junho de 201... | 26/06/2019 | Nota prévia sobre reunião informal do BRICS; sem conteúdo sobre governança digital. |
| 49 | 73 | Cúpula do G20 em Osaka | 26/06/2019 | Nota prévia sobre participação no G20; sem posicionamento substantivo sobre governança digital. |
| 50 | 74 | Reunião informal de líderes do BRICS à margem da Cúpula do G20 – Comunicado conj... | 28/06/2019 | Comunicado informal do BRICS; sem posicionamento sobre governança digital. |
| 51 | 76 | Declaração de Osaka dos Líderes do G20 | 29/06/2019 | Declaração do G20 ampla; sem seção dedicada a governança digital. |
| 52 | 77 | Comunicado conjunto dos Presidentes dos Estados Partes do MERCOSUL e Estados Ass... | 17/07/2019 | Comunicado do MERCOSUL sobre integração; sem conteúdo sobre governança digital. |
| 53 | 81 | MERCOSUL – Documentos adotados na Cúpula do Vale dos Vinhedos – Bento Gonçalves,... | 05/12/2019 | Documentos do MERCOSUL; sem conteúdo sobre governança digital. |
| 54 | 83 | III Conferência Ministerial Hemisférica de Luta contra o Terrorismo – Comunicado... | 20/01/2020 | Conferência sobre luta contra o terrorismo; sem foco em terrorismo cibernético. |
| 55 | 84 | Cúpula extraordinária dos líderes do G20 - Declaração sobre COVID-19 | 26/03/2020 | Declaração sobre resposta à pandemia COVID-19; sem conteúdo sobre governança digital. |
| 56 | 85 | Declaração Conjunta Brasil-Uruguai sobre cooperação para estabelecimento de plat... | 15/07/2020 | Cooperação sobre plataforma de proteção ao consumidor; sem posicionamento sobre governança digital. |
| 57 | 88 | Assinatura de Pacote Comercial com os EUA – Nota Conjunta do Ministério das Rela... | 19/10/2020 | Pacote comercial Brasil-EUA; sem foco em comércio eletrônico ou governança digital. |
| 58 | 89 | Lançamento do Diálogo Trilateral Brasil-Estados Unidos-Japão (JUSBE) | 10/11/2020 | Lançamento de diálogo trilateral; sem conteúdo sobre governança digital. |
| 59 | 91 | XII Cúpula do BRICS | 17/11/2020 | Nota sobre realização da XII Cúpula do BRICS; sem conteúdo sobre governança digital. |
| 60 | 93 | Declaração de Líderes do G20 da Cúpula de Riade – 22/11/2020 | 22/11/2020 | Declaração do G20 sobre recuperação pós-COVID; sem seção dedicada a governança digital. |
| 61 | 97 | Segunda parte da Reunião Ministerial  do Conselho da OCDE | 07/10/2021 | Reunião ministerial da OCDE; sem foco em governança digital. |
| 62 | 98 | Comunicado Conjunto Brasil-Argentina por ocasião da visita a Brasília do Ministr... | 08/10/2021 | Comunicado bilateral Brasil-Argentina; sem conteúdo sobre governança digital. |
| 63 | 99 | Declaração dos Líderes do G20 Roma | 02/11/2021 | Declaração do G20 Roma; sem seção dedicada a governança digital. |
| 64 | 101 | LIX Cúpula de Chefes de Estado do MERCOSUL e Estados Associados e LIX Reunião Or... | 17/12/2021 | Comunicado do MERCOSUL sobre integração; sem conteúdo sobre governança digital. |
| 65 | 102 | Comunicado Conjunto Dos Presidentes Dos Estados Partes Do Mercosul E Estados Ass... | 17/12/2021 | Comunicado do MERCOSUL sobre integração; sem conteúdo sobre governança digital. |
| 66 | 103 | Nota conjunta do Ministério das Relações Exteriores, da Casa Civil e do Ministér... | 25/01/2022 | Nota sobre convite para acessão à OCDE; sem foco em governança digital. |
| 67 | 107 | Declaração Conjunta sobre Cooperação em Cadeias de Suprimentos Globais | 21/07/2022 | Declaração sobre cadeias de suprimentos; sem foco em governança digital. |
| 68 | 108 | Nota conjunta do Ministério das Relações Exteriores, da Casa Civil, do Ministéri... | 06/10/2022 | Nota sobre Memorando Inicial OCDE; sem foco em governança digital. |
| 69 | 110 | Atos assinados por ocasião da viagem do senhor Presidente da República à Repúbli... | 23/01/2023 | Atos de visita Brasil-Argentina; sem conteúdo sobre governança digital. |
| 70 | 112 | Lista e íntegra dos atos assinados no Grande Palácio do Povo, por ocasião da vis... | 14/04/2023 | Lista de atos assinados na China; sem foco em governança digital. |
| 71 | 113 | Lista e íntegra dos atos assinados no Centro Cultural de Belém, em 22 de abril d... | 22/04/2023 | Atos de cooperação Brasil-Portugal; sem conteúdo sobre governança digital. |
| 72 | 114 | Lista e íntegra dos atos assinados por ocasião da visita do Presidente Luiz Inác... | 26/04/2023 | Atos de cooperação Brasil-Espanha; sem conteúdo sobre governança digital. |
| 73 | 115 | Consenso de Brasília – 30 de maio de 2023 | 30/05/2023 | Consenso sobre integração sul-americana; sem conteúdo sobre governança digital. |
| 74 | 116 | Declaração Conjunta do Cabo da Boa Esperança – Ministros das Relações Exteriores... | 02/06/2023 | Declaração dos chanceleres do BRICS; sem seção dedicada a governança digital. |
| 75 | 117 | Discurso do Ministro das Relações Exteriores por ocasião da LXII Reunião Ordinár... | 03/07/2023 | Discurso no CMC do MERCOSUL; sem conteúdo sobre governança digital. |
| 76 | 118 | Comunicado Conjunto dos Estados Partes Argentina, Brasil e Paraguai | 04/07/2023 | Comunicado do MERCOSUL; sem conteúdo sobre governança digital. |
| 77 | 120 | Declaração da Cúpula CELAC-UE 2023 | 18/07/2023 | Declaração da Cúpula CELAC-UE; sem seção dedicada a governança digital. |
| 78 | 121 | Declaração Presidencial por ocasião da Cúpula da Amazônia – IV Reunião de Presid... | 08/08/2023 | Declaração sobre Amazônia; sem conteúdo sobre governança digital. |
| 79 | 122 | XIX Reunião do Conselho de Ministros da ALADI | 18/08/2023 | Reunião da ALADI; sem conteúdo sobre governança digital. |
| 80 | 124 | Atos assinados por ocasião da visita de Estado do senhor Presidente da República... | 25/08/2023 | Atos de cooperação Brasil-Angola; sem conteúdo sobre governança digital. |
| 81 | 126 | Declaração de Líderes do G20 de Nova Delhi - Nova Delhi, Índia - 9 e 10 de setem... | 09/09/2023 | Declaração do G20 Nova Delhi; sem seção dedicada a governança digital. |
| 82 | 127 | Declaração de Havana sobre “os desafios atuais para o desenvolvimento: o papel d... | 16/09/2023 | Declaração do G77 sobre CT&I; sem foco em governança digital. |
| 83 | 128 | Reunião de Chanceleres do BRICS à margem da 78ª Sessão da Assembleia Geral das N... | 20/09/2023 | Comunicado dos chanceleres do BRICS; sem seção dedicada a governança digital. |
| 84 | 129 | 11ª Reunião da Comissão Ministerial Trilateral do Fórum de Diálogo Índia-Brasil-... | 22/09/2023 | Reunião da Comissão IBAS; sem conteúdo sobre governança digital. |
| 85 | 131 | Comunicado conjunto por ocasião da conclusão da visita do Presidente do Brasil à... | 01/12/2023 | Comunicado Brasil-Arábia Saudita; sem conteúdo sobre governança digital. |
| 86 | 132 | Comunicado Conjunto dos Presidentes dos Estados Partes do Mercosul e Bolívia | 07/12/2023 | Comunicado do MERCOSUL; sem conteúdo sobre governança digital. |
| 87 | 134 | Adoção do Documento “Áreas de Cooperação Prática” no âmbito da Parceria de Diálo... | 15/12/2023 | Documento de cooperação com ASEAN; sem foco em governança digital. |
| 88 | 136 | Declaração Conjunta e Declaração de Seguimento da Parceria Estratégica Renovada ... | 06/03/2024 | Declaração bilateral Brasil-Espanha; sem seção dedicada a governança digital. |
| 89 | 137 | Atos adotados por ocasião da visita ao Brasil do Presidente da França, Emmanuel ... | 28/03/2024 | Atos de visita Brasil-França; sem foco em governança digital. |
| 90 | 138 | Declaração Conjunta dos Presidentes de Brasil e Colômbia | 17/04/2024 | Declaração bilateral Brasil-Colômbia; sem conteúdo sobre governança digital. |
| 91 | 139 | Atos adotados por ocasião da visita do presidente Luiz Inácio Lula da Silva à Co... | 18/04/2024 | Atos de visita Brasil-Colômbia; sem conteúdo sobre governança digital. |
| 92 | 140 | Atos adotados por ocasião da visita da Ministra de Relações Internacionais e Coo... | 23/04/2024 | Atos de visita da Ministra da África do Sul; sem conteúdo sobre governança digital. |
| 93 | 142 | Declaração Conjunta dos Presidentes do Estado Plurinacional da Bolívia e da Repú... | 09/07/2024 | Declaração bilateral Brasil-Bolívia; sem conteúdo sobre governança digital. |
| 94 | 143 | Comunicado Conjunto da XXIX Reunião Ordinária do Conselho de Ministros da Comuni... | 19/07/2024 | Comunicado da CPLP; sem conteúdo sobre governança digital. |
| 95 | 144 | Declaração Conjunta dos Presidentes da República Federativa do Brasil, Luiz Inác... | 05/08/2024 | Declaração bilateral Brasil-Chile; sem conteúdo sobre governança digital. |
| 96 | 147 | Reunião de ministros das Relações Exteriores do IBAS à margem da 79ª AGNU – Nova... | 26/09/2024 | Reunião do IBAS à margem da AGNU; sem conteúdo sobre governança digital. |
| 97 | 150 | Reunião de líderes do IBAS – Comunicado de Imprensa – Rio de Janeiro, 19 de nove... | 19/11/2024 | Reunião de líderes do IBAS; sem conteúdo sobre governança digital. |
| 98 | 152 | Comunicado conjunto Brasil - Emirados Árabes Unidos por ocasião da reunião de lí... | 27/11/2024 | Comunicado Brasil-EAU no G20; sem conteúdo sobre governança digital. |
| 99 | 153 | Comunicado Conjunto dos Presidentes dos Estados Partes do Mercosul | 06/12/2024 | Comunicado do MERCOSUL; sem conteúdo sobre governança digital. |
| 100 | 155 | I Comissão Permanente Bilateral Brasil-Espanha – Ata Final – Madri, 17 de fevere... | 17/02/2025 | Ata da Comissão Brasil-Espanha; sem foco em governança digital. |
| 101 | 157 | Discurso proferido pelo Ministro Mauro Vieira por ocasião da 1ª reunião de Sherp... | 25/02/2025 | Discurso na reunião de Sherpas do BRICS; sem foco em governança digital. |
| 102 | 158 | Assinatura de acordo de cooperação entre a Polícia Federal e a EUROPOL – Nota Co... | 05/03/2025 | Acordo PF-EUROPOL; cooperação policial sem foco em governança digital. |
| 103 | 160 | Declaração Conjunta por ocasião da Visita de Estado do Presidente do Chile, Gabr... | 24/04/2025 | Declaração bilateral Brasil-Chile; sem conteúdo sobre governança digital. |
| 104 | 164 | Comunicado Conjunto da Cúpula Brasil–Caribe | 13/06/2025 | Comunicado da Cúpula Brasil-Caribe; sem conteúdo sobre governança digital. |
| 105 | 167 | Parceria do BRICS para a Eliminação de Doenças Socialmente Determinadas | 07/07/2025 | Parceria do BRICS para eliminação de doenças; sem conteúdo sobre governança digital. |
| 106 | 168 | Declaração conjunta por ocasião da visita de Estado do Primeiro-Ministro da Índi... | 08/07/2025 | Declaração bilateral Brasil-Índia; sem seção dedicada a governança digital. |
| 107 | 169 | Comunicado Conjunto entre a República Federativa do Brasil e a República da Indo... | 09/07/2025 | Comunicado bilateral Brasil-Indonésia; sem conteúdo sobre governança digital. |
| 108 | 170 | Participação do Presidente Luiz Inácio Lula da Silva na Reunião de Alto Nível so... | 19/07/2025 | Participação em reunião sobre democracia; sem conteúdo sobre governança digital. |
| 109 | 171 | Reunião de Alto Nível "Democracia Sempre" - Declaração Conjunta - Santiago, 21 d... | 21/07/2025 | Declaração sobre democracia em Santiago; sem conteúdo sobre governança digital. |
| 110 | 172 | Declaração Conjunta dos Presidentes da República Federativa do Brasil e da Repúb... | 20/08/2025 | Declaração bilateral Brasil-Equador; sem conteúdo sobre governança digital. |
| 111 | 173 | Declaração de Bogotá — V Reunião de Presidentes dos Estados Partes do Tratado de... | 23/08/2025 | Declaração da Cúpula da Amazônia; sem conteúdo sobre governança digital. |
| 112 | 174 | Eleição do novo diretor-geral da UNESCO, Khaled El-Enany | 06/10/2025 | Nota sobre eleição de DG da UNESCO; sem conteúdo sobre governança digital. |
| 113 | 177 | XIII Diálogo de Alto Nível sobre Direitos Humanos entre o Brasil e a União Europ... | 07/11/2025 | Diálogo de DH Brasil-UE; sem foco em governança digital. |
| 114 | 178 | Marco da Parceria Estratégica entre o Japão e o MERCOSUL | 20/12/2025 | Parceria Estratégica Japão-MERCOSUL; sem conteúdo sobre governança digital. |

---

## Consistência

- Notas relevantes: 64
- Falsos positivos: 114
- **Total: 64 + 114 = 178** ✓

---

*Gerado automaticamente pela verificação semântica LLM em 2026-09-01.*
