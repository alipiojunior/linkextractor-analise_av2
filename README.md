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

## 📈 Cenários Avaliados e Resultados

Abaixo estão consolidados os resultados sob a **carga máxima de 100 usuários virtuais**, onde os gargalos do sistema se tornam mais evidentes.

### Cenário 1: Python COM Cache (Redis)
Com o Redis ativado, a API em Python consegue aliviar o processamento do banco de dados, mantendo a média de tempo de resposta baixa e os percentis (95% e 99%) estáveis.

> **Estatísticas - 100 Usuários:**
![Estatísticas Python com Cache](imagens/cenario1_100.png)

> **Gráficos de Desempenho:**
![Gráficos Python com Cache](imagens/cenario1_100_charts.png)

### Cenário 2: Python SEM Cache
Sem a camada de cache, o sistema reprocessa cada requisição do zero. Observa-se um aumento na variação do tempo de resposta, exigindo mais processamento da API para manter a taxa de zero falhas.

> **Estatísticas - 100 Usuários:**
![Estatísticas Python sem Cache](imagens/cenario2_100.png)

> **Gráficos de Desempenho:**
![Gráficos Python sem Cache](imagens/cenario2_100_charts.png)

### Cenário 3: Ruby COM Cache (Redis)
A versão em Ruby, quando apoiada pelo cache, apresenta uma vazão (Requests Per Second - RPS) altamente consistente, lidando de forma robusta com o pico de acesso.

> **Estatísticas - 100 Usuários:**
![Estatísticas Ruby com Cache](imagens/cenario3_100.png)

> **Gráficos de Desempenho:**
![Gráficos Ruby com Cache](imagens/cenario3_100_charts.png)

### Cenário 4: Ruby SEM Cache
Assim como no Python, a remoção do Redis sobrecarrega o servidor de aplicação. Os gráficos de latência demonstram picos mais agressivos durante o *ramp-up* inicial dos usuários, estabilizando em uma média ligeiramente mais alta após o período de aquecimento.

> **Estatísticas - 100 Usuários:**
![Estatísticas Ruby sem Cache](imagens/cenario4_100.png)

> **Gráficos de Desempenho:**
![Gráficos Ruby sem Cache](imagens/cenario4_100_charts.png)

---

## 📝 Conclusão

Ambas as linguagens (Python e Ruby) lidaram com as requisições sem apresentar falhas (0% de *Fails*) sob a carga estipulada de 100 usuários. No entanto, a análise dos dados evidencia que a presença do **Redis** atua como o principal nivelador de desempenho na arquitetura. 

A adoção do cache absorve o impacto de requisições simultâneas e repetitivas (GET), reduzindo a latência no 95º percentil e garantindo que o sistema escale sem prejudicar a experiência do usuário final, independentemente da linguagem escolhida para o desenvolvimento da API.

---
**Autor:** Alípio Rollo Júnior (Matrícula: 2320422)