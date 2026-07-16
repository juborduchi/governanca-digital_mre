import os
import json
import time
import glob
import re
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from tqdm import tqdm
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ============================================================
# 1. PREPARAÇÃO DO AMBIENTE E CONFIGURAÇÕES
# ============================================================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("=" * 60)
    print("ERRO: A variável GEMINI_API_KEY não foi encontrada.")
    print("Abra o arquivo .env e cole sua chave de API do Gemini.")
    print("Obtenha sua chave em: https://aistudio.google.com/apikey")
    print("=" * 60)
    exit(1)

client = genai.Client(api_key=API_KEY)

DIR_NOTAS = "json-notas"
ARQUIVO_PROGRESSO = "progresso_analise.json"
ARQUIVO_FINAL = "relatorio_governanca_digital.xlsx"

# Tempo de espera inicial entre requisições (ajusta dinamicamente se atingir o limite de taxa)
DELAY_ENTRE_REQUISICOES = 0.3

# ============================================================
# 2. ESQUEMA DE RESPOSTA ESTRUTURADA (PYDANTIC)
# ============================================================
class AnaliseNota(BaseModel):
    relevante: bool = Field(
        description=(
            "PRIMEIRO, analise se a nota aborda diretamente os conceitos de "
            "Governança Global Digital, Governança da Inteligência Artificial "
            "ou Governança da Internet. Retorne true APENAS se o tema central "
            "ou um dos temas principais da nota estiver relacionado a esses conceitos. "
            "Notas que apenas mencionam tecnologia de passagem, calendários de eventos "
            "ou temas genéricos de cooperação internacional NÃO devem ser consideradas relevantes."
        )
    )
    nota: Optional[int] = Field(
        default=None,
        description=(
            "SOMENTE se 'relevante' for true, atribua uma nota de 1 a 5: "
            "1 = Total alinhamento com Soberania Digital (direitos fundamentais, "
            "multilateralismo, multissetorialismo, garantias democráticas); "
            "2 = Predominantemente soberanista com alguma abertura; "
            "3 = Modelo Misto (equilíbrio entre soberania/direitos e "
            "desenvolvimento/inovação, não puramente mercantil); "
            "4 = Predominantemente liberal com alguma regulação; "
            "5 = Total alinhamento com Baixa Intervenção Estatal "
            "(inovação livre, autorregulação, lógica mercantil). "
            "Se 'relevante' for false, deixe como null."
        )
    )
    justificativa: str = Field(
        description=(
            "Se relevante: explique detalhadamente o posicionamento identificado "
            "nos parágrafos da nota à imprensa, citando evidências do texto. "
            "Se não relevante: explique brevemente por que a nota não se enquadra."
        )
    )

# ============================================================
# 3. PROMPT DO SISTEMA (INSTRUÇÕES DO ESPECIALISTA)
# ============================================================
SYSTEM_INSTRUCTION = """Você é um profissional e pesquisador sênior na área de Relações Internacionais com foco de estudo em Governança Global Digital, incluindo Governança de IA e Governança da Internet.

Você está auxiliando uma pesquisa cujo objetivo principal é analisar o posicionamento do Ministério das Relações Exteriores (MRE) do Brasil em relação à questão da Governança Global Digital.

## DEFINIÇÕES CONCEITUAIS QUE VOCÊ DEVE UTILIZAR:

**GOVERNANÇA GLOBAL**: Um sistema composto por um conjunto de padrões, princípios, normas, regras e/ou costumes, envolvendo tanto ambientes formais quanto informais, que guiam e/ou conduzem as ações de atores das relações internacionais. Estes padrões não necessariamente são preceitos formalizados, podendo constituir-se de condutas tomadas como padrão por diferentes instituições. A criação e a definição de tais padrões é guiada por questões que possuem alcance e interesse de vários membros do sistema internacional, os afetando de diferentes maneiras.

**GOVERNANÇA GLOBAL DIGITAL**: Governança Global Digital requer uma cooperação global para atingir benefícios econômicos e lidar com desafios das transformações digitais, compreendendo questões como a Internet e o fluxo de dados transfronteiriços.

**GOVERNANÇA DA INTELIGÊNCIA ARTIFICIAL**: Um sistema de processos, regras, práticas e ferramentas tecnológicas que são aplicadas para garantir um uso de tecnologias de IA por organizações que estejam em concordância com as estratégias, objetivos e valores de tal instituição, além de seguir requisitos legais e atender a princípios éticos de IA adotados pela entidade.

**GOVERNANÇA DA INTERNET**: O desenvolvimento e aplicação por Governos, pelo setor privado e pela sociedade civil, em seus respectivos papeis, de princípios, normas, regras, processos de tomadas de decisão e programas compartilhados que definem a evolução e uso da internet.

## ESCALA DE CLASSIFICAÇÃO (1 a 5):

Existem dois extremos de como a governança digital pode ser encarada:

**Nota 1 - Soberania Digital**: Abordagem que leva em consideração a soberania digital de um país, com garantias democráticas e dos direitos fundamentais dos seres humanos, com abordagens multilaterais e multissetoriais nas discussões e regulações.

**Nota 2 - Predominantemente Soberanista**: Foco principal na soberania e direitos, mas com alguma abertura para inovação e cooperação com o setor privado.

**Nota 3 - Modelo Misto**: Uma mistura das duas abordagens, onde se preza tanto pela garantia da soberania quanto pelo desenvolvimento e inovações — não necessariamente na lógica mercantil.

**Nota 4 - Predominantemente Liberal**: Foco principal na inovação e abertura de mercado, mas com alguma regulação estatal presente.

**Nota 5 - Baixa Intervenção Estatal**: Modelo marcado pela baixa intervenção estatal, que valoriza a inovação e a autorregulação.

## INSTRUÇÕES DE ANÁLISE:

1. Leia atentamente o texto dos parágrafos da nota à imprensa.
2. PRIMEIRO, determine se a nota é RELEVANTE para os temas de Governança Global Digital, Governança da IA ou Governança da Internet. Uma nota que fala apenas de comércio, visitas diplomáticas genéricas, questões humanitárias sem conexão digital, ou calendários de eventos NÃO é relevante.
3. SOMENTE SE a nota for relevante, analise o posicionamento do MRE e atribua uma nota de 1 a 5 na escala acima.
4. Forneça uma justificativa detalhada baseada estritamente no conteúdo dos parágrafos."""


# ============================================================
# 4. FUNÇÕES AUXILIARES
# ============================================================

def carregar_anos_disponiveis() -> List[int]:
    """Escaneia o diretório e identifica os anos disponíveis nos nomes dos arquivos."""
    padrao = os.path.join(DIR_NOTAS, "*.json")
    arquivos = glob.glob(padrao)
    anos = set()
    for arq in arquivos:
        match = re.search(r'-(\d{4})-\d{2}\.json$', os.path.basename(arq))
        if match:
            anos.add(int(match.group(1)))
    return sorted(list(anos))


def contar_notas_por_ano(anos: List[int]) -> dict:
    """Conta quantas notas existem em cada ano para exibir ao usuário."""
    contagem = {}
    padrao = os.path.join(DIR_NOTAS, "*.json")
    arquivos = glob.glob(padrao)
    for arq in arquivos:
        match = re.search(r'-(\d{4})-\d{2}\.json$', os.path.basename(arq))
        if match:
            ano = int(match.group(1))
            if ano in anos:
                try:
                    with open(arq, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    if "_default" in dados:
                        contagem[ano] = contagem.get(ano, 0) + len(dados["_default"])
                    elif isinstance(dados, list):
                        contagem[ano] = contagem.get(ano, 0) + len(dados)
                except Exception:
                    pass
    return contagem


def extrair_notas_do_arquivo(caminho: str) -> List[dict]:
    """Extrai todas as notas individuais de um arquivo JSON no formato _default."""
    notas = []
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        if "_default" in dados:
            for chave, nota in dados["_default"].items():
                notas.append(nota)
        elif isinstance(dados, list):
            notas.extend(dados)
        elif isinstance(dados, dict):
            notas.append(dados)
    except Exception as e:
        print(f"\n  [Aviso] Erro ao ler {os.path.basename(caminho)}: {e}")
    return notas


def carregar_notas_do_periodo(ano_inicio: int, ano_fim: int) -> List[dict]:
    """Carrega todas as notas que pertencem ao intervalo de anos selecionado."""
    padrao = os.path.join(DIR_NOTAS, "*.json")
    arquivos = sorted(glob.glob(padrao))
    todas_notas = []

    for arq in arquivos:
        match = re.search(r'-(\d{4})-\d{2}\.json$', os.path.basename(arq))
        if match:
            ano_arq = int(match.group(1))
            if ano_inicio <= ano_arq <= ano_fim:
                notas_arquivo = extrair_notas_do_arquivo(arq)
                todas_notas.extend(notas_arquivo)

    return todas_notas


def gerar_id_nota(nota: dict) -> str:
    """Gera um identificador único para cada nota usando link + data + título."""
    link = nota.get("link", "")
    data = nota.get("data", "")
    titulo = nota.get("titulo", "")
    return f"{link}|{data}|{titulo}"


def carregar_progresso() -> tuple:
    """Carrega o progresso anterior se existir. Retorna (resultados, ids_processados)."""
    resultados = []
    ids_processados = set()
    if os.path.exists(ARQUIVO_PROGRESSO):
        try:
            with open(ARQUIVO_PROGRESSO, 'r', encoding='utf-8') as f:
                dados_progresso = json.load(f)
            resultados = dados_progresso.get("resultados", [])
            ids_processados = set(dados_progresso.get("ids_processados", []))
        except Exception:
            pass
    return resultados, ids_processados


def salvar_progresso(resultados: list, ids_processados: set):
    """Salva o progresso atual (resultados + IDs processados) em um JSON temporário."""
    dados = {
        "resultados": resultados,
        "ids_processados": list(ids_processados)
    }
    with open(ARQUIVO_PROGRESSO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def chamar_gemini(texto_paragrafos: str, max_tentativas: int = 6) -> Optional[AnaliseNota]:
    """Chama a API do Gemini com Structured Outputs e Exponential Backoff."""
    prompt_usuario = (
        "Analise os parágrafos da seguinte nota à imprensa do MRE do Brasil:\n\n"
        f"{texto_paragrafos}"
    )

    espera = 2
    for tentativa in range(max_tentativas):
        try:
            response = client.models.generate_content(
                model='gemini-flash-lite-latest',
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_schema=AnaliseNota,
                    temperature=0.1,
                ),
            )
            return response.parsed
        except APIError as e:
            global DELAY_ENTRE_REQUISICOES
            is_rate_limit = getattr(e, "code", None) in [429, 503] or "429" in str(e) or "503" in str(e)
            
            if is_rate_limit:
                if DELAY_ENTRE_REQUISICOES < 4.1:
                    DELAY_ENTRE_REQUISICOES = 4.1
                    print(f"\n  [Rate Limit / Sobrecarga] Ajustando tempo de espera padrão entre notas para {DELAY_ENTRE_REQUISICOES}s.")
                if tentativa == max_tentativas - 1:
                    raise e
                
                espera_rate_limit = 65
                print(f"\n  [Rate Limit] Cota excedida. Aguardando {espera_rate_limit}s antes de tentar novamente (Tentativa {tentativa+1}/{max_tentativas})...")
                time.sleep(espera_rate_limit)
            else:
                print(f"\n  [Erro de API] {e}")
                raise e
        except Exception as e:
            if tentativa == max_tentativas - 1:
                raise e
            print(f"\n  [Erro] {e}. Tentativa {tentativa + 1}/{max_tentativas}...")
            time.sleep(espera)
            espera *= 2
    return None


# ============================================================
# 5. FLUXO PRINCIPAL
# ============================================================

def main():
    print("=" * 60)
    print("  ANALISADOR DE GOVERNANÇA GLOBAL DIGITAL - MRE BRASIL")
    print("=" * 60)

    # --- Etapa 1: Identificar anos disponíveis ---
    anos = carregar_anos_disponiveis()
    if not anos:
        print(f"\nNenhum arquivo JSON encontrado na pasta '{DIR_NOTAS}'.")
        print("Verifique se a pasta existe e contém os arquivos de notas.")
        return

    contagem = contar_notas_por_ano(anos)

    print(f"\nAnos disponíveis nos arquivos ({len(anos)} anos):")
    print("-" * 40)
    for ano in anos:
        qtd = contagem.get(ano, "?")
        print(f"  {ano}  -  {qtd} notas")
    print("-" * 40)
    total_geral = sum(contagem.values())
    print(f"  Total geral: {total_geral} notas")

    # --- Etapa 2: Solicitar intervalo ao usuário ---
    print()
    try:
        ano_inicio = int(input(f"Digite o ano de INÍCIO do intervalo (mín: {anos[0]}): "))
        ano_fim = int(input(f"Digite o ano de FIM do intervalo (máx: {anos[-1]}): "))
    except ValueError:
        print("Entrada inválida. Digite apenas números inteiros.")
        return

    if ano_inicio > ano_fim:
        print("Erro: O ano de início deve ser menor ou igual ao ano final.")
        return

    if ano_inicio < anos[0] or ano_fim > anos[-1]:
        print(f"Erro: O intervalo deve estar entre {anos[0]} e {anos[-1]}.")
        return

    # --- Etapa 3: Carregar notas do período ---
    print("\nCarregando notas do período selecionado...")
    todas_notas = carregar_notas_do_periodo(ano_inicio, ano_fim)
    print(f"Total de {len(todas_notas)} notas encontradas no período {ano_inicio}-{ano_fim}.")

    if not todas_notas:
        print("Nenhuma nota encontrada no intervalo selecionado.")
        return

    # --- Recuperação de progresso ---
    resultados_finais, ids_processados = [], set()

    if os.path.exists(ARQUIVO_PROGRESSO):
        resposta = input(
            "\nUm progresso anterior foi encontrado. Continuar de onde parou? (s/n): "
        ).strip().lower()
        if resposta == 's':
            resultados_finais, ids_processados = carregar_progresso()
            print(f"Retomando: {len(ids_processados)} notas já processadas anteriormente.")
        else:
            os.remove(ARQUIVO_PROGRESSO)
            print("Progresso anterior descartado. Recomeçando do zero.")

    # --- Etapa 4: Análise com Gemini ---
    print("\nIniciando análise com a API do Gemini...")
    print("(Cada nota será enviada para o Gemini verificar relevância e classificar)\n")

    notas_relevantes_encontradas = 0

    for nota in tqdm(todas_notas, desc="Analisando notas", unit="nota"):
        id_nota = gerar_id_nota(nota)

        # Pula se já foi processada
        if id_nota in ids_processados:
            continue

        # Consolida os parágrafos
        paragrafos_lista = nota.get("paragrafos", [])
        if isinstance(paragrafos_lista, list):
            texto_consolidado = "\n".join(paragrafos_lista)
        else:
            texto_consolidado = str(paragrafos_lista)

        if not texto_consolidado.strip():
            ids_processados.add(id_nota)
            continue

        try:
            # Chama o Gemini: primeiro verifica relevância, depois dá nota
            analise = chamar_gemini(texto_consolidado)

            if analise and analise.relevante:
                dados_relatorio = {
                    "Data": nota.get("data", "Não informada"),
                    "Título": nota.get("titulo", "Sem título"),
                    "Link": nota.get("link", ""),
                    "Parágrafos": texto_consolidado,
                    "Nota Atribuída": analise.nota,
                    "Justificativa": analise.justificativa
                }
                resultados_finais.append(dados_relatorio)
                notas_relevantes_encontradas += 1

            # Marca como processada (relevante ou não)
            ids_processados.add(id_nota)

            # Salva progresso após cada nota
            salvar_progresso(resultados_finais, ids_processados)

            # Pequena pausa entre requisições (pode ser ajustada dinamicamente pelo gerenciador de limites)
            time.sleep(DELAY_ENTRE_REQUISICOES)

        except Exception as e:
            print(f"\n\nErro persistente na nota '{nota.get('titulo', '?')}': {e}")
            print("O progresso foi salvo. Execute o script novamente para continuar.")
            salvar_progresso(resultados_finais, ids_processados)
            break

    # --- Etapa 5: Geração da Planilha Excel ---
    if resultados_finais:
        print(f"\n{'=' * 60}")
        print(f"  RESULTADOS")
        print(f"{'=' * 60}")
        print(f"  Notas analisadas no total: {len(ids_processados)}")
        print(f"  Notas RELEVANTES encontradas: {len(resultados_finais)}")
        print(f"  Notas descartadas (irrelevantes): {len(ids_processados) - len(resultados_finais)}")

        df = pd.DataFrame(resultados_finais)
        colunas_ordem = ["Data", "Título", "Link", "Parágrafos", "Nota Atribuída", "Justificativa"]
        df = df[colunas_ordem]

        df.to_excel(ARQUIVO_FINAL, index=False, engine='openpyxl')
        print(f"\n  Planilha salva em: {ARQUIVO_FINAL}")

        # Distribuição das notas
        if "Nota Atribuída" in df.columns:
            print(f"\n  Distribuição das notas:")
            distribuicao = df["Nota Atribuída"].value_counts().sort_index()
            for nota_val, qtd in distribuicao.items():
                print(f"    Nota {nota_val}: {qtd} nota(s)")
    else:
        print("\nNenhuma nota relevante para Governança Global Digital foi encontrada no período.")

    # Limpa progresso se tudo foi processado
    if len(ids_processados) >= len(todas_notas):
        if os.path.exists(ARQUIVO_PROGRESSO):
            os.remove(ARQUIVO_PROGRESSO)
            print("\n  Arquivo de progresso temporário removido (análise completa).")

    print(f"\n{'=' * 60}")
    print("  Análise concluída!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()