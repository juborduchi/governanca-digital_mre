"""
utils.py — Opção 2: embeddings semânticos.

Funções: extração PDF, chunking, embeddings, centr óides, similaridade.
"""

import re
from pathlib import Path
from typing import List, Dict
import unicodedata

try:
    import pymupdf  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    try:
        from PyPDF2 import PdfReader
        HAS_PYPDF2 = True
    except ImportError:
        HAS_PYPDF2 = False
    else:
        HAS_PYPDF2 = True
else:
    HAS_PYPDF2 = False


def extract_text(pdf_path: Path) -> str:
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
        raise ImportError("Instale pymupdf ou PyPDF2")
    return text


def chunk_por_paragrafo(texto: str, min_len: int = 80) -> List[str]:
    """Quebra por linha vazia / parágrafo, filtra muito curtos."""
    # Normaliza quebras
    texto = re.sub(r"\r\n", "\n", texto)
    # Split por 2+ quebras
    brutos = re.split(r"\n\s*\n", texto)
    chunks = []
    for b in brutos:
        b = b.strip().replace("\n", " ")
        b = re.sub(r"\s+", " ", b)
        if len(b) >= min_len:
            chunks.append(b)
    return chunks


def chunk_janela_deslizante(texto: str, tamanho: int = 400, overlap: int = 50) -> List[str]:
    """Janela deslizante por tokens (fallback se parágrafo não funcionar bem)."""
    tokens = texto.split()
    chunks = []
    i = 0
    while i < len(tokens):
        janela = tokens[i:i+tamanho]
        chunks.append(" ".join(janela))
        i += tamanho - overlap
    return chunks


def filtrar_chunks_com_termo(chunks: List[str], regex: str) -> List[Dict]:
    """Retorna só chunks que contêm o termo, com índice original."""
    pat = re.compile(regex, re.IGNORECASE)
    out = []
    for idx, c in enumerate(chunks):
        if pat.search(c):
            out.append({"idx_original": idx, "texto": c})
    return out


# ---------- Embeddings ----------

def carregar_modelo(nome: str):
    """Carrega SentenceTransformer. Lança erro amigável se não instalado."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise ImportError(
            "sentence-transformers não instalado. Rode: pip install sentence-transformers torch\n"
            f"Detalhe: {e}"
        )
    print(f"Carregando modelo: {nome} ...")
    model = SentenceTransformer(nome)
    print(f"Modelo carregado, dim={model.get_sentence_embedding_dimension()}")
    return model


def gerar_centroides(model, termos_a: List[str], termos_b: List[str],
                     frases_a: List[str] = None, frases_b: List[str] = None):
    """
    Gera centr óides A e B como média dos embeddings.
    Se frases fornecidas, usa frases (melhor); senão usa termos.
    Retorna (centroide_A, centroide_B) como vetores numpy.
    """
    import numpy as np
    # Preferir frases se houver, senão termos
    docs_a = frases_a if frases_a else termos_a
    docs_b = frases_b if frases_b else termos_b
    emb_a = model.encode(docs_a, convert_to_numpy=True, show_progress_bar=False)
    emb_b = model.encode(docs_b, convert_to_numpy=True, show_progress_bar=False)
    # Média L2-normalizada (mesma que usar cosine)
    centroide_a = emb_a.mean(axis=0)
    centroide_b = emb_b.mean(axis=0)
    # Normaliza para cosseno = dot
    centroide_a = centroide_a / (np.linalg.norm(centroide_a) + 1e-9)
    centroide_b = centroide_b / (np.linalg.norm(centroide_b) + 1e-9)
    return centroide_a, centroide_b


def embed_chunks(model, chunks: List[str]):
    """Gera embeddings para lista de chunks, já normalizados."""
    import numpy as np
    embs = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
    # Normaliza
    norms = (embs**2).sum(axis=1, keepdims=True)**0.5 + 1e-9
    return embs / norms


def similaridade_cosseno(embs, centroide):
    """Cosseno já que ambos normalizados = dot product."""
    import numpy as np
    return (embs @ centroide)


def classificar_chunks(embs, centroide_a, centroide_b):
    """
    Para cada chunk, compara sim_A vs sim_B.
    Retorna lista de dicts com sim_A, sim_B, diff, vencedor.
    """
    sim_a = similaridade_cosseno(embs, centroide_a)
    sim_b = similaridade_cosseno(embs, centroide_b)
    out = []
    for i in range(len(embs)):
        vencedor = "A" if sim_a[i] > sim_b[i] else "B"
        # empate muito próximo (<0.02) pode ser considerado neutro
        diff = float(sim_a[i] - sim_b[i])
        if abs(diff) < 0.02:
            vencedor = "neutro"
        out.append({
            "sim_A": float(sim_a[i]),
            "sim_B": float(sim_b[i]),
            "diff": diff,
            "vencedor": vencedor,
        })
    return out
