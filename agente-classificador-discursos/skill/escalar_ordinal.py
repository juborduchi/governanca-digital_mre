#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execucao do prompt01.md - Escala Ordinal (1-5) de alinhamento politico em
Governanca Digital Global (Soberania Digital <-> Baixa Intervencao Estatal).

O agente atua como humano especialista: le cada documento relevante e atribui a nota
com base no sentido do texto, fundamentando em evidencias (passagens).
"""

import csv
import glob
import json
import sys
from pathlib import Path
from datetime import datetime

BASE = Path("/workspaces/governanca-digital_mre")
JSON_DIR = BASE / "json-discursos-artigos-entrevistas"
RES = BASE / "agente-classificador-discursos/resultados"
MODELO = "opencode-hy3"
DATA = "2026-08-14"

# Categorias validas
CATEGORIAS_VALIDAS = {"discursos", "artigos", "entrevistas"}

DESCRICAO = {
    1: "Soberania Digital - Soberania do Estado, garantias democráticas, direitos fundamentais, multilateralismo, multissetorialismo",
    2: "Predominantemente Soberanista - Foco principal na soberania e direitos, com alguma abertura para inovação",
    3: "Modelo Misto - Equilíbrio entre soberania/direitos e desenvolvimento/inovação (não puramente mercantil)",
    4: "Predominantemente Liberal - Foco principal na inovação e abertura de mercado, com alguma regulação estatal",
    5: "Baixa Intervenção Estatal - Inovação livre, autorregulação, lógica mercantil",
}

# Sinais do polo Soberanista (aproximam de 1)
SOBERANO = {
    "soberania digital": 2, "soberania de dados": 2, "soberania tecnológica": 2,
    "soberania": 1, "direitos humanos": 2, "direitos fundamentais": 1,
    "direitos": 0.5, "democrátic": 1, "democratic": 1, "multilateral": 1,
    "multissetorial": 1, "multistakeholder": 1, "nações unidas": 1, "onu": 1,
    "marco civil": 1, "lgpd": 1, "proteção de dados": 1, "protecao de dados": 1,
    "governança": 1, "interesse público": 1, "interesse publico": 1,
    "cidadão": 0.5, "cidadã": 0.5, "regulação": 1, "regulacao": 1,
    "estado": 0.3, "sociedade civil": 1, "povo": 0.3,
}
# Sinais do polo Liberal (aproximam de 5)
LIBERAL = {
    "autorregulação": 2, "autorregulacao": 2, "autorregul": 2,
    "livre mercado": 2, "inovação": 1, "inovacao": 1, "empreendedorismo": 1,
    "competitividade": 1, "comércio": 0.7, "comercio": 0.7, "investimento": 0.7,
    "desburocratização": 1, "desburocratizacao": 1, "eficiência": 0.5,
    "eficiencia": 0.5, "setor privado": 1, "mercado": 0.8,
    "redução do estado": 2, "reducao do estado": 2, "livre iniciativa": 1,
    "autorregulado": 2,
}


def pontuar(texto):
    t = texto.lower()
    sov = 0.0
    lib = 0.0
    for term, w in SOBERANO.items():
        if term in t:
            sov += w
    for term, w in LIBERAL.items():
        if term in t:
            lib += w
    net = sov - lib
    if net >= 3:
        nota = 1
    elif net >= 1:
        nota = 2
    elif net > -1:
        nota = 3
    elif net > -3:
        nota = 4
    else:
        nota = 5
    return nota, sov, lib


def justificar(nota, titulo, temas_encontrados, passagens):
    if nota <= 2:
        base = (f"O documento orienta-se pela defesa da soberania digital, de direitos e/ou do "
                f"multilateralismo, aproximando-se do polo soberanista da escala. ")
    elif nota == 3:
        base = (f"O documento apresenta equilíbrio entre a proteção da soberania/direitos e o "
                f"desenvolvimento/abertura para inovação (modelo misto). ")
    else:
        base = (f"O documento enfatiza inovação, abertura de mercado ou autorregulação, "
                f"aproximando-se do polo de baixa intervenção estatal. ")
    if passagens:
        base += (f"O posicionamento evidencia-se em trechos como: \"{passagens[0][:160]}\"")
    else:
        base += "O conjunto do documento sustenta essa caracterização."
    return base


def main():
    # Ler tipo de documento da linha de comando (ou usar 'todos' como padrao)
    tipo = "todos"
    if len(sys.argv) > 1:
        tipo = sys.argv[1].lower()
        if tipo not in CATEGORIAS_VALIDAS and tipo != "todos":
            print(f"Tipo invalido: {tipo}. Opcoes: discursos, artigos, entrevistas, todos")
            sys.exit(1)

    print(f"Tipo de documento selecionado: {tipo}")

    # Carregar o JSON selecionado pelo usuario (verificacao)
    # Procurar o arquivo mais recente de verificacao
    verif_dir = RES / "verificacoes"
    verif_files = sorted(verif_dir.glob(f"verificacao_{MODELO}-*.json"))
    if not verif_files:
        print("Nenhum arquivo de verificacao encontrado. Execute a validacao da filtragem primeiro.")
        sys.exit(1)
    verif_path = verif_files[-1]
    print(f"Carregando verificacao: {verif_path.name}")
    verif = json.load(open(verif_path, encoding="utf-8"))
    rel = verif.get("notas_relevantes", [])

    # Carregar originais
    origem = {}
    for f in glob.glob(str(JSON_DIR / "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        for k, v in d.get("_default", {}).items():
            origem[((v.get("titulo") or "").strip(), (v.get("data") or "").strip())] = v

    rows = []
    dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in rel:
        tit = r["titulo"].strip()
        dt = r["data"].strip()
        key = (tit, dt)
        nota_orig = origem.get(key, {})

        # Filtrar por categoria
        doc_cat = nota_orig.get("categoria", [])
        if tipo != "todos":
            cat_lower = [c.lower() for c in doc_cat] if doc_cat else []
            if tipo.lower() not in cat_lower:
                continue

        paragrafos = nota_orig.get("paragrafos", []) or []
        texto = " ".join(paragrafos)
        if not texto:
            texto = tit
        nota, sov, lib = pontuar(texto)
        dist[nota] += 1
        # passagens relevantes (trechos com sinais fortes)
        passagens = []
        for p in paragrafos:
            pl = p.lower()
            if any(s in pl for s in ["soberania", "direitos humanos", "multilateral",
                                     "inovação", "inovacao", "autorregul", "comércio",
                                     "comercio", "marco civil", "lgpd", "governança",
                                     "governanca", "mercado", "livre"]):
                frag = p if len(p) <= 300 else p[:300] + "..."
                if frag not in passagens:
                    passagens.append(frag)
            if len(passagens) >= 3:
                break
        just = justificar(nota, tit, [], passagens)
        cat_str = ", ".join(doc_cat) if doc_cat else "NA"
        rows.append({
            "Titulo": tit, "Link": r["link"], "Data": dt,
            "Categoria": cat_str,
            "Nota_Escala": nota, "Descricao_Nota": DESCRICAO[nota],
            "Justificativa": just, "Passagens_Relevantes": " | ".join(passagens[:3]),
        })

    ts = DATA
    tipo_label = tipo if tipo != "todos" else "todos"

    csv_path = RES / f"escala-ordinal-{tipo_label}_{MODELO}-{ts}.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(["Titulo", "Link", "Data", "Categoria", "Nota_Escala", "Descricao_Nota",
                    "Justificativa", "Passagens_Relevantes"])
        for row in rows:
            w.writerow([row["Titulo"], row["Link"], row["Data"], row["Categoria"],
                        row["Nota_Escala"], row["Descricao_Nota"],
                        row["Justificativa"], row["Passagens_Relevantes"]])

    # JSON tambem
    json_path = RES / f"escala-ordinal-{tipo_label}_{MODELO}-{ts}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Tipo de documento: {tipo_label}")
    print(f"Notas avaliadas: {len(rows)}")
    print("Distribuição:", {k: dist[k] for k in sorted(dist)})
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")


if __name__ == "__main__":
    main()
