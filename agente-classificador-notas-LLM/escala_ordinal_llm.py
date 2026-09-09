#!/usr/bin/env python3
"""
Gera a escala ordinal semântica (1–5) para as 64 notas relevantes.
 Lê o JSON de verificação e produz CSV + JSON de saída.
"""

import json
import csv
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Parâmetros da escala (definidos pelo usuário)
# ---------------------------------------------------------------------------
ESCALA = {
    1: "Soberania Digital — Soberania digital do Estado, garantias democráticas, direitos fundamentais, multilateralismo, multissetorialismo",
    2: "Predominantemente Soberanista — Foco principal na soberania e direitos, com alguma abertura para inovação",
    3: "Modelo Misto — Equilíbrio entre soberania/direitos e desenvolvimento/inovação (não puramente mercantil)",
    4: "Predominantemente Liberal — Foco principal na inovação e abertura de mercado, com alguma regulação estatal",
    5: "Baixa Intervenção Estatal — Inovação livre, autorregulação, lógica mercantil",
}

# ---------------------------------------------------------------------------
# Avaliação qualitativa de cada nota (atribuída pelo LLM especialista)
# Cada tupla: (nota_escala, justificativa, passagens_relevantes)
# ---------------------------------------------------------------------------
AVALIACOES = {
    1: (
        1,
        "A nota trata de proteção de dados e privacidade como tema de agenda internacional, alinhando-se ao eixo Soberania Digital por enfatizar direitos fundamentais e a necessidade de regulação estatal em contexto de novas tecnologias.",
        [
            "Na agenda internacional, ampliou-se a diversidade de temas e hoje coexistem uma agenda clássica de política externa, com questões ligadas à paz e à segurança internacionais, à integração regional, aos relacionamentos políticos bilaterais e à diplomacia econômica; e uma nova agenda de política externa, associada aos tem..."
        ],
    ),
    2: (
        2,
        "A nota registra cooperação Brasil-Espanha em governança da internet com ênfase em abordagem multissetorial e multilateral. Predomina a preocupação com soberania e direitos, mas há espaço para cooperação técnica e inovação.",
        [
            "13. No plano multilateral, os Ministros mostraram-se dispostos a trabalhar em estreita colaboração a fim de enfrentar os novos desafios globais. Os Ministros mencionaram, entre outros temas, a governança da Internet, e se referiram à Reunião Multissetorial Global sobre o Futuro da Governança da Internet, a ser realizad..."
        ],
    ),
    3: (
        1,
        "A nota aborda reforma das instituições de governança global e segurança das comunicações eletrônicas, com destaque para resolução da ONU sobre privacidade. Predomina o viés soberanista e de direitos fundamentais.",
        [
            "Os Ministros discutirão, igualmente, a reforma das instituições de governança global e temas da agenda de paz e segurança internacionais. Examinarão, ademais, temas afetos ao meio ambiente e à segurança das comunicações eletrônicas. Em dezembro de 2013, a Assembleia Geral da ONU adotou, por consenso, o projeto de resol..."
        ],
    ),
    4: (
        2,
        "A nota registra visita bilateral com menção ao direito à privacidade na era digital como item da agenda. A soberania e os direitos têm precedência, mas o contexto é de cooperação e comércio bilateral.",
        [
            "Também serão discutidas a reforma das instituições de governança global e temas da agenda de paz e segurança internacionais, entre as quais a situação na Síria e no Oriente Médio. Os Chanceleres examinarão, ademais, questões relacionadas ao meio ambiente e ao direito à privacidade na era digital."
        ],
    ),
    5: (
        3,
        "A nota é ampla e abrange infraestrutura digital, comércio e proteção de dados. Há equilíbrio entre soberania/regulação e cooperação para inovação e comércio, sem predomínio claro de nenhum dos polos.",
        [
            "O Brasil e a União Europeia, com a colaboração da indústria privada dos dois lados do Atlântico, reconhecem a importância estratégica e estimulam as partes interessadas relevantes a trabalhar na instalação de um cabo de fibra ótica transatlântico, de alta capacidade, direto, ligando a América do Sul e a Europa. Esse no...",
            "O Brasil e a União Europeia estão comprometidos em reforçar o valor estratégico, a eficiência e o impacto da cooperação no âmbito das TICs.\n  \n  A cooperação em computação em nuvem (cloud computing), padrões de endereçamento, mecanismos de certificação, contratos justos e seguros, bem como arcabouços legislativos será ...",
        ],
    ),
    6: (
        3,
        "O comunicado conjunto da VII Cúpula Brasil-UE aborda governança da internet com modelo multissetorial e cooperação em TICs. Há equilíbrio entre princípios de direitos e cooperação para inovação.",
        [
            "44. We reaffirm our strong belief that Internet governance should be inclusive, transparent, and based on a genuine multi-stakeholder model. In that context, we agreed to cooperate towards the success of the Global Multi-stakeholder Meeting on the Future of Internet Governance to be held in São Paulo on 23-24 April 201...",
            "16. In the domain of ICT cooperation we welcomed the enlarged policy cooperation in Cloud Computing. On ICT infrastructure, we welcomed the plans for the future installation of a fibre-optic submarine cable linking Brazil and Europe, which will improve communications between the two continents, facilitate the take-up o..."
        ],
    ),
    8: (
        2,
        "A Declaração de Fortaleza do BRICS reafirma soberania estatal, direitos humanos online e governança da internet com processo democrático. Predomina o viés soberanista, com referências a inovação e comércio digital.",
        [
            "1. Nós, os líderes da República Federativa do Brasil, da Federação Russa, da República da Índia, da República Popular da China e da República da África do Sul, reunimo-nos em Fortaleza, Brasil, em 15 de julho de 2014 na VI Cúpula do BRICS.",
            "2. Reunião de Altos Representantes Responsáveis por Segurança Nacional do BRICS"
        ],
    ),
    9: (
        2,
        "A declaração Brasil-China aborda privacidade, segurança cibernética e governança da internet com ênfase em soberania e cooperação entre Estados. A dimensão de direitos e soberania é dominante.",
        [
            "35. Os dois Dignitários manifestaram sua preocupação com o uso de tecnologias da informação e da comunicação em atos contrários à manutenção da paz e segurança internacional e prejudiciais aos direitos de privacidade. Coincidiram na necessidade de cooperação para lidar com as ameaças à segurança cibernética, com base n...",
            "36. Os dois Presidentes trocaram impressões sobre os resultados da Reunião Multissetorial Global sobre o Futuro da Governança da Internet – NETmundial (São Paulo, 23 e 24 de abril de 2014) e concordaram em aprofundar o diálogo bilateral sobre temas relativos à governança da Internet."
        ],
    ),
    10: (
        1,
        "A nota celebra relatório da ONU sobre direito à privacidade na era digital, resultado de resolução de iniciativa brasileira. Foco explícito em direitos humanos, soberania e regulação de vigilância estatal.",
        [
            "O Governo brasileiro manifesta satisfação com a divulgação, em 16/7, em Genebra, pela Alta Comissária para os Direitos Humanos das Nações Unidas, Navi Pillay, do relatório \"O direito à privacidade na era digital\". Trata-se de resposta à solicitação da resolução apresentada por Brasil e Alemanha durante a 68ª Assembleia..."
        ],
    ),
    18: (
        3,
        "O comunicado do Diálogo Estratégico Brasil-UK aborda governança da internet, política cibernética e proteção de dados com abordagem multissetorial. Há equilíbrio entre direitos e cooperação para inovação.",
        [
            "Internet Governance",
            "Reino Unido e Brasil desempenham papel de liderança na condução da agenda internacional sobre política cibernética."
        ],
    ),
    19: (
        1,
        "A nota registra criação de relatoria especial da ONU para privacidade na era digital, com foco em direitos humanos, soberania estatal e proteção contra vigilância. Posicionamento fortemente soberanista.",
        [
            "Enfatizando que os Estados devem respeitar suas obrigações internacionais de direitos humanos quanto ao direito à privacidade quando interceptam comunicações digitais dos indivíduos e/ou coletam dados pessoais",
            "Profundamente preocupados com o impacto negativo que a vigilância e/ou interceptação de comunicações, incluindo vigilância e/ou interceptação de comunicações extraterritoriais, assim como a coleta de dados pessoais, em particular quando conduzida em grande escala, pode ter sobre o exercício e o gozo dos direitos humano..."
        ],
    ),
    26: (
        5,
        "A nota é predominantemente sobre comércio eletrônico e cooperação econômica entre países do BRICS. Sem menção a soberania digital ou direitos; foco em lógica mercantil e facilitação de comércio.",
        [
            "3. Diálogo de Peritos do BRICS sobre comércio eletrônico (Moscou, 14 de abril de 2015)."
        ],
    ),
    27: (
        2,
        "A Declaração de Ufá reafirma soberania, direitos humanos e governança da internet com processo aberto e democrático. Predomina o viés soberanista, com referências a TICs e cooperação.",
        [
            "Apoiamos a evolução contínua do ecossistema de governança da Internet, o qual deve se basear em processo aberto e democrático, livre da influência de quaisquer considerações unilaterais.",
            "Reconhecemos a necessidade urgente de fortalecer ainda mais a cooperação em áreas de TICs, inclusive a Internet, que sejam do interesse de nossos países."
        ],
    ),
    30: (
        2,
        "A nota registra cooperação Brasil-Alemanha em privacidade e temas cibernéticos, com foco em soberania e direitos, mas com abertura para cooperação técnica bilateral.",
        [
            "Tendo presente a exitosa cooperação entre Brasil e Alemanha sobre o direito à privacidade na era digital, as Chefes de Governo decidiram estabelecer mecanismo bilateral de consultas e de cooperação sobre temas cibernéticos."
        ],
    ),
    43: (
        1,
        "A nota reafirma resolução da ONU sobre privacidade na era digital e projeta marco regulatório brasileiro para proteção de dados. Foco explícito em soberania, direitos e regulação estatal.",
        [
            "Em atenção à preocupação brasileira com o tema, atualmente tramitam no Congresso Nacional projetos de lei que visam à criação de um marco regulatório eficiente e moderno para a proteção de dados pessoais."
        ],
    ),
    47: (
        3,
        "A Declaração do G20 sobre mundo interconectado aborda digitalização, dados e economia digital com menção a proteção de dados. Há equilíbrio entre desenvolvimento e regulação, sem predomínio claro.",
        [
            "PreâmbuloNós, os Líderes do G20, reunimo-nos em Hamburgo, Alemanha, de 7 a 8 de julho de 2017, para tratar dos grandes desafios econômicos globais e contribuir para a prosperidade e o bem-estar."
        ],
    ),
    53: (
        2,
        "A IX Cúpula BRICS aborda governança da IA, proteção de dados e economia digital com ênfase em soberania e cooperação entre Estados do Sul Global. Predomina o viés soberanista.",
        [
            "21. Em plena era da economia digital, estamos prontos para usar as oportunidades por ela fornecidas e enfrentar os desafios por ela impostos para o crescimento global.",
            "13. Reafirmamos o nosso compromisso com a cooperação industrial do BRICS, incluindo em capacidades e políticas industriais"
        ],
    ),
    59: (
        4,
        "O comunicado Brasil-Singapura foca em cooperação econômica e investimentos no setor digital. Predomina a lógica de abertura de mercado e atração de investimentos, com pouca menção a regulação ou direitos.",
        [
            "4. O ministro Nunes Ferreira saudou os investimentos de Singapura no Brasil. As empresas de Singapura são participantes ativos em vários setores importantes no Brasil, incluindo óleo e gás, infraestrutura, setor imobiliário, agricultura e transportes."
        ],
    ),
    63: (
        4,
        "O evento sobre Grupos de Engajamento do G20 discute economia digital e comércio com participação do setor privado e sociedade civil. Foco em inovação e cooperação econômica, com regulação estatal secundária.",
        [
            "O G20 constitui foro para a cooperação internacional em temas econômicos e financeiros e congrega países desenvolvidos e em desenvolvimento com maior projeção na economia mundial."
        ],
    ),
    64: (
        4,
        "A X Cúpula BRICS aborda blockchain, comércio digital e tributação da economia digital. Predomina a perspectiva econômica e de inovação, com menção a regulação tributária.",
        [
            "73. We welcome the signing of the Memorandum of Understanding on Collaborative Research on Distributed Ledger and Blockchain Technology in the Context of the Development of the Digital Economy.",
            "83. We acknowledge the continued support provided by the BRICS Revenue Authorities for all the international initiatives towards reaching a globally fair and universally transparent tax system."
        ],
    ),
    68: (
        1,
        "A nota registra decisão da ICANN sobre domínio .Amazon e posicionamento brasileiro de defesa de soberania sobre nomes de domínio relacionados à região amazônica. Foco explícito em soberania estatal e interesses nacionais.",
        [
            "Em 10 de março, o Conselho Diretor da Corporação da Internet para Atribuição de Nomes e Números (ICANN) adotou resolução a respeito da atribuição do nome de domínio de primeiro nível “.Amazon” à empresa Amazon Inc."
        ],
    ),
    69: (
        1,
        "A nota detalha posição brasileira sobre domínio .Amazon, defendendo interesses dos países da OTCA e criticando decisão da ICANN. Forte viés soberanista com defesa de direitos de povos e identidade regional.",
        [
            "O Ministério das Relações Exteriores foi informado de que a empresa Amazon Inc. submeteu à Corporação da Internet para Atribuição de Nomes e Números (ICANN), em 17/4/2019, proposta para obter o domínio de primeiro nível .AMAZON, que, na visão do Brasil, não atende preocupações importantes dos países da..."
        ],
    ),
    70: (
        3,
        "A nota sobre comércio eletrônico na OMC apresenta proposta brasileira que aborda proteção de consumidor, dados pessoais, segurança cibernética e cooperação tecnológica. Há equilíbrio entre regulação e facilitação do comércio.",
        [
            "A proposta brasileira resultou de ampla coordenação interna entre diversos órgãos de governo. Aborda questões como proteção do consumidor e de dados pessoais, além de questões tributárias e relacionadas à segurança cibernética e à cooperação tecnológica."
        ],
    ),
    71: (
        1,
        "A nota lamenta decisão da ICANN sobre domínio .Amazon, critica debilitação da abordagem multissetorial e defende soberania dos países amazônicos. Posicionamento fortemente soberanista e de defesa de direitos.",
        [
            "O Ministério das Relações Exteriores lamenta a decisão da Corporação da Internet para Atribuição de Nomes e Números (ICANN), adotada em 17 de maio de 2019, de atribuir o nome de domínio de primeiro nível .Amazon à empresa Amazon Inc., em regime de exclusividade e na ausência de uma solução mutuamente ace...",
            "O Brasil tem sido um firme defensor da abordagem multissetorial para a governança da Internet, com a participação plena das múltiplas partes interessadas"
        ],
    ),
    75: (
        4,
        "A Declaração de Osaka sobre Economia Digital foca em potencial dos dados e digitalização para crescimento econômico e inovação. Predomina a perspectiva de liberalização e maximização de benefícios econômicos.",
        [
            "Afirmamos a importância de promover discussões políticas nacionais e internacionais para aproveitar todo o potencial dos dados e da economia digital para promover a inovação",
            "Com base nesses esforços, nos engajaremos em debates sobre políticas internacionais a fim de aproveitar todo o potencial dos dados e da economia digital"
        ],
    ),
    78: (
        3,
        "A nota apresenta proposta brasileira sobre facilitação do comércio por meio de tecnologias digitais na OMC. Há equilíbrio entre regulação e facilitação, com foco em eficiência e boas práticas.",
        [
            "O Brasil apresentou na segunda-feira, 7 de outubro, na Organização Mundial do Comércio (OMC), proposta acerca de disciplinas para a facilitação do comércio por meio de tecnologias digitais"
        ],
    ),
    79: (
        4,
        "A XI Cúpula BRICS tem como lema 'Crescimento Econômico para um Futuro Inovador' com economia digital como área prioritária. Predomina a perspectiva de inovação e crescimento econômico.",
        [
            "O Brasil exerce, este ano, a presidência de turno do BRICS, sob o lema 'Crescimento Econômico para um Futuro Inovador'. As áreas prioritárias de trabalho são: ciência, tecnologia e inovação; economia digital"
        ],
    ),
    80: (
        4,
        "A Declaração de Brasília do BRICS foca em crescimento econômico, comércio e inovação. Predomina a perspectiva de liberalização e promoção de investimentos em infraestrutura e serviços digitais.",
        [
            "38. Saudamos a realização do Fórum Empresarial do BRICS e reconhecemos os esforços do Conselho Empresarial do BRICS (CEBRICS) para promover o comércio e o investimento entre seus membros"
        ],
    ),
    82: (
        1,
        "A nota sobre adesão à Convenção de Budapeste aborda crimes cibernéticos com foco em cooperação jurídica internacional e persecução penal. Predomina a perspectiva de soberania estatal e proteção de cidadãos.",
        [
            "A iniciativa de adesão do Brasil à Convenção de Budapeste vem somar-se à Lei no 12.965/2014, o Marco Civil da Internet, para a persecução penal dos crimes cibernéticos."
        ],
    ),
    86: (
        4,
        "O Memorando Brasil-Chile sobre telecomunicações e economia digital foca em cooperação técnica, infraestrutura e inovação (5G, IoT, IA). Predomina a perspectiva de desenvolvimento e integração de mercados.",
        [
            "O instrumento permitirá aprofundar a cooperação bilateral em áreas estratégicas para os dois países, tais como conexão digital, infraestrutura de telecomunicações, conectividade e fluxo de dados entre os dois países."
        ],
    ),
    87: (
        3,
        "O V Diálogo Estratégico Brasil-UK aborda IA, proteção de dados, economia digital e cibersegurança com abordagem de cooperação bilateral. Há equilíbrio entre direitos e inovação.",
        [
            "13. Both sides agreed to strengthen security cooperation to counter regional and international threats. The ministers welcomed the deepening bilateral collaboration regarding the use of artificial intelligence, data protection, digital economy and digital access"
        ],
    ),
    90: (
        4,
        "A nota sobre visita do subsecretário americano aborda economia digital, 5G e Clean Network com foco em cooperação技术ica e alinhamento geopolítico. Predomina a perspectiva de abertura de mercado e alianças estratégicas.",
        [
            "Tanto no exercício JUSBE, quanto no âmbito bilateral, Brasil e EUA discutiram novos temas, como economia digital e 5G. O Brasil apoia os princípios contidos na proposta do Clean Network feita pelo EUA"
        ],
    ),
    92: (
        3,
        "A Declaração de Moscou do BRICS reconhece economia digital como ferramenta de modernização e crescimento inclusivo. Há equilíbrio entre desenvolvimento e menção a Objetivos de Desenvolvimento Sustentável.",
        [
            "66. Reconhecemos o papel da economia digital como uma ferramenta importante para a modernização e transformação da indústria, promoção do crescimento econômico inclusivo"
        ],
    ),
    94: (
        3,
        "O Acordo de Comércio Eletrônico do MERCOSUL cria ambiente regulatório para comércio digital com proteção de consumidor. Há equilíbrio entre facilitação do comércio e proteção de direitos.",
        [
            "O objetivo do acordo é criar um ambiente mais seguro para o desenvolvimento do comércio eletrônico entre os estados partes, que beneficie tanto suas empresas quanto seus consumidores."
        ],
    ),
    95: (
        4,
        "A adesão ao cabo Humboldt foca em infraestrutura física de telecomunicações e conectividade. Predomina a perspectiva de desenvolvimento de infraestrutura e integração regional sem componente regulatório.",
        [
            "A adesão brasileira ao projeto do cabo 'Humboldt' vem somar-se a outras importantes iniciativas do governo brasileiro, como o leilão de frequências de 5G"
        ],
    ),
    96: (
        2,
        "A XIII Cúpula BRICS aborda TICs com foco em ambiente aberto, seguro e acessível, com menção a soberania e segurança. Predomina o viés soberanista com referências a cooperação e desenvolvimento.",
        [
            "27. Reafirmamos nosso compromisso com a promoção de um ambiente de TIC aberto, seguro, estável, acessível e pacífico."
        ],
    ),
    100: (
        1,
        "A nota registra aprovação do Senado da Convenção de Budapeste com foco em governança digital e proteção de cidadãos. Posicionamento soberanista com fortalecimento do marco normativo nacional.",
        [
            "A Convenção de Budapeste, até o momento, foi ratificada por 66 países. Com a adesão do Brasil, a Convenção soma-se ao importante marco normativo já adotado pelo País em matéria de governança e de proteção de direitos em meio digital"
        ],
    ),
    104: (
        4,
        "O seminário sobre cadeia de semicondutores foca em segurança de suprimentos e competitividade industrial. Predomina a perspectiva econômica e de política industrial sem componente regulatório de direitos.",
        [
            "Por sua propriedade físico-química singular e sua aplicação múltipla, trata-se de componente central para o pleno funcionamento da economia digital."
        ],
    ),
    105: (
        2,
        "A Declaração Conjunta do BRICS sobre IA apoia cooperação técnica e reconhece potencial da tecnologia, com menção a desenvolvimento. Predomina o viés soberanista com referência a capacitação de países em desenvolvimento.",
        [
            "18. The Ministers supported information exchanges and technical cooperation on AI technology."
        ],
    ),
    106: (
        2,
        "A Declaração de Pequim do BRICS aborda Big Data, IA e economia digital com foco em desenvolvimento sustentável e soberania. Predomina o viés soberanista com referências a cooperação Sul-Sul.",
        [
            "57. We take note that the breakthroughs in the applications of digital technologies, such as Big Data and Artificial Intelligence (AI) may play an important role towards sustainable development.",
            "38. Reconhecemos o dinamismo da economia digital para mitigar o impacto do COVID-19 e permitir a recuperação econômica global."
        ],
    ),
    109: (
        4,
        "A Declaração do G20 de Bali foca em transformação digital, inclusão digital e conectividade como fatores de crescimento. Predomina a perspectiva de liberalização e maximização de oportunidades econômicas.",
        [
            "24. The COVID-19 pandemic has accelerated the transformation of the digital ecosystem and digital economy. We recognize the importance of digital transformation in reaching the SDGs."
        ],
    ),
    111: (
        4,
        "A Declaração Brasil-China foca em economia digital e cooperação em investimentos digitais. Predomina a perspectiva de abertura de mercados e atração de investimentos com foco em desenvolvimento econômico.",
        [
            "24. As duas partes reconheceram os pontos em comum e a complementaridade na área de economia digital e saudaram a assinatura de Memorando de Entendimento sobre o Fortalecimento da Cooperação em Investimentos na Economia Digital"
        ],
    ),
    119: (
        3,
        "A Aliança Digital ALC-UE é abrangente e aborda governança da internet, IA, dados, cibersegurança e infraestrutura com visão centrada no ser humano. Há equilíbrio entre direitos e inovação.",
        [
            "The EU-LAC Digital Alliance promotes cooperation on a wide range of digital issues, including digital policy dialogue, internet governance, data governance, infrastructure, connectivity, security, data protection, artificial intelligence",
            "A Aliança Digital ALC-UE baseia-se em uma visão comum da economia e sociedade digitais, centrada no ser humano"
        ],
    ),
    123: (
        4,
        "A Declaração de Joanesburgo II do BRICS foca em dinamismo da economia digital e papel do comércio e investimento. Predomina a perspectiva de liberalização e crescimento econômico.",
        [
            "33. We recognize the dynamism of the digital economy in enabling global economic growth."
        ],
    ),
    125: (
        1,
        "A nota sobre adesão à Parceria para Informação e Democracia foca em direitos humanos, liberdade de expressão, proteção de jornalistas e confiabilidade da informação. Posicionamento fortemente soberanista e de direitos.",
        [
            "O Brasil integra grupos de países que lideram, em diferentes foros multilaterais, e em particular no âmbito das Nações Unidas, iniciativas dedicadas ao direito à privacidade, à liberdade de expressão, à proteção de jornalistas, ao acesso à informação"
        ],
    ),
    130: (
        2,
        "A Declaração Ministerial do G77 aborda cooperação digital, capacitação e governança de dados com foco em soberania e desenvolvimento. Predomina o viés soberanista com referência atransferência de tecnologia.",
        [
            "51. The Ministers reaffirmed that, the important issues pertaining to digital cooperation remain, inter alia: inclusive digital economy, including the creation of capacities for MSMEs",
            "52. The Ministers looked forward to the development of a global digital compact through an open, transparent and inclusive intergovernmental process."
        ],
    ),
    133: (
        1,
        "A Declaração Especial do MERCOSUL sobre Democracia e Integridade da Informação foca em direitos humanos, proteção de dados, desinformação e responsabilidade de empresas de tecnologia. Posicionamento fortemente soberanista.",
        [
            "COINCIDIRAM na urgência de promover ações conjuntas, a partir de uma perspectiva de direitos humanos, para a construção da confiança cidadã, a proteção de dados pessoais e a promoção da integridade",
            "DECIDIRAM incentivar políticas transparentes, responsáveis e respeitosas dos direitos humanos por parte das empresas de tecnologia"
        ],
    ),
    135: (
        2,
        "O discurso do Ministro Mauro Vieira no G20 aborda multilateralismo, paz e cooperação com referência a direitos humanos. Predomina o viés soberanista e de direitos fundamentais.",
        [
            "Prezados colegas, Sem paz e cooperação, será extremamente difícil alcançarmos a prometida mobilização em larga escala dos recursos necessários para enfrentar as ameaças existenciais que enfrentamos"
        ],
    ),
    141: (
        3,
        "O comunicado Brasil-Japão aborda governança da internet, IA e infraestrutura digital com abordagem centrada no ser humano e inclusiva. Há equilíbrio entre soberania, direitos e inovação.",
        [
            "74. The two leaders reaffirmed the need for a human-centered, inclusive, development-oriented, responsible and ethical approach to the use and development of digital technologies, including Artificial Intelligence"
        ],
    ),
    145: (
        1,
        "A nota sobre participação na Cúpula do Futuro aborda Pacto para o Futuro com temas de direitos humanos, ciência e tecnologia digital e governança global. Posicionamento soberanista e de defesa de multilateralismo.",
        [
            "O Pacto aborda temas como desenvolvimento sustentável; direitos humanos; paz e segurança internacionais; ciência, tecnologia e cooperação digital; juventude e gerações futuras; e reforma da governança global."
        ],
    ),
    146: (
        2,
        "A reunião de ministros do G20 sobre reforma da governança global aborda multilateralismo e fortalecimento de instituições. Predomina o viés soberanista com foco em governança democrática.",
        [
            "The challenges the global community faces today can only be addressed through multilateral solutions for a better tomorrow and the strengthening of global governance for both present and future generations."
        ],
    ),
    148: (
        2,
        "A XVI Cúpula do BRICS abrange governança da internet, IA, dados e cibersegurança com foco em soberania e multilateralismo. Predomina o viés soberanista com referências acooperação e desenvolvimento.",
        [
            "78. Reconhecendo que a rápida mudança tecnológica, incluindo o rápido avanço da Inteligência Artificial, tem o potencial de trazer novas oportunidades para o desenvolvimento socioeconômico em todo o mundo",
            "71. Concerned with the fast-paced digitalization process of all aspects of human life in the 21st century, we underscore the key role of data for development"
        ],
    ),
    149: (
        3,
        "A Declaração sobre DPI, IA e Dados para Governança aborda infraestrutura pública digital com foco em desenvolvimento e inclusão. Há equilíbrio entre soberania e promoção de inovação para desenvolvimento.",
        [
            "Accelerating progress towards the SDGs requires inclusive digital transformation.",
            "Key to this deployment is the establishment of fair and equitable principles for data governance to address data protection and management, privacy and security"
        ],
    ),
    151: (
        4,
        "Os atos da visita de Estado Brasil-China focam em memorandos de cooperação na economia digital e comércio. Predomina a perspectiva de abertura e integração de mercados digitais.",
        [
            "19) Memorando de Entendimento sobre o Fortalecimento da Cooperação na Economia Digital entre o Ministério das Comunicações da República Federativa do Brasil e a Administração Nacional de Dados da República Popular da China"
        ],
    ),
    154: (
        3,
        "O Diálogo Digital Brasil-UE aborda IA, plataformas digitais, conectividade e confiança na economia digital. Há equilíbrio entre desafios regulatórios e oportunidades de inovação.",
        [
            "Este Diálogo acontece em um momento crítico, marcado por avanços rápidos sem precedentes em tecnologias digitais, em particular da Inteligência Artificial (IA) e de plataformas digitais",
            "Ambos os lados reconhecem o papel fundamental da conectividade na era digital"
        ],
    ),
    156: (
        2,
        "O discurso do Ministro no G20 aborda IA, governança de dados e inovação com foco em soberania e inclusão. Predomina o viés soberanista com referência a solidariedade e igualdade.",
        [
            "Ladies and gentlemen, The Rio de Janeiro Leaders' Declaration acknowledged the need for the G20 to further discuss 'artificial intelligence, data governance, and innovation'.",
            "A Declaração de Líderes do Rio de Janeiro reconheceu a necessidade de o G20 aprofundar as discussões sobre 'inteligência artificial, governança de dados e inovação'."
        ],
    ),
    159: (
        4,
        "O seminário sobre economia de dados foca em criação de mercados de dados e valorização estratégica para desenvolvimento. Predomina a perspectiva de inovação e transformação digital com foco econômico.",
        [
            "Durante o seminário, foram discutidos a criação de espaços e mercados de dados e o papel dos dados na transformação digital de empresas e governos.",
            "A valorização estratégica dos dados é essencial para reduzir assimetrias econômicas e garantir que os benefícios desse novo modelo de negócios sejam amplamente..."
        ],
    ),
    161: (
        2,
        "A Declaração da Presidência BRICS aborda IA com foco em responsabilidade, segurança e capacitação de países em desenvolvimento. Predomina o viés soberanista com referência a cooperação e desenvolvimento.",
        [
            "56. The Ministers emphasized that Artificial Intelligence (AI) is instrumental for promoting socio-economic development and inclusive growth in all societies",
            "57. The Ministers looked forward to BRICS cooperation to help developing countries strengthen AI capacity building."
        ],
    ),
    162: (
        4,
        "A Declaração Brasil-China foca em cooperação econômica, comércio e investimentos com menção a economia digital. Predomina a perspectiva de abertura de mercados e integração econômica.",
        [
            "6. As partes reconheceram a importância de continuar a desenvolver de maneira cada vez mais estável as relações econômico-comerciais bilaterais.",
            "31. Durante a visita, as partes assinaram ou chegaram a consenso sobre uma série de atos de cooperação em áreas como desenvolvimento sustentável, finanças, economia digital"
        ],
    ),
    163: (
        4,
        "A participação na OCDE e OMC aborda sistema de comércio internacional e economia digital. Predomina a perspectiva de integração econômica e participação em fóruns de cooperação econômica.",
        [
            "Na ministerial da OCDE, o Ministro Mauro Vieira estará presente na cerimônia de abertura e em sessões de trabalho sobre temas como sistema de comércio internacional e economia digital."
        ],
    ),
    165: (
        1,
        "A Declaração dos Líderes do BRICS sobre Governança Global da IA tem soberania digital como tema central, com foco em direitos fundamentais, direito ao desenvolvimento e marcos regulatórios nacionais.",
        [
            "Digital Sovereignty and the Right to Development are Central to Global AI Governance. We firmly support the right of all countries to harness the benefits of the digital economy and emerging technologies, particularly Artificial Intelligence, while upholding fundamental rights, to establish their own regulatory framewo..."
        ],
    ),
    166: (
        2,
        "A Declaração do Rio de Janeiro do BRICS aborda IA como oportunidade de desenvolvimento com foco em cooperação e mitigação de riscos. Predomina o viés soberanista com referência a países do Sul Global.",
        [
            "16. We recognize that Artificial Intelligence (AI) represents a milestone opportunity to boost development towards a more prosperous future.",
            "4. We underline the significance of the adoption of the BRICS Leaders' Framework Declaration on Climate Finance and of the BRICS Leaders' Statement on the Global Governance of Artificial Intelligence"
        ],
    ),
    175: (
        4,
        "A seleção do projeto UNESCO foca em uso de TICs na educação com análise crítica sobre IA e apoio à equidade. Predomina a perspectiva de inovação educacional com menção a inclusão social.",
        [
            "A seleção do projeto brasileiro, baseado na análise crítica sobre a aplicação da IA e no apoio à equidade e à inclusão, reflete a importância atribuída pelo Brasil às tecnologias digitais como aliadas do desenvolvimento social e educacional."
        ],
    ),
    176: (
        3,
        "A premiação UNESCO de ética na IA foca em governança inclusiva e uso ético e responsável da tecnologia. Há equilíbrio entre desenvolvimento e responsabilidade ética, com foco em direitos.",
        [
            "A premiação do professor Virgílio Almeida reflete o compromisso do governo brasileiro com a governança inclusiva e com o uso ético e responsável da inteligência artificial e de tecnologias digitais na atualidade"
        ],
    ),
}


def main():
    # Diretórios
    base = Path("/workspaces/governanca-digital_mre/agente-classificador-notas-LLM")
    entrada = base / "resultados" / "verificacoes" / "verificacao_llm-2026-09-01.json"
    saida_csv = base / "resultados" / "escala-ordinal_llm-2026-09-01.csv"
    saida_json = base / "resultados" / "escalas-ordinais" / "escala-ordinal-llm-2026-09-01.json"

    with open(entrada, "r", encoding="utf-8") as f:
        dados = json.load(f)

    notas = dados["notas_relevantes"]
    resultados = []
    dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for nota in notas:
        nid = nota["id"]
        if nid not in AVALIACOES:
            print(f"AVISO: nota id={nid} sem avaliação definida!")
            continue

        nota_esc, justificativa, passagens = AVALIACOES[nid]
        descricao = ESCALA[nota_esc]

        resultados.append({
            "titulo": nota["titulo"],
            "link": nota["link"],
            "data": nota["data"],
            "nota_escala": nota_esc,
            "descricao_nota": descricao,
            "justificativa": justificativa,
            "passagens_relevantes": passagens,
        })
        dist[nota_esc] += 1

    # --- CSV ---
    with open(saida_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["Titulo", "Link", "Data", "Nota_Escala", "Descricao_Nota", "Justificativa", "Passagens_Relevantes"])
        for r in resultados:
            # Limpar newlines das passagens para não quebrar o CSV
            passagens_limpa = []
            for p in r["passagens_relevantes"]:
                passagens_limpa.append(p.replace("\n", " ").replace("\r", " ").strip())
            writer.writerow([
                r["titulo"],
                r["link"],
                r["data"],
                r["nota_escala"],
                r["descricao_nota"],
                r["justificativa"].replace("\n", " ").strip(),
                " | ".join(passagens_limpa),
            ])

    # --- JSON ---
    saida_json.parent.mkdir(parents=True, exist_ok=True)
    with open(saida_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    # --- Resumo ---
    print(f"Total avaliado: {len(resultados)}")
    print(f"Distribuição:")
    for nota_val in sorted(dist):
        print(f"  Nota {nota_val}: {dist[nota_val]} notas")
    print(f"Parâmetros usados:")
    for k, v in ESCALA.items():
        print(f"  {k}: {v}")
    print(f"Arquivos gerados:")
    print(f"  CSV:   {saida_csv}")
    print(f"  JSON:  {saida_json}")


if __name__ == "__main__":
    main()
