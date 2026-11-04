import matplotlib.pyplot as plt
import numpy as np

# Dados dos 4 cenários (10, 50, 100 utilizadores)
cenarios = {
    "Cenário 1: Python COM Cache (Redis)": {
        "mediana": [3300.0, 1011.6, 1011.28],
        "maximo": [3519, 3361, 3361]
    },
    "Cenário 2: Python SEM Cache": {
        "mediana": [3300.0, 1013.68, 1014.24],
        "maximo": [3840, 3372, 3506]
    },
    "Cenário 3: Ruby COM Cache (Redis)": {
        "mediana": [3300.0, 1011.49, 1011.21],
        "maximo": [3369, 3364, 3499]
    },
    "Cenário 4: Ruby SEM Cache": {
        "mediana": [3300.0, 1011.43, 1011.13],
        "maximo": [3720, 3715, 3607]
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

print("Gráficos gerados com sucesso na pasta 'imagens/'!")