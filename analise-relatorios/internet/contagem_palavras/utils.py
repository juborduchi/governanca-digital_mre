"""
utils.py - Funções compartilhadas para Opção 1: contagem por janela.

Uso: import utils; text = utils.extract_text(pdf_path); contextos = utils.extrair_contextos(text)
"""

import re
import unicodedata
from pathlib import Path
from collections import Counter

try:
    import pymupdf  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

# Fallback PyPDF2
if not HAS_PYMUPDF:
    try:
        from PyPDF2 import PdfReader
        HAS_PYPDF2 = True
    except ImportError:
        HAS_PYPDF2 = False
else:
    HAS_PYPDF2 = False


def normalizar(texto: str) -> str:
    """Minúsculas + remove acentos para comparar léxicos com/sem acento."""
    texto = texto.lower()
    # NFD decompõe acentos: é -> e + ´
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def extract_text(pdf_path: str | Path) -> str:
    """Extrai texto de PDF usando PyMuPDF se disponível, senão PyPDF2."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
    text = ""
    if HAS_PYMUPDF:
        doc = pymupdf.open(str(pdf_path))
        for page in doc:
            text += page.get_text() + "\n"
    elif HAS_PYPDF2:
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    else:
        raise ImportError("Nenhuma lib PDF disponível: instale pymupdf ou PyPDF2")
    return text


def tokenizar(texto: str) -> list[str]:
    """Tokeniza preservando palavras com hífen, retorna tokens normalizados."""
    # Mantém letras/números, separa pontuação
    tokens = re.findall(r"\b[\w\-]+\b", texto.lower(), flags=re.UNICODE)
    return tokens


def extrair_contextos(texto: str, termo_regex: str, janela: int = 50):
    """
    Retorna lista de dicts para cada ocorrência do termo:
    {idx, match, janela_tokens, janela_texto, pos_inicio, pos_fim}
    janela = nº tokens antes e depois.
    """
    tokens = tokenizar(texto)
    texto_norm = normalizar(texto)
    # Precisa mapear ocorrências no texto normalizado para tokens
    # Simplificação: busca token a token por regex no token normalizado
    pattern = re.compile(termo_regex, re.IGNORECASE)
    contextos = []
    # Normaliza cada token para comparar
    tokens_norm = [normalizar(t) for t in tokens]
    for i, tok_norm in enumerate(tokens_norm):
        if pattern.search(tok_norm):
            inicio = max(0, i - janela)
            fim = min(len(tokens), i + janela + 1)
            janela_tokens = tokens[inicio:fim]
            # Recupera trecho original aproximado
            janela_texto = " ".join(janela_tokens)
            contextos.append({
                "indice_token": i,
                "termo": tokens[i],
                "janela_tokens": janela_tokens,
                "janela_texto": janela_texto,
                "pos_inicio": inicio,
                "pos_fim": fim,
            })
    return contextos, tokens


def contar_lexicos(janela_tokens: list[str], lex_a: list[str], lex_b: list[str]):
    """Conta ocorrências de cada léxico dentro da janela (comparação normalizada)."""
    janela_norm = [normalizar(t) for t in janela_tokens]
    lex_a_norm = [normalizar(t) for t in lex_a]
    lex_b_norm = [normalizar(t) for t in lex_b]
    set_a = set(lex_a_norm)
    set_b = set(lex_b_norm)
    cnt_a = Counter(t for t in janela_norm if t in set_a)
    cnt_b = Counter(t for t in janela_norm if t in set_b)
    total_a = sum(cnt_a.values())
    total_b = sum(cnt_b.values())
    return cnt_a, cnt_b, total_a, total_b


def analisar_texto(texto: str, termo_regex: str, lex_a: list[str], lex_b: list[str], janela: int = 50):
    """Pipeline completo para um texto: extrai contextos + conta."""
    contextos, tokens = extrair_contextos(texto, termo_regex, janela)
    total_a_geral = 0
    total_b_geral = 0
    cnt_a_geral = Counter()
    cnt_b_geral = Counter()
    detalhes = []
    for ctx in contextos:
        cnt_a, cnt_b, tot_a, tot_b = contar_lexicos(ctx["janela_tokens"], lex_a, lex_b)
        cnt_a_geral.update(cnt_a)
        cnt_b_geral.update(cnt_b)
        total_a_geral += tot_a
        total_b_geral += tot_b
        detalhes.append({
            **ctx,
            "contagem_A": dict(cnt_a),
            "contagem_B": dict(cnt_b),
            "total_A": tot_a,
            "total_B": tot_b,
        })
    return {
        "n_ocorrencias": len(contextos),
        "n_tokens_total": len(tokens),
        "total_A": total_a_geral,
        "total_B": total_b_geral,
        "cnt_A": dict(cnt_a_geral),
        "cnt_B": dict(cnt_b_geral),
        "detalhes": detalhes,
        "tokens": tokens,
    }
