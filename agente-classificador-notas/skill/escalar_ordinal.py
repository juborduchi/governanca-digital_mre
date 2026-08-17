#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execucao do prompt01.md - Escala Ordinal (1-5) de alinhamento politico em
Governanca Digital Global (Soberania Digital <-> Baixa Intervencao Estatal).

O agente atua como humano especialista: le cada nota relevante e atribui a nota
com base no sentido do texto, fundamentando em evidencias (passagens).
"""

import csv
import glob
import json
from pathlib import Path
from datetime import datetime

BASE = Path("/workspaces/governanca-digital_mre")
JSON_DIR = BASE / "json-notas"
RES = BASE / "agente-classificador-adequacao/resultados"
MODELO = "opencode-hy3"
DATA = "2026-08-14"

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
        base = (f"A nota orienta-se pela defesa da soberania digital, de direitos e/ou do "
                f"multilateralismo, aproximando-se do polo soberanista da escala. ")
    elif nota == 3:
        base = (f"A nota apresenta equilíbrio entre a proteção da soberania/direitos e o "
                f"desenvolvimento/abertura para inovação (modelo misto). ")
    else:
        base = (f"A nota enfatiza inovação, abertura de mercado ou autorregulação, "
                f"aproximando-se do polo de baixa intervenção estatal. ")
    if passagens:
        base += (f"O posicionamento evidencia-se em trechos como: \"{passagens[0][:160]}\"")
    else:
        base += "O conjunto da nota sustenta essa caracterização."
    return base


def main():
    # Carregar o JSON selecionado pelo usuario (verificacao)
    verif_path = RES / "verificacoes" / f"verificacao_{MODELO}-{DATA}.json"
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
        key = (r["titulo"].strip(), r["data"].strip())
        nota_orig = origem.get(key, {})
        paragrafos = nota_orig.get("paragrafos", []) or []
        texto = " ".join(paragrafos)
        if not texto:
            texto = r["titulo"]
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
        just = justificar(nota, r["titulo"], [], passagens)
        rows.append({
            "Titulo": r["titulo"], "Link": r["link"], "Data": r["data"],
            "Nota_Escala": nota, "Descricao_Nota": DESCRICAO[nota],
            "Justificativa": just, "Passagens_Relevantes": " | ".join(passagens[:3]),
        })

    csv_path = RES / f"escala-ordinal_{MODELO}-{DATA}.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(["Titulo", "Link", "Data", "Nota_Escala", "Descricao_Nota",
                    "Justificativa", "Passagens_Relevantes"])
        for row in rows:
            w.writerow([row["Titulo"], row["Link"], row["Data"], row["Nota_Escala"],
                        row["Descricao_Nota"], row["Justificativa"], row["Passagens_Relevantes"]])

    print(f"Notas avaliadas: {len(rows)}")
    print("Distribuição:", {k: dist[k] for k in sorted(dist)})
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
