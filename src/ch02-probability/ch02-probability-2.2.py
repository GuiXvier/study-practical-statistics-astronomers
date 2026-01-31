import numpy as np
import matplotlib.pyplot as plt

def estrategia_escolha(noites_totais, noites_treino, qualidades):
    """
    Implementa a estratégia de escolha:
    1. Observa as primeiras 'noites_treino' noites
    2. Escolhe a primeira noite subsequente melhor que todas as observadas
    
    Retorna True se escolheu a melhor noite, False caso contrário
    """
    # Qualidade máxima nas noites de treino
    max_treino = max(qualidades[:noites_treino])
    
    # Procura a primeira noite melhor que o máximo do treino
    for i in range(noites_treino, noites_totais):
        if qualidades[i] > max_treino:
            # Verifica se esta é a melhor noite de todas
            return qualidades[i] == max(qualidades)
    
    # Se não encontrou nenhuma melhor, retorna False
    return False

def simular_estrategia(noites_totais, noites_treino, num_simulacoes=10000):
    """
    Simula a estratégia múltiplas vezes e calcula a taxa de sucesso
    """
    sucessos = 0
    
    for _ in range(num_simulacoes):
        # Gera qualidades aleatórias para as noites
        qualidades = np.random.uniform(0, 1, noites_totais)
        
        # Aplica a estratégia
        if estrategia_escolha(noites_totais, noites_treino, qualidades):
            sucessos += 1
    
    return sucessos / num_simulacoes

# PARTE 1: Verificar que 5 noites de treino dá ~25% de sucesso
print("=" * 70)
print("PARTE 1: Verificando a estratégia com 5 noites de treino")
print("=" * 70)

noites_totais = 10
noites_treino = 5
num_simulacoes = 100000

taxa_sucesso = simular_estrategia(noites_totais, noites_treino, num_simulacoes)

print(f"\nNúmero total de noites: {noites_totais}")
print(f"Noites de treino: {noites_treino}")
print(f"Número de simulações: {num_simulacoes:,}")
print(f"\nTaxa de sucesso: {taxa_sucesso:.4f} ({taxa_sucesso*100:.2f}%)")
print(f"Valor teórico esperado: 0.2500 (25.00%)")
print(f"Diferença: {abs(taxa_sucesso - 0.25)*100:.2f}%")

# PARTE 2: Encontrar a fração ótima (deve ser ~1/e ≈ 0.368)
print("\n" + "=" * 70)
print("PARTE 2: Encontrando a fração ótima de treino")
print("=" * 70)

# Testa diferentes frações de treino
fracoes_treino = np.linspace(0.1, 0.9, 30)
taxas_sucesso = []

print("\nTestando diferentes frações de treino...")
for fracao in fracoes_treino:
    noites_treino_teste = int(noites_totais * fracao)
    if noites_treino_teste == 0:
        noites_treino_teste = 1
    if noites_treino_teste >= noites_totais:
        noites_treino_teste = noites_totais - 1
    
    taxa = simular_estrategia(noites_totais, noites_treino_teste, 50000)
    taxas_sucesso.append(taxa)

# Encontra a fração ótima
idx_otimo = np.argmax(taxas_sucesso)
fracao_otima = fracoes_treino[idx_otimo]
taxa_otima = taxas_sucesso[idx_otimo]

print(f"\nFração ótima encontrada: {fracao_otima:.4f}")
print(f"Valor teórico (1/e): {1/np.e:.4f}")
print(f"Diferença: {abs(fracao_otima - 1/np.e):.4f}")
print(f"\nTaxa de sucesso com fração ótima: {taxa_otima:.4f} ({taxa_otima*100:.2f}%)")
print(f"Valor teórico esperado: {1/np.e:.4f} ({100/np.e:.2f}%)")

# PARTE 3: Visualização dos resultados
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Taxa de sucesso vs Fração de treino
ax1.plot(fracoes_treino, taxas_sucesso, 'b-', linewidth=2, label='Simulação')
ax1.axvline(1/np.e, color='r', linestyle='--', linewidth=2, label=f'1/e ≈ {1/np.e:.3f}')
ax1.axhline(1/np.e, color='g', linestyle='--', linewidth=1, alpha=0.5, label=f'Taxa ótima ≈ {1/np.e:.3f}')
ax1.scatter([fracao_otima], [taxa_otima], color='red', s=100, zorder=5, label=f'Máximo: ({fracao_otima:.3f}, {taxa_otima:.3f})')
ax1.set_xlabel('Fração de noites para treino', fontsize=11)
ax1.set_ylabel('Probabilidade de escolher a melhor noite', fontsize=11)
ax1.set_title('Otimização da Estratégia de Escolha', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Gráfico 2: Comparação para diferentes tamanhos de amostra
tamanhos = [10, 20, 50, 100]
cores = ['blue', 'green', 'orange', 'red']

for tamanho, cor in zip(tamanhos, cores):
    fracoes = np.linspace(0.1, 0.9, 25)
    taxas = []
    
    for fracao in fracoes:
        n_treino = int(tamanho * fracao)
        if n_treino == 0:
            n_treino = 1
        if n_treino >= tamanho:
            n_treino = tamanho - 1
        
        taxa = simular_estrategia(tamanho, n_treino, 20000)
        taxas.append(taxa)
    
    ax2.plot(fracoes, taxas, color=cor, linewidth=2, label=f'n = {tamanho}')

ax2.axvline(1/np.e, color='black', linestyle='--', linewidth=2, label=f'1/e ≈ {1/np.e:.3f}')
ax2.set_xlabel('Fração de treino', fontsize=11)
ax2.set_ylabel('Probabilidade de sucesso', fontsize=11)
ax2.set_title('Convergência para 1/e (diferentes tamanhos)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('efficient_choosing.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico salvo como 'efficient_choosing.png'")
plt.show()