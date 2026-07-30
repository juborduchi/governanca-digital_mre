# Relatório de Análise com Gráficos
## Escala Ordinal - Posicionamento do MRE

**Arquivo**: escala-ordinal_mimo-2026-07-30.csv  
**Total**: 7 registros | **Período**: 2025

---

## 1. Resumo Executivo

```
╔═══════════════════════════════════════════════════════════════╗
║  TOTAL: 7 notas  │  MÉDIA: 2.43  │  MODA: 2           ║
║  TENDÊNCIA: SOBERANISTA                                      ║
╚═══════════════════════════════════════════════════════════════╝
```

| Métrica | Valor |
|---------|-------|
| Total | 7 |
| Média | 2.43 |
| Moda | 2 |
| Mín-Máx | 2-3 |

---

## 2. Gráfico de Barras Horizontais

### Distribuição por Nota

```
Nota 1 (Extremo Soberanista)  ░░░░░░░░░░░░░░░░░░░░  0.0% (0)
Nota 2 (Soberanista)         ████████████████████  57.1% (4)
Nota 3 (Misto)               ██████████████░░░░░░  42.9% (3)
Nota 4 (Liberal)             ░░░░░░░░░░░░░░░░░░░░  0.0% (0)
Nota 5 (Extremo Liberal)     ░░░░░░░░░░░░░░░░░░░░  0.0% (0)

                             0%       25%       50%       75%      100%
```

### Categorias Agregadas

```
Soberanista (1-2)  ████████████████████  57.1%
Misto (3)          ██████████████░░░░░░  42.9%
Liberal (4-5)      ░░░░░░░░░░░░░░░░░░░░   0.0%
```

---

## 3. Gráfico de Barras Verticais (Temporal)

### Notas por Mês

```
     |
  2  |     ██          ██
  1  |     ██    ██    ██    ██    ██    ██
  0  |_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____
       Jan   Fev   Mar   Abr   Mai   Jun   Jul   Ago   Set   Out   Nov   Dez
         0     2     1     0     0     0     1     0     0     1     2     0
```

### Por Trimestre

```
Q1 (Jan-Mar)  ████████████████  3 notas
Q2 (Abr-Jun)  ████████████░░░░  0 notas
Q3 (Jul-Set)  ████████████████  1 notas
Q4 (Out-Dez)  ████████████░░░░  3 notas
```

---

## 4. Histograma de Frequências

### Distribuição das Notas

```
Frequência
    │
  4  │         ██████████████████████████
  3  │         ██████████████████████████
  2  │         ██████████████████████████
  1  │         ██████████████████████████
  0  │_____|_________|_________|_________|_________|_____
           1         2         3         4         5
                        Nota
```

**Moda**: Nota 2 (4 ocorrências)

---

## 5. Gráfico de Pizza (ASCII)

### Composição por Categoria

```
                  ┌─────────────────────────────┐
                 ╱                               ╲
                ╱                                 ╲
               ╱         SOBERANISTA               ╲
              ╱            (57.1%)                  ╲
             ╱                 ▲                     ╲
            │                 ╱ ╲                     │
            │                ╱   ╲                    │
            │               ╱     ╲                   │
             ╲             ╱       ╲                 ╱
              ╲           ╱    MISTO╲               ╱
               ╲         ╱   (42.9%) ╲             ╱
                ╲       ╱             ╲           ╱
                 ╲     ╱               ╲         ╱
                  ╲   ╱                 ╲       ╱
                   ╲ ╱                   ╲     ╱
                    ╲                     ╲   ╱
                     └─────────────────────┘
```

**Legenda**:
- `████` Soberanista: 4 notas (57.1%)
- `░░░░` Misto: 3 notas (42.9%)
- `    ` Liberal: 0 notas (0.0%)

---

## 6. Indicador de Posição na Escala

### Onde o MRE se Posiciona

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   SOBERANISTA                                              LIBERAL          │
│        1            2            3            4            5                │
│        │            │            │            │            │                │
│        ├────────────┼────────────┼────────────┼────────────┤                │
│                     ▲                                                 │
│                    ╱│╲                                                │
│                   ╱ │ ╲                                               │
│                  ╱  │  ╲                                              │
│                     │                                                 │
│                MÉDIA: 2.43                                              │
│                                                                             │
│   [████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   │
│   1                        2.43                                 5          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Posicionamento**: Tendência **Soberanista** (média 2.43)

---

## 7. Mapa de Calor (ASCII)

### Distribuição por Mês e Nota

```
┌────────────────────────────────────────────────────────────────────────────┐
│          Jan   Fev   Mar   Abr   Mai   Jun   Jul   Ago   Set   Out   Nov   Dez  │
├────────────────────────────────────────────────────────────────────────────┤
│ Nota 1  │  ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░ │
├────────────────────────────────────────────────────────────────────────────┤
│ Nota 2  │  ░░   ██   ░░   ░░   ░░   ░░   ██   ░░   ░░   ██   ░░   ░░ │
├────────────────────────────────────────────────────────────────────────────┤
│ Nota 3  │  ░░   ░░   ██   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ██   ░░ │
├────────────────────────────────────────────────────────────────────────────┤
│ Nota 4  │  ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░ │
├────────────────────────────────────────────────────────────────────────────┤
│ Nota 5  │  ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░   ░░ │
└────────────────────────────────────────────────────────────────────────────┘

LEGENDA: ░░ = 0 registros  │  ██ = 1+ registros
```

---

## 8. Tabela de Distribuição Completa

| Nota | Descrição | Qtd | % | Gráfico |
|------|-----------|-----|---|---------|
| 1 | Extremo Soberanista | 0 | 0.0% | `░░░░░░░░░░░░░░░░░░░░` |
| 2 | Soberanista | 4 | 57.1% | `████████████████████` |
| 3 | Misto | 3 | 42.9% | `██████████████░░░░░░` |
| 4 | Liberal | 0 | 0.0% | `░░░░░░░░░░░░░░░░░░░░` |
| 5 | Extremo Liberal | 0 | 0.0% | `░░░░░░░░░░░░░░░░░░░░` |

---

## 9. Análise Temporal Detalhada

### Evolução Mensal (Gráfico de Linha)

```
Notas
  2 ┤                    ●
    │                    │
  1 ┤     ●────●────●───●────●────●────●────●────●────●
    │     │    │    │    │    │    │    │    │    │    │
  0 ┼─────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────
        Jan  Fev  Mar  Abr  Mai  Jun  Jul  Ago  Set  Out  Nov  Dez
         0    2    1    0    0    0    1    0    0    1    2    0
```

### Resumo Trimestral

| Trimestre | Qtd | % | Gráfico |
|-----------|-----|---|---------|
| Q1 | 3 | 42.9% | `████████████████` |
| Q2 | 0 | 0.0% | `██████████░░░░░░` |
| Q3 | 1 | 14.3% | `████████████████` |
| Q4 | 3 | 42.9% | `██████████░░░░░░` |

---

## 10. Padrões e Insights

### Padrões Identificados

1. **Concentração em Notas 2 e 3**: 100.0% dos dados
2. **Ausência de Extremos**: Nenhuma nota 1 ou 5
3. **Tendência Soberanista**: 57.1% na nota 2

### Observações

- Posicionamento **consistente** do MRE
- Equilíbrio entre **regulação** e **inovação**
- Foco em **multilateralismo**

---

## 11. Conclusão

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SÍNTESE DOS RESULTADOS                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  • Posicionamento: PREDOMINANTEMENTE SOBERANISTA                              ║
║  • Média: 2.43 (escala 1-5)                                                 ║
║  • Tendência: Soberania digital + Multilateralismo + Proteção de direitos     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

**Fonte**: escala-ordinal_mimo-2026-07-30.csv  
**Gerado em**: 30/07/2026 17:55  
**Modelo**: mimo
