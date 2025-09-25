import random
import sys
import os
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
def header():
    print("-" * 56+"*POKER*"+"-"* 56,"\n")
def playername():
    print("Player:".rjust(110),nome)


valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
naipes = ['♠', '♣', '♥', '♦']
valor_carta = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
baralho = [valor + naipe for valor in valores for naipe in naipes]

limpar_tela()
header()
nome = input("Write your name: ")

while True:

    limpar_tela()
    header()
    playername()

    print("\n\n\n1. Start\n2. How to Play\n3. Exit")

    try:
        start = int(input("\n\nChoose your option: "))
    except ValueError:
        limpar_tela()
        header()
        playername()
        print("\n\nWrong option! Only write numbers (1, 2 or 3).")
        input("\n\nPress ENTER to go back to menu")
        continue

    if start == 3:
        limpar_tela()
        sys.exit()

    elif start == 2:
        limpar_tela()
        header()
        print("\nSoon")
        input("\n\nPress ENTER to go back to menu")

    elif start == 1:
        random.shuffle(baralho)
        mao_jogador = [baralho.pop(), baralho.pop()]
        mao_ia = [baralho.pop(), baralho.pop()]
        mesa = [baralho.pop() for _ in range(5)]

        print("Mão do Oponente: [?] [?]"),print("Sua mão:", mao_jogador)
        print(mesa[:3])
        print(mesa[:4])
        print(mesa[:5])

        input("\nYou Lose! Press ENTER to go back to menu :(")