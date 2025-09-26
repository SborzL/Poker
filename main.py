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
    valores_cartas = sorted([valores[c[:-1]] for c in cartas], reverse=True)
    naipes = [c[-1] for c in cartas]
    if len(set(valores_cartas)) == 4:
        return (2, valores_cartas)
    elif len(set(valores_cartas)) == 3:
        return (3, valores_cartas)
    elif len(set(valores_cartas)) == 2:
        return (7, valores_cartas)
    else:
        return (1, valores_cartas)

valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
naipes = ['♠', '♣', '♥', '♦']
valor_carta = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

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
        carta_mesa = [baralho.pop() for _ in range(5)]


        print(f'{carta_mesa[0]} {carta_mesa[1]} {carta_mesa[2]}'.rjust(46))
        print(f'{carta_mesa[0]} {carta_mesa[1]} {carta_mesa[2]} {carta_mesa[3]}'.rjust(48))
        print(f'{carta_mesa[0]} {carta_mesa[1]} {carta_mesa[2]} {carta_mesa[3]} {carta_mesa[4]}'.rjust(50))

        input('\nVocê Perdeu! Pressione ENTER para voltar para o menu :(')