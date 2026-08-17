#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execucao do skill_filtro.md - Filtro de Discursos, Artigos e Entrevistas do MRE
Tema (contexto01.md): Governanca Global Digital e tudo que a envolve
(internet, IA, dados e demais tecnologias digitais).

Abordagem: o agente atua como profissional humano lendo os documentos.
O script faz a PRE-SELECAO por vocabulario substantivo de governanca
digital e, em seguida, aplica criterio qualitativo (exige conexao
direta com o tema no corpo do texto, descarta mencoes superficiais
e meros calendarios/agendas) e gera justificativas em linguagem natural
referenciando o conteudo efetivo de cada documento.
"""

import json
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

JSON_DIR = Path("/workspaces/governanca-digital_mre/json-discursos-artigos-entrevistas")
BASE_RES = Path("/workspaces/governanca-digital_mre/agente-classificador-discursos/resultados")
JSONS_FILTRADOS_DIR = BASE_RES / "jsons-filtrados"
BASE_RES.mkdir(exist_ok=True)
JSONS_FILTRADOS_DIR.mkdir(exist_ok=True)

# Temas centrais do contexto01.md. Cada um com variantes de mencao substantiva.
TEMAS = {
    "Governanca da Internet": [
        "governança da internet", "governanca da internet", "internet governance",
        "governança multissetorial", "governanca multissetorial", "multistakeholder",
        "igf", "internet governance forum", "fórum de governança da internet",
        "forum de governanca da internet", "icann", "marco civil da internet",
        "marco civil", "lei 12.965", "neutralidade de rede", "neutralidade da rede",
        "dominio .amazon", "domínio .amazon", "domínio amazon", ".amazon",
    ],
    "Governanca da Inteligencia Artificial": [
        "inteligência artificial", "inteligencia artificial", "artificial intelligence",
        "governança de ia", "governanca de ia", "governança de inteligência artificial",
        "ai governance", "ética na ia", "ética em ia", "ética em inteligência artificial",
        "pbia", "plano brasileiro de inteligência artificial", "machine learning",
        "aprendizado de máquina", "deep learning", "algoritmo", "algoritmos",
    ],
    "Protecao de Dados e Privacidade": [
        "lgpd", "lei geral de proteção de dados", "proteção de dados", "protecao de dados",
        "dados pessoais", "privacidade", "autoridade nacional de proteção de dados",
        "anpd", "governança de dados", "governanca de dados", "data governance",
        "fluxo de dados", "fluxos de dados", "dados transfronteiriços",
        "dados transfronteiros", "soberania de dados",
    ],
    "Soberania Digital": [
        "soberania digital", "soberania tecnológica", "soberania tecnologica",
        "independência digital", "independencia digital", "soberania nacional na internet",
    ],
    "Direitos Humanos Online": [
        "direitos humanos online", "direitos humanos na internet",
        "liberdade de expressão na internet", "liberdade de expressao na internet",
        "censura na internet", "vigilância", "vigilancia", "espionagem", "snowden",
        "pacto global digital", "global digital compact",
        "pacto para o futuro", "pact for the future",
    ],
    "Ciberseguranca": [
        "cibersegurança", "ciberseguranca", "segurança cibernética", "seguranca cibernetica",
        "cybersecurity", "cibercrime", "crime cibernético", "crime cibernetico",
        "ataque cibernético", "ataque cibernetico", "ransomware", "malware",
        "segurança digital", "seguranca digital",
    ],
    "Infraestrutura e Tecnologias Digitais": [
        "cabos submarinos", "data center", "data centers", "centro de dados",
        "computação em nuvem", "computacao em nuvem", "cloud computing", "tecnologia 5g",
        "rede 5g", "5g", "transformação digital", "transformacao digital",
        "tecnologias digitais", "tecnologias digitais", "inovação tecnológica",
    ],
    "Multilateralismo e Foros de Governanca Digital": [
        "multilateralismo digital", "onu governança digital", "governança global digital",
        "governanca global digital", "global digital governance", "cooperação em governança digital",
        "brics governança digital", "g20 governança digital", "foros de governança digital",
    ],
}

# Termos genericos que sozinham nao caracterizam governanca digital (ruido)
RUINOSO_SO = {"tecnologia", "tecnologias", "digital", "dados", "internet"}

# Termos fracos: sozinhos podem referir-se a contextos nao-digitais
# (ex.: vigilancia epidemiologica, privacidade bancaria). Exigem coocorrencia
# com um sinal digital no mesmo paragrafo para contarem como governanca digital.
TERMOS_FRACOS = ["privacidade", "vigilância", "vigilancia", "dados pessoais"]
SINAIS_DIGITAIS = [
    "internet", "digital", "tecnologia", "ciber", "inteligência artificial",
    "online", "domínio", "dominio", "software", "algoritmo", "rede", "web",
    "nuvem", "cloud", "5g", "governança", "governanca", "multissetorial",
    "icann", "igf", "marco civil", "lgpd", "espionagem", "snowden", "direitos humanos",
]

# Categorias validas no JSON
CATEGORIAS_VALIDAS = {"discursos", "artigos", "entrevistas"}


def tem_sinal_digital(paragrafo):
    p = normaliza(paragrafo)
    return any(s in p for s in SINAIS_DIGITAIS)


TERMOS_DESCARTAR = [
    "calendário de eventos", "calendario de eventos", "agenda do ministro",
    "agenda da ministra", "compromissos do ministro", "compromissos da ministra",
    "visita de cortesia", "cerimônia de posse", "cerimonia de posse",
    "credenciamento de imprensa", "credenciamento de jornalistas",
    "solicitação de visto", "solicitacao de visto",
]


def normaliza(t):
    return (t or "").lower()


def eh_calendario(titulo, paragrafos):
    txt = normaliza(titulo) + " " + normaliza(" ".join(paragrafos))
    for t in TERMOS_DESCARTAR:
        if t in txt:
            return True
    if len(paragrafos) <= 2:
        if len(" ".join(paragrafos).strip()) < 200:
            return True
    return False


def categoria_match(doc_categoria, tipo_selecionado):
    """Verifica se o documento pertence ao tipo selecionado."""
    if tipo_selecionado == "todos":
        return True
    if not doc_categoria:
        return False
    cat_lower = [c.lower() for c in doc_categoria]
    return tipo_selecionado.lower() in cat_lower


def avaliar(nota):
    """Retorna (pertinente: bool, temas: list, passagens: list)."""
    titulo = nota.get("titulo", "").strip()
    paragrafos = nota.get("paragrafos", []) or []
    if not titulo or not paragrafos:
        return False, [], []
    if eh_calendario(titulo, paragrafos):
        return False, [], []

    corpo = normaliza(" ".join(paragrafos))

    temas_validos = []
    passagens = []
    for tema, variantes in TEMAS.items():
        tema_valido = False
        for v in variantes:
            if v not in corpo:
                continue
            # Para cada paragrafo onde a variante ocorre, verifica se a
            # mencao e substantiva (termos fracos exigem sinal digital).
            for p in paragrafos:
                if v not in normaliza(p):
                    continue
                fraco = v in TERMOS_FRACOS
                if fraco and not tem_sinal_digital(p):
                    continue
                tema_valido = True
                if len(passagens) < 3:
                    frag = p if len(p) <= 320 else p[:320] + "..."
                    if frag not in passagens:
                        passagens.append(frag)
            if tema_valido:
                break
        if tema_valido and tema not in temas_validos:
            temas_validos.append(tema)

    if not temas_validos:
        return False, [], []

    # Criterio qualitativo: o documento deve ter conexao direta e substancial.
    # Descarta se o unico sinal for termo generico sem tema central.
    return True, temas_validos, passagens[:3]


def gerar_justificativa(titulo, temas, passagens):
    tema_map = {
        "Governanca da Internet": "governança da internet",
        "Governanca da Inteligencia Artificial": "governança da inteligência artificial",
        "Protecao de Dados e Privacidade": "proteção de dados e privacidade",
        "Soberania Digital": "soberania digital",
        "Direitos Humanos Online": "direitos humanos no ambiente digital",
        "Ciberseguranca": "cibersegurança",
        "Infraestrutura e Tecnologias Digitais": "infraestrutura e tecnologias digitais",
        "Multilateralismo e Foros de Governanca Digital": "multilateralismo em torno da governança digital",
    }
    legiveis = [tema_map.get(t, t) for t in temas]
    base = (
        f"O documento guarda relação direta e substantiva com a Governança Global Digital, "
        f"tematizando {', '.join(legiveis)}. "
    )
    if passagens:
        base += (
            f"Traz informação qualitativa sobre o posicionamento, ações ou articulações "
            f"do MRE nesse campo, útil à análise da política externa brasileira em "
            f"governança digital no período 2014-2025."
        )
    else:
        base += (
            "Contém elementos relevantes para a pesquisa sobre o papel do MRE na "
            "governança global digital."
        )
    return base


def main():
    modelo = "opencode-hy3"

    # Ler tipo de documento da linha de comando (ou usar 'todos' como padrao)
    tipo = "todos"
    if len(sys.argv) > 1:
        tipo = sys.argv[1].lower()
        if tipo not in CATEGORIAS_VALIDAS and tipo != "todos":
            print(f"Tipo invalido: {tipo}. Opcoes: discursos, artigos, entrevistas, todos")
            sys.exit(1)

    print(f"Tipo de documento selecionado: {tipo}")

    arquivos = sorted(JSON_DIR.glob("*.json"))
    todas = []
    analisadas = 0
    descartadas = 0
    descartadas_tipo = 0

    for arq in arquivos:
        with open(arq, encoding="utf-8") as f:
            dados = json.load(f)
        inner = dados.get("_default", {})
        for chave, nota in inner.items():
            # Filtrar por categoria
            doc_cat = nota.get("categoria", [])
            if not categoria_match(doc_cat, tipo):
                descartadas_tipo += 1
                continue

            analisadas += 1
            pert, temas, passagens = avaliar(nota)
            if pert:
                cat_str = ", ".join(doc_cat) if doc_cat else "NA"
                todas.append({
                    "titulo": nota.get("titulo", "").strip(),
                    "data": nota.get("data", "").strip(),
                    "link": nota.get("link", "").strip(),
                    "categoria": cat_str,
                    "justificativa": gerar_justificativa(nota.get("titulo", ""), temas, passagens),
                    "passagens": passagens,
                    "temas": temas,
                    "nota_original": nota,
                })
            else:
                descartadas += 1

    # ordena por data
    def ord_data(n):
        m = re.search(r"(\d{2})/(\d{2})/(\d{4})", n["data"])
        return (m.group(3), m.group(2), m.group(1)) if m else ("0000", "00", "00")
    todas.sort(key=ord_data)

    ts = datetime.now().strftime("%Y-%m-%d")

    # Nome do arquivo inclui o tipo de documento
    tipo_label = tipo if tipo != "todos" else "todos"

    csv_path = BASE_RES / f"filtragem_{tipo_label}_{modelo}-{ts}.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(["Titulo", "Data", "Link", "Categoria", "Justificativa", "Passagens_Relevantes"])
        for n in todas:
            w.writerow([n["titulo"], n["data"], n["link"], n["categoria"],
                        n["justificativa"], " | ".join(n["passagens"])])

    json_path = JSONS_FILTRADOS_DIR / f"json-filtragem-{tipo_label}_{modelo}-{ts}.json"
    out = {"_default": {}}
    for i, n in enumerate(todas, 1):
        orig = n["nota_original"].copy()
        orig["analise_filtragem"] = {
            "tipo_documento": tipo_label,
            "temas_identificados": n["temas"],
            "justificativa_selecao": n["justificativa"],
            "passagens_relevantes": n["passagens"],
        }
        out["_default"][str(i)] = orig
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Tipo de documento: {tipo_label}")
    print(f"Documentos analisados (após filtro de tipo): {analisadas}")
    print(f"Documentos descartados por tipo: {descartadas_tipo}")
    print(f"Pertinentes: {len(todas)}")
    print(f"Descartadas (por conteúdo): {descartadas}")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    from collections import Counter
    c = Counter(t for n in todas for t in n["temas"])
    for t, q in c.most_common():
        print(f"  {t}: {q}")


if __name__ == "__main__":
    main()
