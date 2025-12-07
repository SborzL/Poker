# Poker em Python ♠♥♦♣

## 📌 Sobre o Projeto
Este projeto é uma implementação simples de um jogo de **Poker (Texas Hold'em simplificado)** usando **Python + Pygame** com interface 2D.  
O objetivo foi aprender programação e lógica do jogo enquanto construía uma versão jogável com cartas gráficas.

Durante o desenvolvimento:
- Aprendi a trabalhar com loops, condições, tratamento de eventos e funções em Python.
- Implementei a lógica básica de avaliação de mãos de poker.
- Usei spritesheets para renderizar cartas e uma imagem separada para o verso das cartas.
- Recebi ajuda da IA em partes mais complexas da avaliação de mãos.

---

## 🚀 Funcionalidades
- Menu inicial com opções: **Jogar**, **Como jogar**, **Ver cartas** e **Sair**.
- Distribuição de cartas para o jogador e para a IA (2 cartas cada).
- Exibição das cartas comunitárias por etapas: **Flop**, **Turn**, **River**.
- Avaliação da melhor mão combinando suas 2 cartas com as 5 comunitárias.
- Determinação do vencedor ao final da rodada.
- Tela "Como jogar" com 3 seções (explicação, hierarquia com exemplos, visualização do baralho).
- Visualização do baralho completo e crédito ao autor das artes.

---

## 📖 Como Jogar (resumo)
1. Execute o programa.
2. Digite seu nome na tela inicial.
3. No menu, selecione **Jogar**.
4. Você recebe 2 cartas; a IA tem 2 cartas ocultas (verso) até o resultado.
5. Pressione o botão para avançar as fases:
   - Flop: 3 cartas comunitárias
   - Turn: +1 carta
   - River: +1 carta
6. Ao chegar em "resultado" as cartas da IA são reveladas e o vencedor é exibido.

---

## ▶️ Como executar
Requisitos:
- Python 3.8+  
- pygame

Instalação:
- pip install pygame

Estrutura mínima de assets:
- Colocar as imagens em `assets/`:
  - `assets/cartas.png` — spritesheet (13 colunas x 4 linhas)
  - `assets/verso.png` — verso da carta

Executar:
- `python main.py`

Dica: o jogo abre em fullscreen por padrão. Para rodar em janela, altere a criação da tela em `main.py`.


---

## ✍️ Relato da Experiência
Esse foi um projeto para aprender e praticar lógica de programação com Python, usando um tema que gosto (poker).  
Aprendi sobre organização de código, eventos do Pygame e como representar cartas graficamente.  
Precisei de ajuda em partes mais complexas da avaliação de mãos, o que fez parte do aprendizado e motivou a continuar melhorando.

---

## 🛠️ Planejo Implementar
- Sistema de apostas / fichas para cada jogador.
- Melhorias na interface (responsividade, animações simples).
- IA mais inteligente para decisões de jogo.
- Salvamento de estatísticas e múltiplas rodadas com histórico.

---

## Créditos e licença
- Cartas (pixel art): Vircon32 (Carra) — CC-BY 4.0 (OpenGameArt) — crédito exibido no rodapé do jogo.
- Verifique licenças dos assets antes de redistribuir.

---

## 🔗 Repositório
- https://github.com/SborzL555/Poker
