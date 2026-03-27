# Benchmark de Estruturas de Dados

Este projeto executa benchmarks comparando diferentes estruturas de dados, analisando métricas como tempo de CPU, uso de memória e número médio de iterações.

## 📦 Pré-requisitos

Instale as dependências necessárias:

```
pip install psutil tabulate matplotlib
```

## ▶️ Como executar

No diretório raiz do projeto, execute:

```
python main.py
```

## 📊 Resultados

Após a execução:

* Os resultados em tabela serão exibidos no terminal
* Os gráficos serão gerados automaticamente no diretório:

```
/results
```

## 📁 Estrutura dos resultados

Os gráficos são organizados da seguinte forma:

* `results/general/` → comparação entre todas as estruturas
* `results/individuals/binary_tree/` → apenas árvores binárias
* `results/individuals/hash_table/` → apenas tabelas hash

Cada pasta contém gráficos para:

* Inserção (`insertion`)
* Busca (`search`)

## 📝 Observações

* Os benchmarks são executados em múltiplas rodadas para maior precisão
* Os valores exibidos representam médias dos resultados obtidos
* O desempenho pode variar dependendo do hardware da máquina
