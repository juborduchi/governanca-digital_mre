# Análise por IA — Embeddings Semânticos (Opção 2)

**Pergunta:** *Em que sentido o MRE aborda “internet” nos Relatórios de Gestão 2020-2025?*  
**Resposta da Opção 2:** Cada trecho que menciona `internet` vira um vetor (embedding) e é comparado a dois protótipos semânticos: **A Soberana/Multilateral** vs **B Mercado/Inovação**.

Diferente da `contagem_palavras` (Opção 1) que conta palavras exatas na janela, aqui a IA entende sinônimos e contexto: `regulação multilateral da rede` conta para A mesmo sem a palavra `soberania`.

---

## Como funciona

```
PDF -> texto -> chunks (parágrafos) -> filtra só chunks com "internet"
                                          |
modelo multilíngue (paraphrase-multilingual-MiniLM-L12-v2, 384 dims)
                                          |
             +----------------------------+-------------------+
             |                                                |
      centroide_A (média dos                     centroide_B (média dos
       embeddings de A)                          embeddings de B)
             |                                                |
             +----------- cosseno(chunk, centroide) ----------+
                              |
                 sim_A vs sim_B -> diff = sim_A - sim_B
                 diff>0 => A, diff<0 => B, |diff|<0.02 => neutro
```

1. **Extração** `utils.extract_text` usa `PyMuPDF` (fallback `PyPDF2`).
2. **Chunking** `chunk_por_paragrafo` quebra por parágrafos (2+ quebras de linha). Alternativa `janela_deslizante` em `config.py:CHUNK_TIPO` para PDFs mal formatados. Filtra só chunks com `TERMO_CENTRAL_REGEX = \binternet(s)?\b` se `FILTRAR_SOMENTE_COM_TERMO=True`.
3. **Centr óides** `gerar_centroides` codifica `ABORDAGEM_A_TERMOS` + `ABORDAGEM_A_FRASES` (frases-âncora são melhores que palavras isoladas) e tira a média L2-normalizada. Idem para B.
4. **Embeddings** `embed_chunks` gera vetores normalizados para cada chunk.
5. **Classificação** `classificar_chunks` faz `dot(chunk, centroide)` = cosseno e decide vencedor. Guarda `sim_A`, `sim_B`, `diff` para cada chunk.
6. **Agregação** conta `A/B/neutro` por ano e média `diff` ( >0 puxa soberano, <0 puxa mercado). Visualização: barras empilhadas + dispersão `sim_A x sim_B` (diagonal = empate).

**Por que não é o método do colab original?** `notebooks/relatorio-gestao-mre-colab/relatorio_gestao2021.ipynb:928` comparava `internet vs governança` no dicionário genérico da IA, sem ler o relatório. Aqui o vetor vem **do parágrafo real do MRE**.

## Estrutura

```
analise_IA/
  config.py              # modelo, léxicos, frases-âncora, chunking, mapa ano->PDF
  utils.py               # funções compartilhadas
  analise_2020.ipynb     # um por ano, mesma lógica, só muda ANO/PDF_FILE
  analise_2021.ipynb
  analise_2022.ipynb
  analise_2023.ipynb
  analise_2024.ipynb
  analise_2025.ipynb
  analise_comparativa.ipynb # roda todos os anos, plota evolução, salva comparativo_ia.csv
  requirements.txt
  README.md              # este arquivo
```

## Como usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
# ou manual:
pip install pymupdf sentence-transformers torch pandas matplotlib scikit-learn
```
> ~400 MB para `torch` + ~120 MB para o modelo na primeira execução (cache em `~/.cache/huggingface`).

### 2. Rodar um ano
```bash
jupyter lab analise_2020.ipynb   # ou analise_2021 ... analise_2025
# Executar células em ordem: extrai -> chunking -> carrega modelo -> classifica -> plota
```

Ou via Python puro:
```python
from pathlib import Path
from config import *
from utils import extract_text, chunk_por_paragrafo, filtrar_chunks_com_termo, carregar_modelo, gerar_centroides, embed_chunks, classificar_chunks

pdf = Path("/workspaces/governanca-digital_mre/relatorios-gestao-mre/relatorio-gestao-mre-2021.pdf")
texto = extract_text(pdf)
chunks = chunk_por_paragrafo(texto)
filtrados = filtrar_chunks_com_termo(chunks, TERMO_CENTRAL_REGEX)
model = carregar_modelo(MODELO_EMBEDDING)
ca, cb = gerar_centroides(model, ABORDAGEM_A_TERMOS, ABORDAGEM_B_TERMOS, ABORDAGEM_A_FRASES, ABORDAGEM_B_FRASES)
embs = embed_chunks(model, [f["texto"] for f in filtrados])
res = classificar_chunks(embs, ca, cb)
print(res[:2])
```

### 3. Comparar todos os anos
```bash
jupyter lab analise_comparativa.ipynb
# Gera: comparativo_ia.csv com colunas ano,chunks,A,B,neutro,media_diff
```

### 4. Ajustar léxicos
Edite `config.py`:
- `MODELO_EMBEDDING` para testar `distiluse-base-multilingual-cased-v2` (512d) ou `intfloat/multilingual-e5-large`
- `ABORDAGEM_A/B_TERMOS` e `ABORDAGEM_A/B_FRASES` — frases-âncora dão centr óide mais estável que palavras soltas
- `CHUNK_TIPO` / `CHUNK_TAMANHO` / `CHUNK_OVERLAP`
- `TERMO_CENTRAL_REGEX` para incluir `digital`, `cibernétic.*` etc
Re-execute os notebooks.

## Interpretar resultados
- `A > B` ou `media_diff > 0` => entorno de `internet` mais próximo do discurso soberano/multilateral naquele ano
- `TOP A/B` nos notebooks mostra os parágrafos âncora — leia para validar qualitativamente (ex: 2022 tem 19 chunks, 2025 tem 0)
- `neutro` (|diff|<0.02) indica trecho equidistante — útil para calibrar threshold

## Limitações
- Modelo multilíngue genérico, não treinado em diplomacia — considere validar 10-20% dos chunks manualmente
- `2025` com 0 menções a `internet` retorna vazio (esperado, não é erro)
- Primeira execução baixa modelo da Hugging Face (requer internet)

## Requisitos
```
pymupdf>=1.23
sentence-transformers>=2.2
torch>=2.0
pandas>=1.5
matplotlib>=3.7
scikit-learn>=1.2  # para t-SNE futuro
```
