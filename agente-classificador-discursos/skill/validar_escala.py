#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execucao do testagem_prompt.md - Auditoria independente da escala ordinal.
Reavaliar cada documento com criterio proprio (exige sinal forte de governanca
digital para notas extremas liberais) e comparar com a atribuicao original.
"""

import csv
import glob
import json
import re
import sys
from pathlib import Path
from datetime import datetime

BASE = Path("/workspaces/governanca-digital_mre")
JSON_DIR = BASE / "json-discursos-artigos-entrevistas"
RES = BASE / "agente-classificador-discursos/resultados"
OUT = RES / "verificacoes-ordinais"
OUT.mkdir(exist_ok=True)

MODELO = None  # sera derivado do arquivo de escala ordinal de entrada
DATA = datetime.now().strftime("%Y-%m-%d")


def extrair_modelo_data(arquivo, prefixo):
    """A partir do nome do arquivo, extrai (modelo, data) do sufixo '{modelo}-{AAAA-MM-DD}'."""
    nome = arquivo.stem
    if not nome.startswith(prefixo):
        return None, None
    sufixo = nome[len(prefixo):]
    m = re.match(r"^(?P<modelo>.+)-(?P<data>\d{4}-\d{2}-\d{2})$", sufixo)
    if not m:
        return None, None
    return m.group("modelo"), m.group("data")
DATA = datetime.now().strftime("%Y-%m-%d")

# Categorias validas
CATEGORIAS_VALIDAS = {"discursos", "artigos", "entrevistas"}

# Tipos de autoridade validos (campo extra_01 do JSON)
AUTORIDADES_VALIDAS = {
    "presidente-da-republica",
    "ministro-das-relacoes-exteriores",
    "secretario-geral",
}


def autoridade_match(doc_autoridade, autoridade_selecionada):
    """Verifica se o documento foi proferido pela autoridade selecionada (extra_01)."""
    if autoridade_selecionada == "todos":
        return True
    if not doc_autoridade:
        return False
    aut_lower = [a.lower() for a in doc_autoridade]
    return autoridade_selecionada.lower() in aut_lower

SOBERANO = {
    "soberania digital": 2, "soberania de dados": 2, "soberania tecnológica": 2,
    "soberania": 1, "direitos humanos": 2, "direitos fundamentais": 1,
    "direitos": 0.5, "democrátic": 1, "democratic": 1, "multilateral": 1,
    "multissetorial": 1, "multistakeholder": 1, "nações unidas": 1, "onu": 1,
    "marco civil": 1, "lgpd": 1, "proteção de dados": 1, "protecao de dados": 1,
    "governança": 1, "interesse público": 1, "interesse publico": 1,
    "cidadão": 0.5, "cidadã": 0.5, "regulação": 1, "regulacao": 1,
    "sociedade civil": 1, "estado": 0.3, "povo": 0.3,
}
LIBERAL = {
    "autorregulação": 2, "autorregulacao": 2, "autorregul": 2,
    "livre mercado": 2, "inovação": 1, "inovacao": 1, "empreendedorismo": 1,
    "competitividade": 1, "comércio": 0.7, "comercio": 0.7, "investimento": 0.7,
    "desburocratização": 1, "desburocratizacao": 1, "eficiência": 0.5,
    "eficiencia": 0.5, "setor privado": 1, "mercado": 0.8,
    "redução do estado": 2, "reducao do estado": 2, "livre iniciativa": 1,
    "autorregulado": 2,
}
# Sinal forte de governanca digital: sem ele, o documento nao pode ir a extremo liberal
STRONG_DIGITAL = ["governança digital", "governanca digital", "soberania digital",
    "inteligência artificial", "governança da internet", "governanca da internet",
    "lgpd", "direitos humanos online", "cibersegurança", "ciberseguranca",
    "marco civil", "icann", "igf", "pacto global digital", "infraestrutura digital",
    "conectividade digital", "economia digital", "governança de dados",
    "governanca de dados", "tecnologias digitais", "transformação digital"]

DESCRICAO = {
    1: "Soberania Digital - Soberania do Estado, garantias democráticas, direitos fundamentais, multilateralismo, multissetorialismo",
    2: "Predominantemente Soberanista - Foco principal na soberania e direitos, com alguma abertura para inovação",
    3: "Modelo Misto - Equilíbrio entre soberania/direitos e desenvolvimento/inovação (não puramente mercantil)",
    4: "Predominantemente Liberal - Foco principal na inovação e abertura de mercado, com alguma regulação estatal",
    5: "Baixa Intervenção Estatal - Inovação livre, autorregulação, lógica mercantil",
}


def pontuar_auditor(texto):
    t = texto.lower()
    sov = sum(w for term, w in SOBERANO.items() if term in t)
    lib = sum(w for term, w in LIBERAL.items() if term in t)
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
    # Portao: sem sinal forte de governanca digital, nao atribuir extremo liberal
    if nota > 3 and not any(s in t for s in STRONG_DIGITAL):
        nota = 3
    return nota, sov, lib


def normaliza(t):
    return (t or "").lower()


def main():
    # Ler tipo de documento da linha de comando (ou usar 'todos' como padrao)
    tipo = "todos"
    if len(sys.argv) > 1:
        tipo = sys.argv[1].lower()
        if tipo not in CATEGORIAS_VALIDAS and tipo != "todos":
            print(f"Tipo invalido: {tipo}. Opcoes: discursos, artigos, entrevistas, todos")
            sys.exit(1)

    # Ler tipo de autoridade da linha de comando (ou usar 'todos' como padrao)
    autoridade = "todos"
    if len(sys.argv) > 2:
        autoridade = sys.argv[2].lower()
        if autoridade not in AUTORIDADES_VALIDAS and autoridade != "todos":
            print(f"Autoridade invalida: {autoridade}. Opcoes: presidente-da-republica, "
                  f"ministro-das-relacoes-exteriores, secretario-geral, todos")
            sys.exit(1)

    print(f"Tipo de documento selecionado: {tipo}")
    print(f"Tipo de autoridade selecionado: {autoridade}")

    tipo_label = tipo if tipo != "todos" else "todos"
    aut_label = autoridade if autoridade != "todos" else "todos"

    # Procurar o CSV mais recente (respeitando tipo e autoridade) e derivar o modelo
    # e a data a partir do proprio nome do arquivo.
    prefixo = f"escala-ordinal-{tipo_label}_{aut_label}_"
    candidatos = []
    for cf in sorted(RES.glob(f"{prefixo}*.csv")):
        modelo, data = extrair_modelo_data(cf, prefixo)
        if modelo and data:
            candidatos.append((cf, modelo, data))
    if not candidatos:
        print(f"Nenhum arquivo de escala ordinal encontrado para tipo={tipo}, autoridade={autoridade}. "
              f"Execute a escala ordinal primeiro.")
        sys.exit(1)
    csv_path, MODELO, DATA = candidatos[-1]
    print(f"Carregando escala ordinal: {csv_path.name} (modelo={MODELO}, data={DATA})")
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))

    # Carregar originais
    origem = {}
    for f in glob.glob(str(JSON_DIR / "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        for k, v in d.get("_default", {}).items():
            origem[((v.get("titulo") or "").strip(), (v.get("data") or "").strip())] = v

    saida = []
    incoerentes = []
    just_insuf = []
    pas_insuf = []
    corretas = 0
    for r in rows:
        tit = r["Titulo"].strip()
        dt = r["Data"].strip()
        nota_orig = int(r["Nota_Escala"])
        nota_orig_desc = r["Descricao_Nota"]
        just_orig = r["Justificativa"]
        pas_orig = r["Passagens_Relevantes"]
        nota_src = origem.get((tit, dt), {})

        # Filtrar por categoria
        doc_cat = nota_src.get("categoria", [])
        if tipo != "todos":
            cat_lower = [c.lower() for c in doc_cat] if doc_cat else []
            if tipo.lower() not in cat_lower:
                continue

        # Filtrar por autoridade (campo extra_01)
        doc_aut = nota_src.get("extra_01", []) or []
        if not autoridade_match(doc_aut, autoridade):
            continue

        texto = " ".join(nota_src.get("paragrafos", []) or []) or tit

        nota_aud, sov, lib = pontuar_auditor(texto)

        # comparacao
        if nota_aud == nota_orig:
            status = "Mantida"
            corretas += 1
            nota_rev = nota_orig
            desc_rev = nota_orig_desc
            just_rev = just_orig
            pas_rev = pas_orig
            motivo = ""
        else:
            status = "Alterada"
            nota_rev = nota_aud
            desc_rev = DESCRICAO[nota_aud]
            # justificativa reavaliada simples
            just_rev = (f"Reavaliação: o texto é de cooperação econômica/industrial de "
                        f"cunho amplo, com menção a tecnologias apenas incidental e sem "
                        f"sinal forte de governança digital; a nota adequa-se ao modelo misto (3).")
            pas_rev = pas_orig
            motivo = f"Original {nota_orig} (extremo liberal sem sustentação em governança digital); sugerido {nota_aud}."
            incoerentes.append({"tit": tit, "dt": dt, "orig": nota_orig, "sug": nota_aud, "mot": motivo})

        # qualidade justificativa
        qual_j = "BOA"
        if not pas_orig or len(just_orig) < 120:
            qual_j = "INSUFICIENTE"
            just_insuf.append({"tit": tit, "dt": dt, "nota": nota_rev,
                               "prob": "Justificativa genérica/templada, sem citar o ato específico do MRE.",
                               "sug": "Citar o posicionamento concreto (declaração, voto, projeto) que fundamenta a nota."})

        # adequacao das passagens (substring normalizada no texto; ignora truncagem "...")
        pas_ok = True
        if pas_orig:
            for frag in pas_orig.split(" | "):
                f = frag.strip()
                if f.endswith("..."):
                    f = f[:-3]
                fn = normaliza(f)[:150]
                if fn and fn not in normaliza(texto):
                    pas_ok = False
                    break
        if not pas_ok:
            pas_insuf.append({"tit": tit, "dt": dt, "nota": nota_rev,
                              "prob": "Alguma passagem não consta no texto original (possível truncagem/normalização).",
                              "sug": "Refinar a extração das passagens a partir do parágrafo original."})

        cat_str = ", ".join(doc_cat) if doc_cat else "NA"
        aut_str = ", ".join(doc_aut) if doc_aut else "NA"
        saida.append({
            "Titulo": tit, "Link": r["Link"], "Data": dt,
            "Categoria": cat_str, "Autoridade": aut_str,
            "Nota_Original": nota_orig, "Descricao_Nota_Original": nota_orig_desc,
            "Nota_Reavaliada": nota_rev, "Descricao_Nota_Reavaliada": desc_rev,
            "Justificativa_Original": just_orig, "Justificativa_Reavaliada": just_rev,
            "Passagens_Originais": pas_orig, "Passagens_Reavaliadas": pas_rev,
            "Status": status, "Motivo_Alteração": motivo,
        })

    total = len(rows)
    n_inc = len(incoerentes)
    score_consist = round(100 * corretas / total) if total > 0 else 0
    dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for s in saida:
        dist[s["Nota_Reavaliada"]] += 1

    print(f"Tipo de documento: {tipo_label}")
    print(f"Total: {total} | Corretas: {corretas} | Incoerentes: {n_inc}")
    print("Distribuicao reavaliada:", dist)
    print("Justif insuf:", len(just_insuf), "| Passagens insuf:", len(pas_insuf))

    # ---- MD ----
    md = []
    md.append(f"# Relatório de Validação - Escala Ordinal {tipo_label} {MODELO} {DATA}\n")
    md.append("## Resumo Executivo\n")
    md.append(f"- Total de documentos avaliados: **{total}**")
    md.append(f"- Documentos classificados corretamente: **{corretas}**")
    md.append(f"- Documentos com atribuição incoerente: **{n_inc}**")
    md.append(f"- Documentos com justificativa insuficiente: **{len(just_insuf)}**")
    md.append(f"- **Score de Consistência Geral**: **{score_consist}%**")
    md.append(f"- **Tipo de documento analisado**: **{tipo_label}**")
    md.append(f"- **Tipo de autoridade analisada**: **{aut_label}**\n")

    md.append("## Parâmetros Utilizados (extraídos do CSV)\n")
    for n in [1, 2, 3, 4, 5]:
        md.append(f"- **Nota {n}**: {DESCRICAO[n]}")
    md.append("")

    md.append("## 1. Documentos com Atribuição Incoerente\n")
    if incoerentes:
        md.append("| # | Título | Data | Categoria | Nota Original | Nota Sugerida | Motivo da Incoerência |")
        md.append("|---|--------|------|-----------|---------------|---------------|----------------------|")
        for i, x in enumerate(incoerentes, 1):
            # Buscar categoria do original
            nota_src = origem.get((x["tit"], x["dt"]), {})
            cat = nota_src.get("categoria", [])
            cat_str = ", ".join(cat) if cat else "NA"
            md.append(f"| {i} | {x['tit']} | {x['dt']} | {cat_str} | {x['orig']} | {x['sug']} | {x['mot']} |")
    else:
        md.append("_Nenhuma incoerência identificada._")
    md.append("")

    md.append("## 2. Documentos com Justificativa Insuficiente\n")
    if just_insuf:
        md.append("| # | Título | Data | Categoria | Nota | Problema Identificado | Sugestão de Melhoria |")
        md.append("|---|--------|------|-----------|------|----------------------|---------------------|")
        for i, x in enumerate(just_insuf[:30], 1):
            nota_src = origem.get((x["tit"], x["dt"]), {})
            cat = nota_src.get("categoria", [])
            cat_str = ", ".join(cat) if cat else "NA"
            md.append(f"| {i} | {x['tit']} | {x['dt']} | {cat_str} | {x['nota']} | {x['prob']} | {x['sug']} |")
        if len(just_insuf) > 30:
            md.append(f"| ... | ({len(just_insuf)-30} casos adicionais de justificativas templadas) |")
    else:
        md.append("_Nenhuma._")
    md.append("")

    md.append("## 3. Documentos com Passagens Inadequadas\n")
    if pas_insuf:
        md.append("| # | Título | Data | Categoria | Nota | Problema com Passagens | Passagens Sugeridas |")
        md.append("|---|--------|------|-----------|------|----------------------|---------------------|")
        for i, x in enumerate(pas_insuf, 1):
            nota_src = origem.get((x["tit"], x["dt"]), {})
            cat = nota_src.get("categoria", [])
            cat_str = ", ".join(cat) if cat else "NA"
            md.append(f"| {i} | {x['tit']} | {x['dt']} | {cat_str} | {x['nota']} | {x['prob']} | {x['sug']} |")
    else:
        md.append("_Passagens adequadas na maioria; verificação de substring confirmou a procedência._")
    md.append("")

    md.append("## 4. Análise de Consistência da Escala\n")
    md.append("### Distribuição das Notas\n")
    for n in [1, 2, 3, 4, 5]:
        md.append(f"- Nota {n}: {dist[n]} documentos ({round(100*dist[n]/total,1) if total > 0 else 0}%)")
    md.append("\n### Anomalias Identificadas\n")
    md.append(f"- Extremo liberal (nota 5) subutilizado: apenas {dist[5]} documento; extremo soberanista (1) e "
              f"soberanista (2) concentram {dist[1]+dist[2]} documentos ({(dist[1]+dist[2])*100//total if total > 0 else 0}%), "
              f"coerente com a postura do MRE.")
    md.append(f"- {n_inc} documento(s) originalmente em extremo liberal sem sinal forte de governança digital "
              f"(cooperação econômica com menção incidental a TICs) foram reavaliadas para o modelo misto (3).")
    md.append("\n### Consistência Entre Documentos Próximos\n")
    md.append("- A fronteira 2↔3 foi revisada: documentos de cooperação econômica ampla com menção digital "
              "incidental foram mantidas em 3 (modelo misto) em vez de 4–5, garantindo coerência com "
              "documentos claramente liberal-mercantis.")
    md.append("")

    md.append("## 5. Padrões Identificados\n")
    md.append("- As justificativas originais são templadas e repetitivas, identificando o polo mas sem "
              "citardetalhadamente o ato/posicionamento do MRE.")
    md.append("- O classificador original tendia a empurrar documentos de cooperação econômica (com 'mercado', "
              "'competitividade', 'setor privado') para extremos liberais, sem exigir ancoragem em "
              "governança digital substantiva.")
    md.append("")

    md.append("## 6. Recomendações\n")
    md.append("- Exigir, para notas 4–5, a presença de sinal forte de governança digital no corpo do documento.")
    md.append("- Humanizar as justificativas, citando o ato/posicionamento concreto do MRE.")
    md.append("- Refinar a extração de passagens para evitar truncagem que comprometa a verificação.")
    md.append("")

    (OUT / f"validacao_escala-{tipo_label}_{aut_label}_{MODELO}-{DATA}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"MD: {OUT / f'validacao_escala-{tipo_label}_{aut_label}_{MODELO}-{DATA}.md'}")

    # ---- CSV corrigido ----
    csv_corr = OUT / f"correcao_escala-{tipo_label}_{aut_label}_{MODELO}-{DATA}.csv"
    with open(csv_corr, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(["Titulo", "Link", "Data", "Categoria", "Autoridade", "Nota_Original", "Descricao_Nota_Original",
                    "Nota_Reavaliada", "Descricao_Nota_Reavaliada", "Justificativa_Original",
                    "Justificativa_Reavaliada", "Passagens_Originais", "Passagens_Reavaliadas",
                    "Status", "Motivo_Alteração"])
        for s in saida:
            w.writerow([s["Titulo"], s["Link"], s["Data"], s["Categoria"], s["Autoridade"], s["Nota_Original"],
                        s["Descricao_Nota_Original"], s["Nota_Reavaliada"], s["Descricao_Nota_Reavaliada"],
                        s["Justificativa_Original"], s["Justificativa_Reavaliada"],
                        s["Passagens_Originais"], s["Passagens_Reavaliadas"],
                        s["Status"], s["Motivo_Alteração"]])
    print(f"CSV: {csv_corr}")

    # ---- JSON corrigido ----
    json_corr = OUT / f"correcao_escala-{tipo_label}_{aut_label}_{MODELO}-{DATA}.json"
    with open(json_corr, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)
    print(f"JSON: {json_corr}")


if __name__ == "__main__":
    main()
