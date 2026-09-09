# Contagem de Palavras — Em que sentido o MRE aborda "internet"

Opção 1 da análise semântica. Cada notebook lê um PDF de `../../relatorios-gestao-mre/` e mede o vocabulário ao redor de `internet`.

## Estrutura
- `config.py` — termo central, janela (±50 tokens), léxicos A (Soberana/Multilateral) e B (Mercado/Inovação), mapa ano->PDF
- `utils.py` — `extract_text`, `extrair_contextos`, `contar_lexicos`, `analisar_texto`
- `analise_2020.ipynb` ... `analise_2025.ipynb` — um por ano, mesma lógica, só muda `ANO` e `PDF_FILE`
- Comparar resultados entre anos para evolução temporal

## Como rodar
```bash
pip install pymupdf pandas matplotlib
jupyter lab analise_2020.ipynb
```
Ou direto via python:
```python
from pathlib import Path
from config import *
from utils import extract_text, analisar_texto
texto = extract_text("../../relatorios-gestao-mre/relatorio-gestao-mre-2021.pdf")
res = analisar_texto(texto, TERMO_CENTRAL_REGEX, ABORDAGEM_A_TERMOS, ABORDAGEM_B_TERMOS)
print(res)
```

## Léxicos atuais
- A: multilateral*, multissetorial*, governança, democrática/o, soberania/soberano/a
- B: autorregulação, inovação, desenvolvimento, mercado, investimento(s)
Edite `config.py` para expandir.
