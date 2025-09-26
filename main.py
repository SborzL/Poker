import random
import sys
import os
import itertools

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def header():
    print('-' * 56 +'*POKER*'+'-'* 56,'\n')
def playername():
    print('Player:'.rjust(110),nome)
def avaliar_mao(cartas):
    valores_cartas = sorted([valor_carta[c[:-1]] for c in cartas], reverse=True)
    naipes = [c[-1] for c in cartas]
    contagem = {v: valores_cartas.count(v) for v in valores_cartas}
    pares = list(contagem.values())
    flush = any(naipes.count(n) >= 5 for n in naipes)
    valores_unicos = sorted(set(valores_cartas), reverse=True)
    straight = False
    for i in range(len(valores_unicos) - 4):
        if valores_unicos[i] - valores_unicos[i+4] == 4:
            straight = True
    if straight and flush and max(valores_unicos) == 14:
        return (10, valores_cartas)  # Royal Flush
    if straight and flush:
        return (9, valores_cartas)   # Straight Flush
    if 4 in pares:
        return (8, valores_cartas)   # Four of a Kind
    if 3 in pares and 2 in pares:
        return (7, valores_cartas)   # Full House
    if flush:
        return (6, valores_cartas)   # Flush
    if straight:
        return (5, valores_cartas)   # Straight
    if 3 in pares:
        return (4, valores_cartas)   # Three of a Kind
    if pares.count(2) >= 2:
        return (3, valores_cartas)   # Two Pair
    if 2 in pares:
        return (2, valores_cartas)   # One Pair
    return (1, valores_cartas)

valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
naipes = ['♠', '♣', '♥', '♦']
valor_carta = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
               '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

clear()
header()
nome = input('Escreva seu nome: ')

while True:
    clear()
    header()
    playername()
    print('\n\n\n1. Iniciar\n2. Como Jogar\n3. Sair')
    try:
        start = int(input('\n\nEscolha uma opção: '))
    except ValueError:
        clear()
        header()
        playername()
        print('\n\nOpção incorreta! Escolha um número (1, 2 ou 3).')
        input('\n\nPressione ENTER para voltar para o menu')
        continue

    if start == 3:
        clear()
        sys.exit()

    elif start == 2:
        clear()
        header()
        playername()
        print('\nEm breve')
        input('\n\nPressione ENTER para voltar para o menu')

    elif start == 1:
        clear()
        header()
        playername()
        baralho = [valor + naipe for valor in valores for naipe in naipes]
        random.shuffle(baralho)

    mao_jogador = [baralho.pop(), baralho.pop()]
    mao_ia = [baralho.pop(), baralho.pop()]
    mesa = []

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    clear()
    header()
    playername()
    mesa.extend([baralho.pop(), baralho.pop(), baralho.pop()])
    print('Mesa:', ' '.join(mesa))

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    clear()
    header()
    playername()
    mesa.append(baralho.pop())
    print('Mesa:', ' '.join(mesa))

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')
    clear()
    header()
    playername()
    mesa.append(baralho.pop())
    print('Mesa:', ' '.join(mesa))


    cartas_jogador = mao_jogador + mesa

    cartas_ia = mao_ia + mesa

    melhor_jogador = max([avaliar_mao(c) for c in itertools.combinations(cartas_jogador, 5)])
    melhor_ia = max([avaliar_mao(c) for c in itertools.combinations(cartas_ia, 5)])

    print(f'\nMão do CPU: {mao_ia[0]} {mao_ia[1]}')

    print(f'\nSuas cartas: {mao_jogador[0]} {mao_jogador[1]}')

    input('\nPressione ENTER')

    if melhor_jogador > melhor_ia:
        print('\n\n🔥 Você GANHOU! 🔥')
    elif melhor_jogador < melhor_ia:
        print('\n\n💀 Você PERDEU! 💀')
    else:
        print('\n\n😐 Empate! 😐')

    input('\nPressione ENTER para voltar ao menu...')
