import random
import sys
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
naipes = ['♠', '♣', '♥', '♦']
valor_carta = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
baralho = [valor + naipe for valor in valores for naipe in naipes]

print("---------------------------------------------------------- Poker ----------------------------------------------------------\n\n")

nome = input("Digite seu nome: ")
limpar_tela()
print("Name:".rjust(60),nome)

print("\n\n\n1. Start\n"
      "2. How to Play\n"
      "3. Exit")

start = int(input("\n\n Choose your option: "))

if start == 3:
    sys.exit()

elif start == 2:
   print("Soon")

elif start == 1:
    random.shuffle(baralho)
    mao_jogador = [baralho.pop(), baralho.pop()]
    mao_ia = [baralho.pop(), baralho.pop()]
    mesa = [baralho.pop() for _ in range(5)]

    print("Mão do Oponente: [?] [?]"),print("Sua mão:", mao_jogador)
    print(mesa[:3])
    print(mesa[:4])
    print(mesa[:5])
