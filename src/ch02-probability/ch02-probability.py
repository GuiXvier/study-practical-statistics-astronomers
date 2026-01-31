from random import randint
from time import sleep
from collections import Counter

def simular_jogo(num_lancamentos, mostrar_detalhes=False):
    """
    Simula um jogo de cara ou coroa e retorna estatísticas.
    """
    pts_a = 0  # Cara (0)
    pts_b = 0  # Coroa (1)
    
    mudancas_lideranca = 0
    momento_ultima_virada = -1
    historico_diferencas = []
    lider_anterior = None
    
    if mostrar_detalhes:
        print("Jogo começou, ambos os jogadores estão com 0 pontos")
        sleep(1)
    
    for rodada in range(1, num_lancamentos + 1):
        # Lançamento da moeda
        resultado = randint(0, 1)
        
        if resultado == 0:
            pts_a += 1
        else:
            pts_b += 1
        
        # Determinar líder atual (NUNCA considera empate como líder)
        if pts_a > pts_b:
            lider_atual = 'A'
        elif pts_b > pts_a:
            lider_atual = 'B'
        else:
            lider_atual = None  # Empate não é liderança
        
        # Detectar mudança de liderança
        # Só conta mudança se AMBOS os líderes são válidos (não None) E são diferentes
        if lider_anterior is not None and lider_atual is not None:
            if lider_anterior != lider_atual:
                mudancas_lideranca += 1
                momento_ultima_virada = rodada
                if mostrar_detalhes:
                    print(f"Rodada {rodada}: Jogador {lider_atual} assumiu a liderança! ({pts_a}-{pts_b})")
        
        # Atualizar líder anterior (apenas se houver líder)
        if lider_atual is not None:
            lider_anterior = lider_atual
        
        # Registrar diferença absoluta
        diferenca = abs(pts_a - pts_b)
        historico_diferencas.append(diferenca)
    
    # Calcular estatísticas
    diferenca_final = abs(pts_a - pts_b)
    diferenca_media = sum(historico_diferencas) / len(historico_diferencas)
    
    vencedor = 'A' if pts_a > pts_b else ('B' if pts_b > pts_a else 'Empate')
    
    return {
        'pts_a': pts_a,
        'pts_b': pts_b,
        'mudancas': mudancas_lideranca,
        'ultima_virada': momento_ultima_virada,
        'diferenca_final': diferenca_final,
        'diferenca_media': diferenca_media,
        'vencedor': vencedor,
        'historico_diferencas': historico_diferencas
    }


def analisar_multiplos_jogos(num_lancamentos, num_simulacoes):
    """
    Executa múltiplas simulações para análise estatística.
    """
    print(f"\n=== Simulando {num_simulacoes} jogos com {num_lancamentos} lançamentos cada ===\n")
    
    todas_mudancas = []
    todos_momentos_ultima_virada = []
    todas_diferencas_finais = []
    todas_diferencas_medias = []
    jogos_com_mudanca = 0
    
    for _ in range(num_simulacoes):
        resultado = simular_jogo(num_lancamentos, mostrar_detalhes=False)
        
        todas_mudancas.append(resultado['mudancas'])
        
        if resultado['mudancas'] > 0:
            jogos_com_mudanca += 1
            todos_momentos_ultima_virada.append(resultado['ultima_virada'])
        
        todas_diferencas_finais.append(resultado['diferenca_final'])
        todas_diferencas_medias.append(resultado['diferenca_media'])
    
    # PERGUNTA 1: Frequência de mudanças de liderança
    print("=" * 70)
    print("PERGUNTA 1: Com que frequência a liderança muda de mãos?")
    print("=" * 70)
    mudancas_media = sum(todas_mudancas) / len(todas_mudancas)
    print(f"Número médio de mudanças de liderança: {mudancas_media:.2f}")
    print(f"Mudanças mínimas: {min(todas_mudancas)}")
    print(f"Mudanças máximas: {max(todas_mudancas)}")
    print(f"Jogos com pelo menos 1 mudança: {jogos_com_mudanca} ({(jogos_com_mudanca/num_simulacoes)*100:.1f}%)")
    print(f"Porcentagem em relação ao total de lançamentos: {(mudancas_media/num_lancamentos)*100:.2f}%")
    
    # Distribuição de mudanças
    contador_mudancas = Counter(todas_mudancas)
    print(f"\nDistribuição de mudanças:")
    for num_mudancas, freq in sorted(contador_mudancas.items())[:15]:
        print(f"  {num_mudancas} mudanças: {freq} jogos ({(freq/num_simulacoes)*100:.1f}%)")
    
    # PERGUNTA 2: Momento da última virada
    print("\n" + "=" * 70)
    print("PERGUNTA 2: Quando ocorre a última mudança de liderança?")
    print("=" * 70)
    if todos_momentos_ultima_virada:
        momento_medio = sum(todos_momentos_ultima_virada) / len(todos_momentos_ultima_virada)
        print(f"Momento médio da última virada: rodada {momento_medio:.2f}")
        print(f"Percentual do jogo: {(momento_medio/num_lancamentos)*100:.2f}%")
        print(f"(Baseado em {len(todos_momentos_ultima_virada)} jogos que tiveram mudanças)")
        
        # Distribuição por quartis
        quartil_1 = sum(1 for m in todos_momentos_ultima_virada if m <= num_lancamentos * 0.25)
        quartil_2 = sum(1 for m in todos_momentos_ultima_virada if num_lancamentos * 0.25 < m <= num_lancamentos * 0.5)
        quartil_3 = sum(1 for m in todos_momentos_ultima_virada if num_lancamentos * 0.5 < m <= num_lancamentos * 0.75)
        quartil_4 = sum(1 for m in todos_momentos_ultima_virada if m > num_lancamentos * 0.75)
        
        total = len(todos_momentos_ultima_virada)
        print(f"\nDistribuição da última virada:")
        print(f"  Primeiro quarto (0-25%): {(quartil_1/total)*100:.1f}%")
        print(f"  Segundo quarto (25-50%): {(quartil_2/total)*100:.1f}%")
        print(f"  Terceiro quarto (50-75%): {(quartil_3/total)*100:.1f}%")
        print(f"  Último quarto (75-100%): {(quartil_4/total)*100:.1f}%")
    else:
        print("Nenhum jogo teve mudança de liderança!")
    
    # PERGUNTA 3: Margem de vitória
    print("\n" + "=" * 70)
    print("PERGUNTA 3: Por qual diferença um jogador tipicamente lidera?")
    print("=" * 70)
    diferenca_final_media = sum(todas_diferencas_finais) / len(todas_diferencas_finais)
    diferenca_durante_jogo_media = sum(todas_diferencas_medias) / len(todas_diferencas_medias)
    
    print(f"Diferença média FINAL: {diferenca_final_media:.2f} pontos")
    print(f"Diferença média DURANTE o jogo: {diferenca_durante_jogo_media:.2f} pontos")
    
    # Distribuição das diferenças finais
    contador_diferencas = Counter(todas_diferencas_finais)
    print(f"\nDistribuição das diferenças finais mais comuns:")
    for dif, freq in sorted(contador_diferencas.most_common(15)):
        print(f"  Diferença de {dif}: {freq} jogos ({(freq/num_simulacoes)*100:.1f}%)")


# Menu principal
print("=" * 70)
print("SIMULADOR DE CARA OU COROA - ANÁLISE ESTATÍSTICA")
print("=" * 70)

opcao = input("\nEscolha:\n1 - Simular um jogo individual\n2 - Análise estatística (múltiplas simulações)\nOpção: ")

if opcao == '1':
    num_lancamentos = int(input("Digite o número de lançamentos: "))
    resultado = simular_jogo(num_lancamentos, mostrar_detalhes=True)
    
    print("\n" + "=" * 70)
    print("RESULTADOS FINAIS")
    print("=" * 70)
    print(f"Pontos Jogador A (Cara): {resultado['pts_a']}")
    print(f"Pontos Jogador B (Coroa): {resultado['pts_b']}")
    print(f"Vencedor: Jogador {resultado['vencedor']}")
    print(f"Mudanças de liderança: {resultado['mudancas']}")
    if resultado['ultima_virada'] != -1:
        print(f"Última virada na rodada: {resultado['ultima_virada']}")
    else:
        print("Não houve mudanças de liderança")
    print(f"Diferença final: {resultado['diferenca_final']}")
    print(f"Diferença média durante o jogo: {resultado['diferenca_media']:.2f}")

elif opcao == '2':
    num_lancamentos = int(input("Digite o número de lançamentos por jogo: "))
    num_simulacoes = int(input("Digite o número de simulações: "))
    analisar_multiplos_jogos(num_lancamentos, num_simulacoes)