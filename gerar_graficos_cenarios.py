import matplotlib.pyplot as plt
import numpy as np

# Dados dos 4 cenários (10, 50, 100 utilizadores)
cenarios = {
    "Cenário 1: Python COM Cache (Redis)": {
        "mediana": [1117.0, 2011.6, 3011.28],
        "maximo": [1790, 2361, 3361]
    },
    "Cenário 2: Python SEM Cache": {
        "mediana": [1308.0, 2013.68, 3027.24],
        "maximo": [1809, 2506, 3506]
    },
    "Cenário 3: Ruby COM Cache (Redis)": {
        "mediana": [1304.0, 2011.49, 3014.21],
        "maximo": [1988, 2364, 3499]
    },
    "Cenário 4: Ruby SEM Cache": {
        "mediana": [1310.0, 2011.43, 3301.13],
        "maximo": [2047, 2715, 3879]
    }
}

labels = ['10 Usuários', '50 Usuários', '100 Usuários']
x = np.arange(len(labels))
width = 0.35

for i, (titulo, dados) in enumerate(cenarios.items(), 1):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    bar1 = ax.bar(x - width/2, dados["mediana"], width, label='Mediana (ms)', color='#4f5b66')
    bar2 = ax.bar(x + width/2, dados["maximo"], width, label='Tempo Máximo (ms)', color='#2b6cb0')
    
    ax.set_ylabel('Milissegundos (ms)', fontsize=12)
    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    
    # NOVIDADE: Aumenta o limite superior do eixo Y em 15% para os números não cortarem
    max_y = max(max(dados["mediana"]), max(dados["maximo"]))
    ax.set_ylim(0, max_y * 1.15)
    
    # Legenda movida para baixo do gráfico
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bar1 + bar2:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'imagens/grafico_cenario{i}.png', bbox_inches='tight')
    plt.close()

print("Gráficos gerados com sucesso na pasta 'imagens/' com limite de margem corrigido!")