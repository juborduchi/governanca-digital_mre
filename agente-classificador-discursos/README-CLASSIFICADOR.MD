# Classificador de Discursos, Artigos e Entrevistas do MRE

## Objetivo

Este agente é responsável por realizar a filtragem e classificação de discursos, artigos e entrevistas do Ministério das Relações Exteriores (MRE) do Brasil, identificando documentos pertinentes à **Governança Global Digital** e classificando-os numa escala ordinal de alinhamento político.

## Estrutura

```
agente-classificador-discursos/
├── README-CLASSIFICADOR.MD          # Este arquivo
├── contextos/
│   └── contexto01.md                # Contexto de pesquisa: Governança Global Digital
├── skill/
│   ├── skill_filtro.md              # Skill da filtragem de documentos
│   ├── executar_filtro.py           # Script de execução da filtragem
│   ├── skill_testagem.md            # Skill de validação da filtragem
│   ├── validar_filtragem.py         # Script de execução da validação da filtragem
│   ├── escalar_ordinal.py           # Script de execução da escala ordinal
│   └── validar_escala.py            # Script de execução da validação da escala
├── prompts/
│   ├── prompt01.md                  # Skill da escala ordinal
│   └── testagem_prompt.md           # Skill de validação da escala ordinal
├── resultados/
│   ├── filtragem_[tipo]_[modelo]-[data].csv
│   ├── escala-ordinal-[tipo]_[modelo]-[data].csv
│   ├── jsons-filtrados/
│   │   └── json-filtragem-[tipo]_[modelo]-[data].json
│   ├── verificacoes/
│   │   ├── validacao_[tipo]_[modelo]-[data].md
│   │   ├── notas-relevantes_[tipo]_[modelo]-[data].csv
│   │   └── verificacao_[tipo]_[modelo]-[data].json
│   └── verificacoes-ordinais/
│       ├── validacao_escala-[tipo]_[modelo]-[data].md
│       ├── correcao_escala-[tipo]_[modelo]-[data].csv
│       └── correcao_escala-[tipo]_[modelo]-[data].json
├── ignorar/
├── sessões/
└── visualizacao/
```

## Pipeline de Análise

### Estágio 1: Filtragem
- **Arquivo**: `skill/skill_filtro.md` + `skill/executar_filtro.py`
- **Entrada**: JSONs de discursos, artigos e entrevistas do MRE (2014-2025)
- **Filtros**: Tipo de documento (discurso/artigo/entrevista) + período + contexto de pesquisa
- **Método**: Pré-seleção por vocabulário substantivo + filtro de calendários
- **Saída**: CSV + JSON com documentos pertinentes

### Estágio 2: Escala Ordinal
- **Arquivo**: `prompts/prompt01.md` + `skill/escalar_ordinal.py`
- **Entrada**: Documentos filtrados no Estágio 1
- **Escala**: 1 (Soberania Digital) ↔ 5 (Baixa Intervenção Estatal)
- **Método**: Pontuação por vocabulário ponderado (soberanista vs. liberal)
- **Saída**: CSV + JSON com notas 1-5

### Estágio 3: Validação da Filtragem
- **Arquivo**: `skill/skill_testagem.md` + `skill/validar_filtragem.py`
- **Ação**: Auditoria independente dos documentos filtrados
- **Saída**: Relatório MD + CSV + JSON de verificação

### Estágio 4: Validação da Escala
- **Arquivo**: `prompts/testagem_prompt.md` + `skill/validar_escala.py`
- **Ação**: Reavaliação independente da escala ordinal
- **Saída**: Relatório MD + CSV + JSON de correção

## Tipos de Documento

O campo `categoria` do JSON original identifica o tipo de cada documento:
- **discursos** - Discursos oficiais de autoridades do MRE
- **artigos** - Artigos publicados por representantes do MRE
- **entrevistas** - Entrevistas concedidas por representantes do MRE

## Uso

### Executar Filtragem (para um tipo específico)
```bash
python3 skill/executar_filtro.py discursos
python3 skill/executar_filtro.py artigos
python3 skill/executar_filtro.py entrevistas
python3 skill/executar_filtro.py todos
```

### Executar Escala Ordinal
```bash
python3 skill/escalar_ordinal.py discursos
python3 skill/escalar_ordinal.py artigos
python3 skill/escalar_ordinal.py entrevistas
python3 skill/escalar_ordinal.py todos
```

### Executar Validação da Filtragem
```bash
python3 skill/validar_filtragem.py discursos
python3 skill/validar_filtragem.py artigos
python3 skill/validar_filtragem.py entrevistas
python3 skill/validar_filtragem.py todos
```

### Executar Validação da Escala
```bash
python3 skill/validar_escala.py discursos
python3 skill/validar_escala.py artigos
python3 skill/validar_escala.py entrevistas
python3 skill/validar_escala.py todos
```

## Formato dos Arquivos de Saída

Todos os arquivos de saída incluem o **tipo de documento** sendo analisado além do modelo de IA:

- `filtragem_discursos_opencode-hy3-2026-08-14.csv`
- `escala-ordinal-artigos_opencode-hy3-2026-08-14.csv`
- `validacao_entrevistas_opencode-hy3-2026-08-14.md`
- etc.

## Observações

- Os scripts Python usam **pré-seleção por vocabulário** para identificar documentos potencialmente relevantes
- A validação é feita por um "auditor humano" que reavalia os resultados
- O contexto de pesquisa padrão é sobre **Governança Global Digital** (2014-2025)
- É possível usar outros contextos criando novos arquivos na pasta `contextos/`
