#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para filtrar notas à imprensa do MRE baseadas no contexto de pesquisa
sobre Governança Global Digital (2014-2025).
"""

import json
import csv
import os
import re
from datetime import datetime
from pathlib import Path

# Configurações
JSON_NOTAS_DIR = Path("/workspaces/governanca-digital_mre/json-notas")
RESULTADOS_DIR = Path("/workspaces/governanca-digital_mre/agente-classificador-adequacao/resultados")
JSONS_FILTRADOS_DIR = RESULTADOS_DIR / "jsons-filtrados"

# Criar diretórios de saída
RESULTADOS_DIR.mkdir(exist_ok=True)
JSONS_FILTRADOS_DIR.mkdir(exist_ok=True)

# Palavras-chave e temas do contexto01.md para análise de relevância
TEMAS_CENTRAIS = {
    "governanca_global_digital": [
        "governança global digital", "governança digital", "global digital governance",
        "governança da internet", "internet governance", "governança de dados",
        "data governance", "governança de ia", "governança de inteligência artificial",
        "ai governance", "artificial intelligence governance"
    ],
    "marco_civil_internet": [
        "marco civil da internet", "lei 12.965", "marco civil", "civil internet",
        "direitos na internet", "neutralidade de rede", "neutralidade da rede"
    ],
    "lgpd_protecao_dados": [
        "lgpd", "lei geral de proteção de dados", "proteção de dados", "dados pessoais",
        "privacidade", "proteção da privacidade", "anpd", "autoridade nacional de proteção de dados"
    ],
    "soberania_digital": [
        "soberania digital", "soberania nacional", "soberania de dados",
        "soberania tecnológica", "independência digital"
    ],
    "multilateralismo_onu": [
        "multilateralismo", "multilateral", "organização das nações unidas", "onu",
        "nacoes unidas", "united nations", "pacto global digital", "global digital compact",
        "pacto para o futuro", "pact for the future"
    ],
    "multissetorialidade": [
        "multissetorial", "multissetorialidade", "multistakeholder", "multistakeholderism",
        "sociedade civil", "setor privado", "governos", "icann", "igf",
        "internet governance forum", "fórum de governança da internet"
    ],
    "direitos_humanos_online": [
        "direitos humanos", "human rights", "direitos humanos online",
        "liberdade de expressão", "freedom of expression", "censura",
        "vigilância", "surveillance", "espionagem", "snowden"
    ],
    "cooperacao_internacional_foros": [
        "cooperação internacional", "cooperação", "international cooperation",
        "brics", "g20", "g77", "oit", "omc", "organização mundial",
        "fórum", "forum", "cúpula", "summit", "reunião de cúpula"
    ],
    "ia_inteligencia_artificial": [
        "inteligência artificial", "artificial intelligence", "ia", "ai",
        "pbia", "plano brasileiro de inteligência artificial",
        "ética", "ethics", "algoritmo", "algoritmos", "machine learning",
        "aprendizado de máquina", "deep learning"
    ],
    "infraestrutura_critica": [
        "infraestrutura crítica", "cabos submarinos", "data center",
        "centro de dados", "cloud computing", "computação em nuvem",
        "5g", "tecnologia 5g", "rede 5g"
    ],
    "ciberseguranca": [
        "cibersegurança", "cybersecurity", "segurança cibernética",
        "segurança digital", "crime cibernético", "cibercrime",
        "ataque cibernético", "ransomware", "malware"
    ],
    "dominio_amazon_icann": [
        ".amazon", "domínio amazon", "amazon dominio", "icann", "otca",
        "organização do tratado de cooperação amazônica"
    ],
    "suspensao_x_twitter": [
        "suspensão do x", "suspensao do x", "x no brasil", "twitter brasil",
        "elon musk", "stf", "supremo tribunal federal", "artigo 11 marco civil"
    ]
}

# Termos que indicam notas de apenas calendário/agenda (para descartar)
TERMOS_DESCARTAR = [
    "calendário de eventos", "calendario de eventos", "agenda do ministro",
    "agenda da ministra", "compromissos do ministro", "compromissos da ministra",
    "visita de cortesia", "cerimônia de posse", "cerimonia de posse",
    "reunião de rotina", "reuniao de rotina", "encontro bilateral de rotina"
]

def eh_nota_calendario(titulo, paragrafos):
    """Verifica se a nota é apenas calendário/agenda."""
    texto_completo = (titulo + " " + " ".join(paragrafos)).lower()
    for termo in TERMOS_DESCARTAR:
        if termo in texto_completo:
            return True
    # Verificar se tem muito pouca substância (poucos parágrafos curtos)
    if len(paragrafos) <= 2:
        texto_curto = " ".join(paragrafos).strip()
        if len(texto_curto) < 200:
            return True
    return False

def calcular_relevancia(titulo, paragrafos):
    """
    Calcula a relevância da nota baseada nos temas do contexto.
    Retorna (score, temas_encontrados, passagens_relevantes)
    """
    texto_completo = (titulo + " " + " ".join(paragrafos)).lower()
    score = 0
    temas_encontrados = []
    passagens_relevantes = []
    
    for tema, palavras_chave in TEMAS_CENTRAIS.items():
        tema_encontrado = False
        for palavra in palavras_chave:
            if palavra.lower() in texto_completo:
                if not tema_encontrado:
                    temas_encontrados.append(tema)
                    tema_encontrado = True
                    score += 2  # Peso base por tema
                
                # Encontrar passagens relevantes (até 3 por tema)
                for i, paragrafo in enumerate(paragrafos):
                    if palavra.lower() in paragrafo.lower() and len(passagens_relevantes) < 3:
                        # Limitar tamanho da passagem
                        passagem = paragrafo[:300] + "..." if len(paragrafo) > 300 else paragrafo
                        if passagem not in passagens_relevantes:
                            passagens_relevantes.append(passagem)
    
    # Bonus por múltiplos temas (indica conexão mais profunda)
    if len(temas_encontrados) >= 3:
        score += 3
    elif len(temas_encontrados) >= 2:
        score += 1
    
    return score, temas_encontrados, passagens_relevantes

def gerar_justificativa(titulo, temas_encontrados, passagens_relevantes):
    """Gera justificativa de 2-3 frases baseada nos temas e passagens."""
    if not temas_encontrados:
        return ""
    
    # Mapear temas para descrições legíveis
    tema_descricoes = {
        "governanca_global_digital": "governança global digital",
        "marco_civil_internet": "Marco Civil da Internet",
        "lgpd_protecao_dados": "LGPD e proteção de dados",
        "soberania_digital": "soberania digital",
        "multilateralismo_onu": "multilateralismo e ONU",
        "multissetorialidade": "governança multissetorial",
        "direitos_humanos_online": "direitos humanos online",
        "cooperacao_internacional_foros": "cooperação internacional em foros",
        "ia_inteligencia_artificial": "inteligência artificial",
        "infraestrutura_critica": "infraestrutura crítica digital",
        "ciberseguranca": "cibersegurança",
        "dominio_amazon_icann": "disputa do domínio .amazon/ICANN",
        "suspensao_x_twitter": "suspensão do X/Twitter no Brasil"
    }
    
    temas_legiveis = [tema_descricoes.get(t, t) for t in temas_encontrados[:4]]
    
    justificativa = (
        f"A nota aborda {', '.join(temas_legiveis[:2])}"
        + (f" e {temas_legiveis[2]}" if len(temas_legiveis) > 2 else "")
        + (f" e {temas_legiveis[3]}" if len(temas_legiveis) > 3 else "")
        + f", temas centrais da pesquisa sobre posicionamento do MRE na governança global digital. "
    )
    
    if passagens_relevantes:
        justificativa += (
            f"Contém informações qualitativas sobre posicionamentos, ações ou articulações "
            f"do Ministério em foros internacionais e políticas domésticas correlatas. "
            f"Trechos relevantes demonstram a atuação concreta do MRE nesses temas."
        )
    else:
        justificativa += (
            f"Traz informações qualitativas relevantes para análise da política externa "
            f"brasileira em governança digital no período 2014-2025."
        )
    
    return justificativa

def processar_arquivo_json(caminho_arquivo):
    """Processa um arquivo JSON de notas à imprensa."""
    notas_relevantes = []
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        return notas_relevantes
    
    # Navegar na estrutura _default
    if "_default" not in dados:
        return notas_relevantes
    
    for chave, nota in dados["_default"].items():
        try:
            titulo = nota.get("titulo", "").strip()
            data = nota.get("data", "").strip()
            link = nota.get("link", "").strip()
            paragrafos = nota.get("paragrafos", [])
            
            if not titulo or not paragrafos:
                continue
            
            # Descartar notas de calendário/agenda
            if eh_nota_calendario(titulo, paragrafos):
                continue
            
            # Calcular relevância
            score, temas_encontrados, passagens_relevantes = calcular_relevancia(titulo, paragrafos)
            
            # Considerar relevante se score >= 2 (pelo menos 1 tema forte ou 2 temas)
            if score >= 2 and temas_encontrados:
                justificativa = gerar_justificativa(titulo, temas_encontrados, passagens_relevantes)
                
                nota_filtrada = {
                    "titulo": titulo,
                    "data": data,
                    "link": link,
                    "justificativa": justificativa,
                    "passagens_relevantes": " | ".join(passagens_relevantes[:3]),
                    "temas": temas_encontrados,
                    "score": score,
                    "nota_original": nota
                }
                notas_relevantes.append(nota_filtrada)
                
        except Exception as e:
            print(f"Erro ao processar nota {chave} em {caminho_arquivo}: {e}")
            continue
    
    return notas_relevantes

def main():
    print("=" * 60)
    print("FILTRAGEM DE NOTAS À IMPRENSA DO MRE - GOVERNANÇA DIGITAL")
    print("Período: 2014-2025 | Contexto: contexto01.md")
    print("=" * 60)
    
    # Listar arquivos JSON
    arquivos_json = sorted(JSON_NOTAS_DIR.glob("*.json"))
    print(f"\nEncontrados {len(arquivos_json)} arquivos JSON para processar.")
    
    todas_notas_relevantes = []
    total_notas_analisadas = 0
    total_notas_descartadas = 0
    
    for i, arquivo in enumerate(arquivos_json, 1):
        print(f"\n[{i}/{len(arquivos_json)}] Processando: {arquivo.name}")
        
        notas_relevantes = processar_arquivo_json(arquivo)
        todas_notas_relevantes.extend(notas_relevantes)
        
        # Contar notas no arquivo para estatísticas
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            if "_default" in dados:
                total_arquivo = len(dados["_default"])
                total_notas_analisadas += total_arquivo
                total_notas_descartadas += (total_arquivo - len(notas_relevantes))
                print(f"  -> {total_arquivo} notas no arquivo, {len(notas_relevantes)} relevantes")
        except:
            pass
    
    print("\n" + "=" * 60)
    print("RESUMO DA FILTRAGEM")
    print("=" * 60)
    print(f"Total de notas analisadas: {total_notas_analisadas}")
    print(f"Notas identificadas como pertinentes: {len(todas_notas_relevantes)}")
    print(f"Notas desconsideradas: {total_notas_descartadas}")
    
    # Ordenar por score (mais relevantes primeiro) e depois por data
    todas_notas_relevantes.sort(key=lambda x: (-x["score"], x["data"]))
    
    # Gerar nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    modelo = "nemotron3ultra"
    
    # Salvar CSV
    csv_path = RESULTADOS_DIR / f"filtragem_{modelo}-{timestamp}.csv"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["Titulo", "Data", "Link", "Justificativa", "Passagens_Relevantes"])
        for nota in todas_notas_relevantes:
            writer.writerow([
                nota["titulo"],
                nota["data"],
                nota["link"],
                nota["justificativa"],
                nota["passagens_relevantes"]
            ])
    print(f"\nCSV salvo em: {csv_path}")
    
    # Salvar JSON (estrutura compatível com original)
    json_path = JSONS_FILTRADOS_DIR / f"json-filtragem-{modelo}-{timestamp}.json"
    json_output = {"_default": {}}
    for idx, nota in enumerate(todas_notas_relevantes, 1):
        # Manter estrutura original mas adicionar campos de análise
        nota_original = nota["nota_original"].copy()
        nota_original["analise_relevancia"] = {
            "temas_identificados": nota["temas"],
            "score_relevancia": nota["score"],
            "justificativa_selecao": nota["justificativa"],
            "passagens_relevantes": nota["passagens_relevantes"].split(" | ")
        }
        json_output["_default"][str(idx)] = nota_original
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"JSON salvo em: {json_path}")
    
    # Estatísticas por tema
    print("\nDistribuição por temas identificados:")
    tema_contador = {}
    for nota in todas_notas_relevantes:
        for tema in nota["temas"]:
            tema_contador[tema] = tema_contador.get(tema, 0) + 1
    
    for tema, count in sorted(tema_contador.items(), key=lambda x: -x[1]):
        print(f"  {tema}: {count} notas")
    
    print("\n✅ Filtragem concluída com sucesso!")

if __name__ == "__main__":
    main()