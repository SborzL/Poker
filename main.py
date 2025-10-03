import random
import sys
import os
import itertools

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
def cabecalho():
    print('-' * 56 +'*POKER*'+'-'* 56,'\n')
def nomejogador():
    print('Player:'.rjust(110),nome)
def avaliar_mao(cartas):
    valores_cartas = sorted([valor_carta[c[:-1]] for c in cartas], reverse=True)
    naipes = [c[-1] for c in cartas]
    contagem = {v: valores_cartas.count(v) for v in set(valores_cartas)}
    ordenados = sorted(contagem.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # Flush
    flush = None
    for n in naipes:
        if naipes.count(n) >= 5:
            flush = n

    # Straight
    valores_unicos = sorted(set(valores_cartas), reverse=True)
    straight = None
    for i in range(len(valores_unicos) - 4):
        seq = valores_unicos[i:i+5]
        if seq[0] - seq[4] == 4:
            straight = seq
            break
    if set([14, 5, 4, 3, 2]).issubset(valores_unicos):
        straight = [5, 4, 3, 2, 1]

    # Royal / Straight Flush
    if flush and straight:
        flush_vals = [valor_carta[c[:-1]] for c in cartas if c[-1] == flush]
        flush_unicos = sorted(set(flush_vals), reverse=True)
        for i in range(len(flush_unicos) - 4):
            seq = flush_unicos[i:i+5]
            if seq[0] - seq[4] == 4:
                if seq[0] == 14:
                    return (10, seq, "Royal Flush")
                return (9, seq, "Straight Flush")

    # Quadra
    if 4 in contagem.values():
        quadra = [v for v, c in contagem.items() if c == 4][0]
        kicker = max(v for v in valores_cartas if v != quadra)
        return (8, [quadra, kicker], "Quadra")

    # Full House
    if 3 in contagem.values() and 2 in contagem.values():
        trinca = max(v for v, c in contagem.items() if c == 3)
        par = max(v for v, c in contagem.items() if c == 2)
        return (7, [trinca, par], "Full House")

    # Flush
    if flush:
        flush_vals = [valor_carta[c[:-1]] for c in cartas if c[-1] == flush]
        return (6, sorted(flush_vals, reverse=True)[:5])

    # Straight
    if straight:
        return (5, straight, "Straight")

    # Trinca
    if 3 in contagem.values():
        trinca = max(v for v, c in contagem.items() if c == 3)
        kickers = sorted([v for v in valores_cartas if v != trinca], reverse=True)[:2]
        return (4, [trinca] + kickers, "Trinca")

    # Dois Pares
    pares = [v for v, c in contagem.items() if c == 2]
    if len(pares) >= 2:
        pares = sorted(pares, reverse=True)[:2]
        kicker = max(v for v in valores_cartas if v not in pares)
        return (3, pares + [kicker], "Dois Pares")

    # Um Par
    if 2 in contagem.values():
        par = max(v for v, c in contagem.items() if c == 2)
        kickers = sorted([v for v in valores_cartas if v != par], reverse=True)[:3]
        return (2, [par] + kickers, "Par")


    return (1, valores_cartas[:5], "Carta Alta")



valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
naipes = ['♠', '♣', '♥', '♦']
valor_carta = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
               '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
nomes_maos = {
    10: "Royal Flush",
    9: "Straight Flush",
    8: "Quadra",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Trinca",
    3: "Dois Pares",
    2: "Um Par",
    1: "Carta Alta"}

limpar_tela()
cabecalho()
nome = input('Escreva seu nome: ')

while True:
    limpar_tela()
    cabecalho()
    nomejogador()
    print('\n\n\n1. Iniciar\n2. Como Jogar\n3. Sair')
    try:
        start = int(input('\n\nEscolha uma opção: '))
    except ValueError:
        limpar_tela()
        cabecalho()
        nomejogador()
        print('\n\nOpção incorreta! Escolha um número (1, 2 ou 3).')
        input('\n\nPressione ENTER para voltar para o menu')
        continue

    if start == 3:
        limpar_tela()
        sys.exit()

    elif start == 2:
        limpar_tela()
        cabecalho()
        nomejogador()
        print('\nEm breve')
        input('\n\nPressione ENTER para voltar para o menu')

    elif start == 1:
        limpar_tela()
        cabecalho()
        nomejogador()
        baralho = [valor + naipe for valor in valores for naipe in naipes]
        random.shuffle(baralho)

    mao_jogador = [baralho.pop(), baralho.pop()]
    mao_ia = [baralho.pop(), baralho.pop()]
    mesa = []

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    limpar_tela()
    cabecalho()
    nomejogador()
    mesa.extend([baralho.pop(), baralho.pop(), baralho.pop()])
    print('Mesa:', ' '.join(mesa))

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    limpar_tela()
    cabecalho()
    nomejogador()
    mesa.append(baralho.pop())
    print('Mesa:', ' '.join(mesa))

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    limpar_tela()
    cabecalho()
    nomejogador()
    mesa.append(baralho.pop())
    print('Mesa:', ' '.join(mesa))


    cartas_jogador = mao_jogador + mesa

    cartas_ia = mao_ia + mesa

    melhor_jogador = max([avaliar_mao(c) for c in itertools.combinations(cartas_jogador, 5)])
    melhor_ia = max([avaliar_mao(c) for c in itertools.combinations(cartas_ia, 5)])

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    limpar_tela()
    cabecalho()
    nomejogador()
    print('Mesa:', ' '.join(mesa))


    print(f'\nMão do CPU: {mao_ia[0]} {mao_ia[1]}')

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')


    input('\nPressione ENTER')

    if melhor_jogador[0] > melhor_ia[0] or (melhor_jogador[0] == melhor_ia[0] and melhor_jogador[1] > melhor_ia[1]):
        print(f'\n\n🔥 Você GANHOU com {melhor_jogador[2]}! 🔥')
    elif melhor_jogador[0] < melhor_ia[0] or (melhor_jogador[0] == melhor_ia[0] and melhor_jogador[1] < melhor_ia[1]):
        print(f'\n\n💀 Você PERDEU! O CPU fez {melhor_ia[2]} 💀')
    else:
        print(f'\n\n😐 Empate com {melhor_jogador[2]}! 😐')

    input('\nPressione ENTER para voltar ao menu...')
