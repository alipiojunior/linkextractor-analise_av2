import matplotlib.pyplot as plt
import numpy as np

# Dados dos 4 cenários (100 usuários)
cenarios = ['Python\nCom Cache', 'Python\nSem Cache', 'Ruby\nCom Cache', 'Ruby\nSem Cache']
medias = [1202.60, 1220.91, 1217.94, 1215.09]
maximos = [3361, 3506, 3499, 3607]

x = np.arange(len(cenarios))
width = 0.35

# Criando a figura
fig, ax = plt.subplots(figsize=(10, 6))
barras_medias = ax.bar(x - width/2, medias, width, label='Tempo Médio (ms)', color='#4C72B0')
barras_maximos = ax.bar(x + width/2, maximos, width, label='Tempo Máximo (ms)', color='#C44E52')

# Configurando rótulos e título
ax.set_ylabel('Milissegundos (ms)', fontsize=12)
ax.set_title('Comparativo de Desempenho (100 Usuários) - Tempo Médio vs Máximo', fontsize=14, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(cenarios, fontsize=11)
ax.legend()

# Adicionando os valores exatos no topo de cada barra
ax.bar_label(barras_medias, padding=3, fmt='%.1f')
ax.bar_label(barras_maximos, padding=3, fmt='%.0f')

# Ajustando layout e salvando a imagem na pasta imagens
fig.tight_layout()
plt.savefig('imagens/comparativo_tempos.png', dpi=300)
print("Gráfico gerado com sucesso: imagens/comparativo_tempos.png")