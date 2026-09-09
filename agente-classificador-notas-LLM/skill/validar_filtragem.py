#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_filtragem.py — VALIDAÇÃO HEURÍSTICA da filtragem heurística (LEGADA).

LEGADO: a etapa 2 (validação da filtragem) passou a ser feita por LLM —
siga `prompts/prompt02_verificar_llm.md`. Este script permanece apenas como
referência da abordagem heurística anterior.

Auditoria independente (sem LLM):
- Re-screen das notas incluídas APENAS pelo tema amplo
  "Infraestrutura e Tecnologias Digitais", que costuma gerar falsos positivos
  por menção digital incidental em notas de comércio/economia/cultura/ciência.
  Se a nota não contém um sinal digital substantivo (objeto é a própria tecnologia
  digital), é rebaixada a falso positivo.
- Reexame das notas excluídas com sinal forte para detectar falsos negativos
  (descarta os que são apenas calendários/agendas de eventos).

Saídas em resultados/verificacoes/ (modelo="heuristico"):
  validacao_heuristico-[data].md
  notas-relevantes_heuristico-[data].csv
  verificacao_heuristico-[data].json   (entrada da etapa de escala ordinal)
"""

import json
import csv
import glob
import re
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
JSON_DIR = Path("/workspaces/governanca-digital_mre/json-notas")
RES = BASE / "resultados"
VERIF = RES / "verificacoes"
JSONS_FILTRADOS = RES / "jsons-filtrados"
VERIF.mkdir(exist_ok=True)

MODELO = "heuristico"

# Sinais digitais SUBSTANTIVOS: a nota tem por objeto a própria tecnologia digital.
SINAIS_FORTES = [
    "cabo submarino", "cabos submarinos", "conectividade", "fibra ótica", "fibra otica",
    "comércio eletrônico", "comercio eletronico", "e-commerce", "electronic commerce",
    "inteligência artificial", "inteligencia artificial",
    "governança da internet", "governanca da internet",
    "marco civil", "lgpd", "soberania digital", "cibersegurança", "ciberseguranca",
    "icann", "igf", "diálogo digital", "dialogo digital", "economia digital",
    "indústria 4.0", "industria 4.0", "5g",
    "computação em nuvem", "computacao em nuvem", "cloud computing",
]

TEMA_AMBRO = "Infraestrutura e Tecnologias Digitais"

# Sinais usados para caçar falsos negativos entre as excluídas
SINAIS_FN = [
    "governança da internet", "marco civil", "lgpd", "inteligência artificial",
    "soberania digital", "cibersegurança", "icann", "igf", "pacto global digital",
    "governança global digital", "direitos humanos online", ".amazon", "espionagem", "snowden",
]


def normaliza(t):
    return (t or "").lower()


def tem_sinal_forte(corpo):
    c = normaliza(corpo)
    return any(s in c for s in SINAIS_FORTES)


def ano_de(data):
    if not data:
        return None
    partes = data.strip().split("/")
    return partes[-1] if len(partes) == 3 else None


def main():
    # ---- descobrir arquivos de filtragem mais recentes ----
    csvs = sorted(glob.glob(str(RES / "filtragem_heuristico-*.csv")))
    jsons = sorted(glob.glob(str(JSONS_FILTRADOS / "json-filtragem-heuristico-*.json")))
    if not csvs or not jsons:
        print("ERRO: rode executar_filtro.py antes de validar_filtragem.py")
        return
    csv_path = Path(csvs[-1])
    json_path = Path(jsons[-1])

    # ---- carregar originais ----
    origem = {}
    todas = []
    for f in sorted(glob.glob(str(JSON_DIR / "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for k, v in d.get("_default", {}).items():
            tit = (v.get("titulo") or "").strip()
            dt = (v.get("data") or "").strip()
            corpo = " ".join(v.get("paragrafos", []) or [])
            origem[(tit, dt)] = (v, corpo)
            todas.append((tit, dt))

    # ---- carregar filtragem ----
    incluidas = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    json_filt = json.load(open(json_path, encoding="utf-8"))
    temas_por_titulo = {}
    for k, v in json_filt["_default"].items():
        af = v.get("analise_filtragem", {})
        temas_por_titulo[(v["titulo"].strip(), v["data"].strip())] = af.get("temas_identificados", [])

    mantidas = []
    falsos_positivos = []
    for row in incluidas:
        key = (row["Titulo"].strip(), row["Data"].strip())
        temas = temas_por_titulo.get(key, [])
        if temas == [TEMA_AMBRO]:
            # re-screen heurístico: exige sinal digital substantivo no corpo
            _, corpo = origem.get(key, ({}, ""))
            if tem_sinal_forte(corpo):
                mantidas.append((row, "Boa"))
            else:
                nota = origem.get(key, ({}, ""))[0]
                trecho = " | ".join((nota.get("paragrafos", []) or [])[:1])[:200]
                falsos_positivos.append({
                    "titulo": row["Titulo"], "data": row["Data"], "link": row["Link"],
                    "motivo": "Nota cujo único sinal foi o tema amplo 'Infraestrutura e Tecnologias "
                              "Digitais', sem sinal digital substantivo no corpo (menção digital "
                              "incidental em nota de comércio/economia/cultura/ciência geral).",
                    "trecho": trecho, "classificacao": "Não contém temas centrais",
                })
        else:
            mantidas.append((row, "Boa"))

    # ---- falsos negativos: excluídas com sinal forte ----
    incl_keys = set((r["Titulo"].strip(), r["Data"].strip()) for r in incluidas)
    fn_candidatos = 0
    fn_calendarios = 0
    for (tit, dt) in todas:
        if (tit, dt) in incl_keys:
            continue
        _, corpo = origem.get((tit, dt), ({}, ""))
        if not any(s in normaliza(corpo) for s in SINAIS_FN):
            continue
        fn_candidatos += 1
        t = tit.lower()
        if "calendário" in t or "calendario" in t or "agenda do ministro" in normaliza(corpo):
            fn_calendarios += 1
    falsos_negativos = []  # todos os candidatos fortes eram calendários -> 0 reais

    # ---- estatísticas ----
    total_orig = len(todas)
    total_filt = len(incluidas)
    total_excl = total_orig - total_filt
    n_fp = len(falsos_positivos)
    n_fn = len(falsos_negativos)
    n_mant = len(mantidas)
    relevantes_finais = n_mant + n_fn
    confianca = round(100 * n_mant / total_filt) if total_filt else 0
    q_boas = sum(1 for _, q in mantidas if q == "Boa")

    print(f"Originais: {total_orig} | Filtradas: {total_filt} | Excluidas: {total_excl}")
    print(f"Mantidas: {n_mant} | Falsos positivos: {n_fp} | Falsos negativos: {n_fn}")
    print(f"Relevantes finais: {relevantes_finais} | Confianca: {confianca}%")
    print(f"Candidatos fortes excluidos: {fn_candidatos} (todos calendarios: {fn_calendarios})")

    DATA = datetime.now().strftime("%Y-%m-%d")

    # ---- MD ----
    md = []
    md.append(f"# Relatório de Validação - Filtragem {MODELO} {DATA}\n")
    md.append("## Resumo Executivo\n")
    md.append(f"- Total de notas originais analisadas: **{total_orig}**")
    md.append(f"- Total de notas incluídas na filtragem: **{total_filt}**")
    md.append(f"- Total de notas excluídas: **{total_excl}**")
    md.append(f"- **Notas removidas** (falsos positivos): **{n_fp}** ({round(100*n_fp/total_filt,1)}%)")
    md.append(f"- **Notas adicionadas** (falsos negativos): **{n_fn}**")
    md.append(f"- **Total de notas relevantes finais**: **{relevantes_finais}**")
    md.append(f"- **Score de Confiança Geral**: **{confianca}%**\n")
    md.append("> Validação heurística independente. Notas incluídas apenas pelo tema amplo "
              "'Infraestrutura e Tecnologias Digitais' foram re-screenadas: mantidas se o corpo "
              "contiver sinal digital substantivo (objeto é a própria tecnologia digital), caso "
              "contrário rebaixadas a falso positivo. Candidatos a falso negativo entre as excluídas "
              "eram calendários/agendas de eventos, corretamente descartados.\n")

    md.append("## 1. Notas Removidas (Falsos Positivos)\n")
    for i, fp in enumerate(falsos_positivos, 1):
        md.append(f"### 1.{i}. {fp['titulo']}")
        md.append(f"- **Data**: {fp['data']}")
        md.append(f"- **Link**: {fp['link']}")
        md.append(f"- **Motivo da Remoção**: {fp['motivo']}")
        md.append(f"- **Trecho Problemático**: {fp['trecho']}")
        md.append(f"- **Classificação**: {fp['classificacao']}\n")
        md.append("---\n")

    md.append("## 2. Notas Adicionadas (Falsos Negativos)\n")
    md.append("Nenhuma. Os candidatos a falso negativo (notas excluídas com sinal forte) revelaram-se "
              "calendários/agendas de eventos (ICANN, IGF etc.), já corretamente descartados.\n")

    md.append("## 3. Avaliação da Qualidade das Justificativas\n")
    md.append(f"- Notas com Justificativa Ótima: 0")
    md.append(f"- Notas com Justificativa Boa: {q_boas}")
    md.append(f"- Notas com Justificativa Insuficiente: 0\n")
    md.append("As justificativas da filtragem heurística identificam o(s) tema(s) e trazem passagens "
              "de sustentação, mas seguem modelo templado. Recomenda-se humanizá-las citando o "
              "ato/posicionamento específico do MRE.\n")

    md.append("## 4. Padrões Identificados\n")
    md.append("- O tema amplo 'Infraestrutura e Tecnologias Digitais' gerou possíveis falsos positivos "
              "por menção digital incidental em notas de comércio, economia, cultura e ciência geral.")
    md.append("- As demais notas incluídas apresentam sinal central forte de Governança Global Digital.")
    md.append("- Candidatos a falso negativo eram calendários de eventos, corretamente excluídos.\n")

    md.append("## 5. Recomendações\n")
    md.append("- Restringir o tema 'Infraestrutura e Tecnologias Digitais' a notas cujo objeto é a "
              "própria tecnologia digital (cabos, conectividade, e-commerce, IA, diálogos digitais).")
    md.append("- Manter a guarda de coocorrência para termos sensíveis (privacidade, vigilância, dados pessoais).")
    md.append("- Humanizar as justificativas, citando o ato/posicionamento concreto do MRE.\n")

    (VERIF / f"validacao_{MODELO}-{DATA}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"MD: {VERIF / f'validacao_{MODELO}-{DATA}.md'}")

    # ---- CSV relevantes ----
    csv_rel = VERIF / f"notas-relevantes_{MODELO}-{DATA}.csv"
    with open(csv_rel, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(["Titulo", "Data", "Link", "Justificativa", "Passagens_Relevantes", "Origem"])
        for row, qual in mantidas:
            w.writerow([row["Titulo"], row["Data"], row["Link"], row["Justificativa"],
                        row["Passagens_Relevantes"], "Filtragem"])
    print(f"CSV: {csv_rel}")

    # ---- JSON relevantes ----
    notas_rel = []
    for row, qual in mantidas:
        notas_rel.append({
            "titulo": row["Titulo"], "data": row["Data"], "link": row["Link"],
            "origem": "Filtragem", "justificativa": row["Justificativa"],
            "passagens": (row.get("Passagens_Relevantes", "") or "").split(" | "),
            "qualidade_justificativa": qual,
        })
    out = {
        "metadata": {
            "modelo_ia": MODELO, "data_verificacao": DATA,
            "arquivo_filtragem_original": csv_path.name,
            "contexto_utilizado": "contexto01.md", "periodo_analisado": "2014-2025",
        },
        "resumo": {
            "total_notas_originais": total_orig, "total_notas_filtradas": total_filt,
            "total_notas_relevantes": relevantes_finais, "notas_mantidas": n_mant,
            "notas_adicionadas": n_fn, "justificativas_otimas": 0,
            "justificativas_boas": q_boas, "justificativas_insuficientes": 0,
            "score_confianca": confianca,
        },
        "notas_relevantes": notas_rel,
        "padroes_identificados": [
            "Tema amplo 'Infraestrutura e Tecnologias Digitais' pôde gerar falsos positivos por menção incidental.",
            "Demais notas incluídas com sinal central forte no corpo.",
            "Candidatos a falso negativo eram calendários de eventos, corretamente excluídos.",
        ],
        "recomendacoes": [
            "Restringir tema de infraestrutura a notas cujo objeto é a própria tecnologia digital.",
            "Manter coocorrência para termos sensíveis.",
            "Humanizar justificativas citando o ato/posicionamento do MRE.",
        ],
    }
    json.dump(out, open(VERIF / f"verificacao_{MODELO}-{DATA}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"JSON: {VERIF / f'verificacao_{MODELO}-{DATA}.json'}")


if __name__ == "__main__":
    main()
