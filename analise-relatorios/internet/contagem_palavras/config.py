"""
Configuração da análise por contagem de palavras (Opção 1).

Define termo central e dois léxicos que representam enquadramentos
contrastantes do tema internet.
"""

# Termo central buscado no relatório
TERMO_CENTRAL = "internet"

# Regex para capturar variações do termo central (case-insensitive)
# Inclui plural e termos correlatos próximos se desejar expandir
TERMO_CENTRAL_REGEX = r"\binternet(s)?\b"

# Janela de contexto: nº de tokens antes e depois de cada ocorrência
JANELA_TOKENS = 50

# Léxicos das duas abordagens (minúsculas, sem acento normalizado na contagem)
ABORDAGEM_A_NOME = "Soberana/Multilateral"
ABORDAGEM_A_TERMOS = [
    "multilateral",
    "multilaterais",
    "multissetorial",
    "multissetoriais",
    "multissetorialidade",
    "governança",
    "governanca",
    "democrática",
    "democratica",
    "democrático",
    "democratico",
    "soberania",
    "soberano",
    "soberana",
]

ABORDAGEM_B_NOME = "Mercado/Inovação"
ABORDAGEM_B_TERMOS = [
    "autorregulação",
    "autorregulacao",
    "autoregulação",
    "inovação",
    "inovacao",
    "desenvolvimento",
    "mercado",
    "investimento",
    "investimentos",
    "autorregulacao",
]

# Mapeamento ano -> arquivo PDF em ../relatorios-gestao-mre/
# Usar Path relativo ao notebook: Path(__file__).parent / "../../relatorios-gestao-mre/..."
MAPA_ARQUIVOS = {
    2020: "relatorio-de-gestao-2020-final.pdf",
    2021: "relatorio-gestao-mre-2021.pdf",
    2022: "Relatrio2022.Versocompleta.pdf",
    2023: "relatorio-gestao-mre-2023-versao-final.pdf",
    2024: "Relatorio-Gestao-MRE-2024.pdf",
    2025: "Relatório-de-gestão_2025 (1).pdf",
}
