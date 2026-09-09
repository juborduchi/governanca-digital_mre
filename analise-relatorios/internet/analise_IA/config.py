"""
config.py — Opção 2: Análise por embeddings semânticos.

Modelo multilíngue converte texto em vetor (512/384 dims).
Comparamos cada trecho com "internet" aos protótipos A/B via cosseno.
"""

# Modelo sentence-transformers (multilíngue, bom para PT)
# Alternativas: "distiluse-base-multilingual-cased-v2" (512d, usado no colab original)
#               "paraphrase-multilingual-MiniLM-L12-v2" (384d, mais leve e rápido)
#               "intfloat/multilingual-e5-large" (560d, mais preciso, mais pesado)
MODELO_EMBEDDING = "paraphrase-multilingual-MiniLM-L12-v2"

# Termo central
TERMO_CENTRAL = "internet"
TERMO_CENTRAL_REGEX = r"\binternet(s)?\b"

# Léxicos das duas abordagens — usados para criar centr óides semânticos
ABORDAGEM_A_NOME = "Soberana/Multilateral"
ABORDAGEM_A_TERMOS = [
    "multilateral",
    "multilaterais",
    "multissetorial",
    "multissetoriais",
    "governança",
    "governança democrática",
    "soberania",
    "soberania digital",
]

ABORDAGEM_B_NOME = "Mercado/Inovação"
ABORDAGEM_B_TERMOS = [
    "autorregulação",
    "inovação",
    "desenvolvimento",
    "mercado",
    "investimento",
    "autorregulação do setor privado",
]

# Frases-âncora (opcional, melhor que palavras isoladas para centr óide)
# Se não quiser usar, deixe lista vazia que o código usa só os termos acima
ABORDAGEM_A_FRASES = [
    "governança multilateral e democrática da internet",
    "soberania digital e regulação estatal da internet",
]

ABORDAGEM_B_FRASES = [
    "autorregulação e inovação no mercado digital",
    "desenvolvimento do mercado e investimento privado na internet",
]

# Chunking: como recortar o relatório em trechos para embedding
CHUNK_TIPO = "paragrafo"  # "paragrafo" ou "janela_deslizante"
CHUNK_TAMANHO = 400       # se janela deslizante: tokens por chunk
CHUNK_OVERLAP = 50        # overlap entre chunks

# Filtro: só analisar chunks que contêm o termo central (recomendado)
FILTRAR_SOMENTE_COM_TERMO = True

# Mapa ano -> PDF (relativo a analise_IA/)
MAPA_ARQUIVOS = {
    2020: "relatorio-de-gestao-2020-final.pdf",
    2021: "relatorio-gestao-mre-2021.pdf",
    2022: "Relatrio2022.Versocompleta.pdf",
    2023: "relatorio-gestao-mre-2023-versao-final.pdf",
    2024: "Relatorio-Gestao-MRE-2024.pdf",
    2025: "Relatório-de-gestão_2025 (1).pdf",
}
