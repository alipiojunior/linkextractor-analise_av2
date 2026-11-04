# 📊 Análise de Desempenho - Link Extractor

Este repositório documenta a infraestrutura e os resultados dos testes de carga realizados na aplicação **Link Extractor**, desenvolvida como projeto prático da disciplina de Computação Distribuída. 

O objetivo central foi avaliar o comportamento de diferentes tecnologias de backend (Python e Ruby) sob estresse e medir o impacto arquitetural da introdução de uma camada de cache em memória (Redis).

---

## 🛠️ Metodologia de Testes e Infraestrutura

A infraestrutura foi totalmente orquestrada utilizando **Docker Compose** para garantir o isolamento do ambiente (APIs, Base de Dados e Redis). Os testes de carga foram executados com a ferramenta **Locust**, aplicando um *ramp-up* progressivo:
* Carga Leve: 10 utilizadores (1/s)
* Carga Média: 50 utilizadores (2/s)
* Carga Máxima: 100 utilizadores (3/s)

### 🔄 Configuração de URLs e Comutação (Python vs. Ruby)
A aplicação recebe uma URL alvo como parâmetro de entrada. Para isolar as métricas de cada linguagem sem alterar o script de carga (`locustfile.py`), o tráfego gerado pelo Locust foi redirecionado para as portas específicas expostas pelo Docker Compose na rede local (`http://127.0.0.1`). O proxy encarregou-se de encaminhar a carga para o contentor correto, permitindo testar o Python e o Ruby de forma estritamente independente.

### 🧠 Controlo do Cache (Redis)
Os testes "Com e Sem Cache" validaram o comportamento da infraestrutura. Com o Redis ativo, a primeira requisição do Locust a uma URL processava a página e guardava-a em memória; as milhares de requisições seguintes eram entregues quase instantaneamente pelo Redis. No cenário "Sem Cache", o contentor do Redis foi ignorado, forçando as APIs a recalcular a extração de links a cada nova requisição, gerando sobrecarga de CPU.

---

## 📊 Visão Geral do Desempenho (Carga Máxima: 100 Utilizadores)

Para ilustrar o impacto do cache, o gráfico centralizado compara o **Tempo Médio** e o **Tempo Máximo** de resposta dos quatro cenários sob estresse.

![Gráfico Comparativo de Tempos](imagens/comparativo_tempos.png)

*(Nota: Embora as médias globais convirjam para ~1200 ms, a ausência da camada de cache provocou picos de latência máxima visivelmente superiores nos Cenários 2 e 4).*

---

## 📈 Análise Detalhada por Cenário (10, 50 e 100 Utilizadores)

### 🟢 Cenário 1: Python COM Cache (Redis)
A API em Python operou com eficiência, delegando a resposta de consultas repetidas para a memória.
![Cenário 1](imagens/grafico_cenario1.png)

**Resumo da Carga Máxima (100 Utilizadores):**
| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 11576 | 0 | 1011.28 | 1900 | 1202.60 | 3361 |

---

### 🔴 Cenário 2: Python SEM Cache
Sem a proteção da memória, o servidor precisou reprocessar integralmente cada requisição.
![Cenário 2](imagens/grafico_cenario2.png)

**Resumo da Carga Máxima (100 Utilizadores):**
| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 13251 | 0 | 1014.24 | 1900 | 1220.91 | 3506 |

---

### 🟢 Cenário 3: Ruby COM Cache (Redis)
A estabilidade na carga média e máxima demonstrou excelente sinergia entre o Ruby e o Redis.
![Cenário 3](imagens/grafico_cenario3.png)

**Resumo da Carga Máxima (100 Utilizadores):**
| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 15365 | 0 | 1011.21 | 1900 | 1217.94 | 3499 |

---

### 🔴 Cenário 4: Ruby SEM Cache
A API em Ruby absorveu diretamente todo o estresse, sendo empurrada aos limites do teste durante os picos.
![Cenário 4](imagens/grafico_cenario4.png)

**Resumo da Carga Máxima (100 Utilizadores):**
| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 12741 | 0 | 1011.13 | 1900 | 1215.09 | 3607 |

---

## 📝 Conclusões Finais

Ambas as linguagens mantiveram a integridade do sistema com 0% de falhas durante as fases de estresse. No entanto, a análise demonstra que o **Redis atua como um escudo computacional imprescindível**. A ausência da base de dados em memória elevou drasticamente as latências máximas nos picos de acesso. Melhorias arquiteturais trazem um impacto muito mais profundo na resiliência do que a escolha isolada da linguagem.

---
**Autor:** Alípio Fernando Gonçalves Rollo Júnior (Matrícula: 2320422/3)  
**Curso:** Ciência da Computação