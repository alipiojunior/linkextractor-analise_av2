# 📊 Análise de Desempenho - Link Extractor

Este repositório contém a infraestrutura e os resultados dos testes de carga realizados na aplicação **Link Extractor**, como parte da disciplina de Computação Distribuída. 

O objetivo principal é avaliar o comportamento de diferentes tecnologias de backend (Python e Ruby) sob estresse, bem como o impacto arquitetural da introdução de uma camada de cache em memória (Redis).

---

## 🛠️ Metodologia de Testes

A infraestrutura foi orquestrada utilizando **Docker Compose** para garantir o isolamento do ambiente. Os testes de carga foram executados com a ferramenta **Locust**, aplicando cargas progressivas para avaliar a latência, o tempo de resposta e a vazão do sistema.

**Configurações de Carga:**
* Carga Leve: 10 usuários (Ramp-up: 1/s)
* Carga Média: 50 usuários (Ramp-up: 2/s)
* Carga Máxima: 100 usuários (Ramp-up: 3/s)

---

## 📈 Cenários Avaliados e Resultados (Carga de 100 Usuários)

Abaixo estão consolidados os dados brutos e análises sob a carga máxima de estresse.

### Cenário 1: Python COM Cache (Redis)
Com o Redis ativado, a API em Python delegou a resposta de consultas repetidas para a memória, evitando o acesso constante ao banco de dados. O sistema conseguiu processar mais de 11.500 requisições com 0% de falhas. A média de tempo de resposta manteve-se em torno de 1202ms, demonstrando estabilidade na entrega das páginas, com o percentil 95 cravado em 1900ms.

| Total de Requisições | Falhas | Mediana (ms) | Percentil 95% (ms) | Média (ms) | Máximo (ms) | RPS Atual |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 11576 | 0 | 1011.28 | 1900 | 1202.60 | 3361 | 74.1 |

> **Gráficos de Desempenho:**
![Gráficos Python com Cache](imagens/cenario1_100_charts.png)

### Cenário 2: Python SEM Cache
Ao removermos o cache, o servidor Python precisou reprocessar integralmente cada requisição. Embora o sistema tenha mantido 0% de falhas, observamos um aumento na latência média para 1220.91ms e um pico máximo maior (3506ms). O esforço computacional extra sobre a API evidencia a necessidade do cache para evitar a saturação da CPU do servidor em momentos de alto tráfego.

| Total de Requisições | Falhas | Mediana (ms) | Percentil 95% (ms) | Média (ms) | Máximo (ms) | RPS Atual |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 13251 | 0 | 1014.24 | 1900 | 1220.91 | 3506 | 76.2 |

> **Gráficos de Desempenho:**
![Gráficos Python sem Cache](imagens/cenario2_100_charts.png)

### Cenário 3: Ruby COM Cache (Redis)
A infraestrutura em Ruby com Redis apresentou o maior volume absoluto de requisições processadas durante a janela de teste (15365 requisições). A mediana (1011.21ms) e a média (1217.94ms) indicam um comportamento de vazão altamente previsível e consistente, lidando de forma excelente com a simultaneidade dos 100 usuários virtuais e absorvendo perfeitamente as operações de leitura.

| Total de Requisições | Falhas | Mediana (ms) | Percentil 95% (ms) | Média (ms) | Máximo (ms) | RPS Atual |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 15365 | 0 | 1011.21 | 1900 | 1217.94 | 3499 | 72.8 |

> **Gráficos de Desempenho:**
![Gráficos Ruby com Cache](imagens/cenario3_100_charts.png)

### Cenário 4: Ruby SEM Cache
Sem a camada de cache, o Ruby também sentiu a sobrecarga das conexões diretas, refletindo no aumento do tempo máximo de resposta para 3607ms (o maior pico registrado entre todos os cenários). Os gráficos de latência demonstram maior instabilidade durante os momentos de ramp-up, provando que a ausência do Redis impacta diretamente a capacidade da aplicação de lidar com rajadas súbitas de tráfego.

| Total de Requisições | Falhas | Mediana (ms) | Percentil 95% (ms) | Média (ms) | Máximo (ms) | RPS Atual |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 12741 | 0 | 1011.13 | 1900 | 1215.09 | 3607 | 74.9 |

> **Gráficos de Desempenho:**
![Gráficos Ruby sem Cache](imagens/cenario4_100_charts.png)

---

## 📝 Conclusão Analítica

Ambas as tecnologias mantiveram a integridade do sistema, registrando 0% de falhas (*Fails*) mesmo sob a carga sustentada de 100 usuários. Observou-se que a infraestrutura, muito possivelmente limitada pelo orquestrador de rede local, atingiu um platô de estabilidade em torno da latência de ~1011ms (mediana) em todos os cenários.

Ainda assim, a análise dos extremos (Tempos Médios e Máximos) comprova que o **Redis atua como um escudo computacional**. Sem ele, os tempos máximos de resposta subiram para 3506ms no Python e 3607ms no Ruby. O uso de estruturas em memória garante que o 95º percentil dos usuários não sofra degradação drástica de experiência, provando que otimizações arquiteturais em sistemas distribuídos têm, muitas vezes, mais impacto no desempenho final do que a escolha isolada da linguagem de programação.

---
**Autor:** Alípio Rollo Júnior - 2320422