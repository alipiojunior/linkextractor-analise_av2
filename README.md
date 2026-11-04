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
A aplicação recebe uma URL alvo como parâmetro de entrada. Para isolar as métricas de cada linguagem sem alterar o script de carga (`locustfile.py`), o tráfego gerado pelo Locust foi redirecionado para as portas específicas expostas pelo Docker Compose na rede local (`http://127.0.0.1`). O proxy encarregou-se de encaminhar a carga para o contentor correto, permitindo testar o Python e o Ruby de forma estritamente independente, através de requisições `GET` repetitivas.

### 🧠 Controlo do Cache (Redis)
Os testes "Com e Sem Cache" validaram o comportamento da infraestrutura. Com o Redis ativo, a primeira requisição do Locust a uma URL processava a página e guardava-a em memória; as milhares de requisições seguintes eram entregues quase instantaneamente pelo Redis. No cenário "Sem Cache", o contentor do Redis foi ignorado, forçando as APIs a recalcular a extração de links a cada nova requisição, o que gerou sobrecarga de CPU e picos de latência.

---

## 📊 Visão Geral do Desempenho (Carga Máxima: 100 Utilizadores)

Para ilustrar o impacto do cache, o gráfico abaixo (gerado em Python com a biblioteca Matplotlib) compara o **Tempo Médio** e o **Tempo Máximo** de resposta (em milissegundos) dos quatro cenários sob a carga máxima de estresse.

![Gráfico Comparativo de Tempos](imagens/comparativo_tempos.png)

*(Nota: Embora as médias globais convirjam para ~1200 ms, a ausência da camada de cache provocou picos de latência máxima visivelmente superiores nos Cenários 2 e 4, exigindo muito mais poder de processamento bruto dos servidores durante as rajadas de tráfego).*

---

## 📈 Análise Detalhada por Cenário (100 Utilizadores)

### Cenário 1: Python COM Cache (Redis)
A API delegou a resposta de consultas repetidas para a memória. O sistema processou de forma eficiente mais de 11.500 requisições, mantendo o percentil 95% estável em 1900 ms e absorvendo a simultaneidade sem esforço computacional excessivo.

| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 11576 | 0 | 1011.28 | 1900 | 1202.60 | 3361 |

### Cenário 2: Python SEM Cache
O servidor precisou reprocessar integralmente cada requisição, sem o auxílio da memória rápida. Este esforço evidenciou a vulnerabilidade da CPU perante picos de tráfego, resultando num pico máximo de resposta de 3506 ms.

| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 13251 | 0 | 1014.24 | 1900 | 1220.91 | 3506 |

### Cenário 3: Ruby COM Cache (Redis)
Apresentou o maior volume absoluto de requisições consolidadas no teste (15.365). A mediana e a média comprovam um comportamento de vazão altamente previsível e robusto, absorvendo as operações de leitura simultâneas com distinção.

| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 15365 | 0 | 1011.21 | 1900 | 1217.94 | 3499 |

### Cenário 4: Ruby SEM Cache
Sem a barreira protetora do cache, o backend em Ruby sentiu as rajadas iniciais, registando o maior pico de latência de toda a análise (3607 ms). Demonstrou que o *ramp-up* inicial gera uma instabilidade acentuada até que o servidor consiga estabilizar as filas de processos.

| Total de Requisições | Falhas | Mediana (ms) | P95% (ms) | Média (ms) | Máximo (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 12741 | 0 | 1011.13 | 1900 | 1215.09 | 3607 |

---

## 🔍 Histórico de Escalabilidade (Progressão de Carga)

<details>
<summary>👉 <b>Clique aqui para expandir os gráficos de desempenho do Locust (10 e 50 Utilizadores)</b></summary>
<br>
O comportamento do sistema durante as fases iniciais de escalabilidade. Pode observar-se a transição da carga leve (10 utilizadores) para a carga média (50 utilizadores), comprovando a estabilidade da aplicação antes do pico de estresse máximo.

### Cenário 1: Python COM Cache
**Carga de 10 e 50 Utilizadores:**
<img src="imagens/cenario1_10_charts.png" width="48%"> <img src="imagens/cenario1_50_charts.png" width="48%">

### Cenário 2: Python SEM Cache
**Carga de 10 e 50 Utilizadores:**
<img src="imagens/cenario2_10_charts.png" width="48%"> <img src="imagens/cenario2_50_charts.png" width="48%">

### Cenário 3: Ruby COM Cache
**Carga de 10 e 50 Utilizadores:**
<img src="imagens/cenario3_10_charts.png" width="48%"> <img src="imagens/cenario3_50_charts.png" width="48%">

### Cenário 4: Ruby SEM Cache
**Carga de 10 e 50 Utilizadores:**
<img src="imagens/cenario4_10_charts.png" width="48%"> <img src="imagens/cenario4_50_charts.png" width="48%">

</details>

---

## 📝 Conclusões Finais

Ambas as linguagens de programação mantiveram a total integridade do sistema, alcançando a marca de 0% de falhas (*fails*) durante as fases de estresse prolongado. No entanto, a análise dos extremos (Tempos Máximos) consolida a tese de que o **Redis atua como um escudo computacional imprescindível**. 

A ausência de uma base de dados em memória para mitigar o reprocessamento de leituras elevou drasticamente as latências máximas. Em sistemas distribuídos modernos, otimizações arquiteturais e a correta aplicação de componentes de cache trazem um impacto muito mais profundo na resiliência e na experiência do utilizador final do que a mera escolha da linguagem de desenvolvimento da API.

---
**Autor:** Alípio Fernando Gonçalves Rollo Júnior (Matrícula: 2320422/3)  
**Curso:** Ciência da Computação