import pygame, sys, random
from collections import Counter

pygame.init()

tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Poker 2D")

fonte = pygame.font.Font(None, 60)
fonte_media = pygame.font.Font(None, 40)
fonte_pequena = pygame.font.Font(None, 30)

estado = "nome"
entrada_texto = ""
nome_jogador = ""

VALORES = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
NAIPES = ["ouros", "paus", "copas", "espadas"]

def carregar_cartas_spritesheet(caminho):
    largura_carta = 71
    altura_carta = 97
    spritesheet = pygame.image.load(caminho).convert_alpha()
    cartas = {}
    for linha, naipe in enumerate(NAIPES):
        for coluna, valor in enumerate(VALORES):
            x = coluna * largura_carta
            y = linha * altura_carta
            carta = spritesheet.subsurface((x, y, largura_carta, altura_carta))
            cartas[f"{valor}_{naipe}"] = carta
    return cartas

cartas = carregar_cartas_spritesheet("assets/cartas.png")

def desenhar_botao(texto, y_offset, cor_normal, cor_hover):
    largura_botao, altura_botao = 320, 70
    x = tela.get_width()//2 - largura_botao//2
    y = tela.get_height()//2 + y_offset
    rect = pygame.Rect(x, y, largura_botao, altura_botao)

    mouse = pygame.mouse.get_pos()
    cor = cor_normal if not rect.collidepoint(mouse) else cor_hover

    pygame.draw.rect(tela, cor, rect, border_radius=10)
    txt = fonte_media.render(texto, True, (255,255,255))
    tela.blit(txt, (x + (largura_botao - txt.get_width())//2,
                    y + (altura_botao - txt.get_height())//2))
    return rect

def desenhar_botao_x():
    largura, altura = 50, 50
    x = tela.get_width() - largura - 10
    y = 10
    rect = pygame.Rect(x, y, largura, altura)

    mouse = pygame.mouse.get_pos()
    cor = (150,0,0) if not rect.collidepoint(mouse) else (200,0,0)

    pygame.draw.rect(tela, cor, rect, border_radius=8)
    txt = fonte.render("X", True, (255,255,255))
    tela.blit(txt, (x + (largura - txt.get_width())//2,
                    y + (altura - txt.get_height())//2))
    return rect

def desenhar_nome_canto():
    if nome_jogador:
        txt = fonte_pequena.render(f"Jogador: {nome_jogador}", True, (255,255,255))
        tela.blit(txt, (20, 20))


VALOR_ORDEM = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14
}

def criar_baralho():
    baralho = [f"{v}_{n}" for v in VALORES for n in NAIPES]
    random.shuffle(baralho)
    return baralho

def dar(baralho, n):
    return [baralho.pop() for _ in range(n)]

def parse_carta(c):
    v, n = c.split("_")
    return v, n

def ranks_e_naipes(cartas_lista):
    ranks = []
    naipes = []
    for c in cartas_lista:
        v, n = parse_carta(c)
        ranks.append(VALOR_ORDEM[v])
        naipes.append(n)
    return ranks, naipes

def encontrar_straight(ranks):
    uniq = sorted(set(ranks))
    if 14 in uniq:
        uniq = [1] + uniq  # A baixo
    run = 1
    best_high = None
    for i in range(1, len(uniq)):
        if uniq[i] == uniq[i-1] + 1:
            run += 1
            if run >= 5:
                best_high = uniq[i]
        else:
            run = 1
    return best_high

def avaliar_mao7(cartas7):
    ranks, naipes = ranks_e_naipes(cartas7)
    cont_rank = Counter(ranks)
    cont_naipe = Counter(naipes)

    # Flush
    flush_naipe = next((n for n, cnt in cont_naipe.items() if cnt >= 5), None)
    flush_cards = []
    if flush_naipe:
        flush_cards = sorted([VALOR_ORDEM[parse_carta(c)[0]]
                              for c in cartas7 if parse_carta(c)[1] == flush_naipe], reverse=True)

    # Straight
    straight_high = encontrar_straight(ranks)

    # Straight Flush
    if flush_naipe:
        ranks_flush = [VALOR_ORDEM[parse_carta(c)[0]]
                       for c in cartas7 if parse_carta(c)[1] == flush_naipe]
        sf_high = encontrar_straight(ranks_flush)
        if sf_high:
            return (8, [sf_high])

    # Quadra
    quad = [r for r, cnt in cont_rank.items() if cnt == 4]
    if quad:
        quad_rank = max(quad)
        kicker = max([r for r in ranks if r != quad_rank])
        return (7, [quad_rank, kicker])

    # Full House
    trips = sorted([r for r, cnt in cont_rank.items() if cnt == 3], reverse=True)
    pares = sorted([r for r, cnt in cont_rank.items() if cnt == 2], reverse=True)
    if trips and (pares or len(trips) >= 2):
        trip_rank = trips[0]
        pair_rank = trips[1] if len(trips) >= 2 else pares[0]
        return (6, [trip_rank, pair_rank])

    # Flush
    if flush_naipe:
        return (5, flush_cards[:5])

    # Sequência
    if straight_high:
        return (4, [straight_high])

    # Trinca
    if trips:
        trip_rank = trips[0]
        kickers = sorted([r for r in ranks if r != trip_rank], reverse=True)[:2]
        return (3, [trip_rank] + kickers)

    # Dois Pares
    if len(pares) >= 2:
        p1, p2 = pares[0], pares[1]
        kicker = max([r for r in ranks if r not in (p1, p2)])
        return (2, [p1, p2, kicker])

    # Um Par
    if len(pares) == 1:
        p = pares[0]
        kickers = sorted([r for r in ranks if r != p], reverse=True)[:3]
        return (1, [p] + kickers)

    # Carta Alta
    top5 = sorted(ranks, reverse=True)[:5]
    return (0, top5)

def comparar_maos(jogador7, ia7):
    rj = avaliar_mao7(jogador7)
    ri = avaliar_mao7(ia7)
    if rj[0] > ri[0]:
        return 1, rj, ri
    elif rj[0] < ri[0]:
        return -1, rj, ri
    else:
        if rj[1] > ri[1]:
            return 1, rj, ri
        elif rj[1] < ri[1]:
            return -1, rj, ri
        else:
            return 0, rj, ri

def nome_mao(rank_tuple):
    nomes = {
        8: "Sequência de mesmo naipe",
        7: "Quadra",
        6: "Full House",
        5: "Cor (Flush)",
        4: "Sequência",
        3: "Trinca",
        2: "Dois Pares",
        1: "Um Par",
        0: "Carta Alta"
    }
    return nomes[rank_tuple[0]]

baralho = []
jogador = []
ia = []
comunitarias = []
rodada = "preflop"  # preflop, flop, turn, river, resultado

def nova_partida():
    global baralho, jogador, ia, comunitarias, rodada
    baralho = criar_baralho()
    jogador = dar(baralho, 2)
    ia = dar(baralho, 2)
    comunitarias = []
    rodada = "preflop"

def avancar_rodada():
    global rodada, comunitarias
    if rodada == "preflop":
        comunitarias = dar(baralho, 3)
        rodada = "flop"
    elif rodada == "flop":
        comunitarias.append(dar(baralho, 1)[0])
        rodada = "turn"
    elif rodada == "turn":
        comunitarias.append(dar(baralho, 1)[0])
        rodada = "river"
    elif rodada == "river":
        rodada = "resultado"

# Inicializa partida
nova_partida()

# -------------------------------------------------------
# Retângulos dos botões por tela (atualizados a cada frame)
# -------------------------------------------------------
rects_nome = {}
rects_menu = {}
rects_mesa = {}
rects_como = {}
rects_cartas = {}
rects_confirmacao = {}

# -------------------------------------------------------
# Telas
# -------------------------------------------------------
def desenhar_nome():
    tela.fill((0,0,50))
    titulo = fonte.render("Digite seu nome:", True, (255,255,255))
    tela.blit(titulo, (tela.get_width()//2 - titulo.get_width()//2, 200))

    # Caixa de texto
    caixa = pygame.Rect(tela.get_width()//2 - 250, 300, 500, 60)
    pygame.draw.rect(tela, (255,255,255), caixa, 2)
    texto = fonte_media.render(entrada_texto, True, (255,255,255))
    # Cortar texto se passar da caixa
    if texto.get_width() > caixa.width - 20:
        # Reduzir visualmente: mostrar final do texto
        corte = entrada_texto[-30:]
        texto = fonte_media.render(corte, True, (255,255,255))
    tela.blit(texto, (caixa.x+10, caixa.y+10))

    # Dica
    dica = fonte_pequena.render("Pressione Enter para confirmar.", True, (200,200,200))
    tela.blit(dica, (tela.get_width()//2 - dica.get_width()//2, 380))

    # Botão confirmar
    rects_nome.clear()
    rects_nome["confirmar"] = desenhar_botao("Confirmar", 150, (0,100,0), (0,150,0))
    return "nome"

def desenhar_menu():
    tela.fill((0,0,0))
    desenhar_nome_canto()
    titulo = fonte.render("POKER 2D", True, (255,255,255))
    subtitulo = fonte_pequena.render("Texas Hold'em — Versão demonstrativa", True, (180,180,180))
    tela.blit(titulo, (tela.get_width()//2 - titulo.get_width()//2,
                       tela.get_height()//2 - 220))
    tela.blit(subtitulo, (tela.get_width()//2 - subtitulo.get_width()//2,
                          tela.get_height()//2 - 170))

    rects_menu["jogar"] = desenhar_botao("Jogar", -60, (0,100,0), (0,150,0))
    rects_menu["como"] = desenhar_botao("Como jogar", 30, (0,100,0), (0,150,0))
    rects_menu["cartas"] = desenhar_botao("Ver cartas", 120, (0,100,0), (0,150,0))
    rects_menu["sair"] = desenhar_botao("Sair", 210, (100,0,0), (150,0,0))
    return "menu"

def desenhar_mesa():
    tela.fill((0,128,0))
    desenhar_nome_canto()
    titulo = fonte.render("Mesa de Pôquer", True, (255,255,255))
    tela.blit(titulo, (tela.get_width()//2 - titulo.get_width()//2, 40))

    W, H = tela.get_width(), tela.get_height()
    card_w, card_h = 80, 120
    espac = 20

    # Cartas comunitárias
    tot_w = 5*card_w + 4*espac
    start_x = W//2 - tot_w//2
    y_middle = H//2 - card_h//2
    for i, c in enumerate(comunitarias):
        carta_img = pygame.transform.scale(cartas[c], (card_w, card_h))
        tela.blit(carta_img, (start_x + i*(card_w+espac), y_middle))

    # Cartas do jogador (embaixo)
    tot_w_j = 2*card_w + espac
    start_x_j = W//2 - tot_w_j//2
    y_player = H - card_h - 80
    for i, c in enumerate(jogador):
        carta_img = pygame.transform.scale(cartas[c], (card_w, card_h))
        tela.blit(carta_img, (start_x_j + i*(card_w+espac), y_player))

    # Cartas do computador (em cima)
    tot_w_i = 2*card_w + espac
    start_x_i = W//2 - tot_w_i//2
    y_ai = 120
    for i, c in enumerate(ia):
        carta_img = pygame.transform.scale(cartas[c], (card_w, card_h))
        tela.blit(carta_img, (start_x_i + i*(card_w+espac), y_ai))

    # Fase atual
    fase_txt = fonte_pequena.render(f"Rodada: {rodada.upper()}", True, (255,255,255))
    tela.blit(fase_txt, (W//2 - fase_txt.get_width()//2, y_middle - 50))

    # Resultado (após river)
    if rodada == "resultado":
        resultado, rj, ri = comparar_maos(jogador + comunitarias, ia + comunitarias)
        nome_j = nome_mao(rj)
        nome_i = nome_mao(ri)

        msg_j = fonte_pequena.render(f"{nome_jogador}: {nome_j}", True, (255,255,255))
        msg_i = fonte_pequena.render(f"Computador: {nome_i}", True, (255,255,255))
        tela.blit(msg_j, (W//2 - msg_j.get_width()//2, y_player - 40))
        tela.blit(msg_i, (W//2 - msg_i.get_width()//2, y_ai + card_h + 10))

        if resultado == 1:
            vencedor_txt = f"{nome_jogador} vence!"
        elif resultado == -1:
            vencedor_txt = "Computador vence!"
        else:
            vencedor_txt = "Empate!"
        vencedor = fonte.render(vencedor_txt, True, (255,255,255))
        tela.blit(vencedor, (W//2 - vencedor.get_width()//2, y_middle + card_h + 30))

    # Botões de ação
    rects_mesa.clear()
    if rodada == "resultado":
        rects_mesa["acao"] = desenhar_botao("Nova partida", 220, (0,100,0), (0,150,0))
    else:
        rects_mesa["acao"] = desenhar_botao("Próxima rodada", 220, (0,100,0), (0,150,0))
    rects_mesa["fechar"] = desenhar_botao_x()
    return "mesa"

def desenhar_como_jogar():
    tela.fill((30,30,30))
    desenhar_nome_canto()
    titulo = fonte.render("Como jogar — Hierarquia das mãos", True, (255,255,255))
    tela.blit(titulo, (tela.get_width()//2 - titulo.get_width()//2, 30))

    hierarquia = [
        ("Royal Flush", "A, K, Q, J, 10 do mesmo naipe. Imbatível.",
         ["A_espadas","K_espadas","Q_espadas","J_espadas","10_espadas"]),
        ("Sequência de mesmo naipe", "Cinco cartas consecutivas do mesmo naipe.",
         ["5_copas","6_copas","7_copas","8_copas","9_copas"]),
        ("Quadra", "Quatro cartas do mesmo valor.",
         ["9_ouros","9_paus","9_copas","9_espadas"]),
        ("Full House", "Trinca + Par (ex.: Q-Q-Q e 2-2).",
         ["Q_ouros","Q_paus","Q_copas","2_espadas","2_copas"]),
        ("Cor (Flush)", "Cinco cartas do mesmo naipe, não consecutivas.",
         ["2_paus","5_paus","9_paus","J_paus","K_paus"]),
        ("Sequência", "Cinco cartas consecutivas (naipes variados).",
         ["4_ouros","5_paus","6_copas","7_espadas","8_ouros"]),
        ("Trinca", "Três cartas do mesmo valor.",
         ["7_ouros","7_paus","7_copas"]),
        ("Dois Pares", "Dois pares diferentes.",
         ["8_ouros","8_copas","K_paus","K_espadas"]),
        ("Um Par", "Duas cartas do mesmo valor.",
         ["5_ouros","5_copas"]),
        ("Carta Alta", "Nenhuma combinação; vale a carta mais alta.",
         ["A_ouros"])
    ]

    rects_como.clear()
    rects_como["fechar"] = desenhar_botao_x()

    linha_altura = 95
    y_base = 110
    for i, (nome, explicacao, exemplo) in enumerate(hierarquia):
        linha_rect = pygame.Rect(60, y_base + i*linha_altura - 10, tela.get_width()-120, linha_altura-10)
        pygame.draw.rect(tela, (45,45,45), linha_rect, border_radius=8)

        # Cartas à esquerda
        x_cartas = 90
        for j, chave in enumerate(exemplo):
            if chave in cartas:
                carta = pygame.transform.scale(cartas[chave], (50,70))
                tela.blit(carta, (x_cartas + j*55, y_base + i*linha_altura))

        # Texto ao lado das cartas
        texto = fonte_pequena.render(f"{i+1}. {nome} — {explicacao}", True, (230,230,230))
        x_texto = x_cartas + len(exemplo)*55 + 30
        tela.blit(texto, (x_texto, y_base + i*linha_altura + 20))

    # Rodapé com crédito
    credito = fonte_pequena.render(
        'Pixel art poker cards: Vircon32 (Carra) — CC-BY 4.0 (OpenGameArt)',
        True, (180,180,180)
    )
    tela.blit(credito, (tela.get_width()//2 - credito.get_width()//2, tela.get_height() - 40))
    return "como_jogar"

def desenhar_cartas():
    tela.fill((20,20,20))
    desenhar_nome_canto()
    largura_carta = 71
    altura_carta = 97
    espacamento = 10

    total_largura = len(VALORES) * largura_carta + (len(VALORES)-1)*espacamento
    total_altura = len(NAIPES) * altura_carta + (len(NAIPES)-1)*espacamento

    margem_x = (tela.get_width() - total_largura)//2
    margem_y = (tela.get_height() - total_altura)//2

    for linha, naipe in enumerate(NAIPES):
        for coluna, valor in enumerate(VALORES):
            chave = f"{valor}_{naipe}"
            x = margem_x + coluna*(largura_carta+espacamento)
            y = margem_y + linha*(altura_carta+espacamento)
            tela.blit(cartas[chave], (x,y))

    aviso = fonte_pequena.render(
        'Pixel art poker cards por Vircon32 (Carra), CC-BY 4.0',
        True, (200,200,200))
    tela.blit(aviso, (tela.get_width()//2 - aviso.get_width()//2,
                      tela.get_height()-40))

    rects_cartas.clear()
    rects_cartas["fechar"] = desenhar_botao_x()
    return "cartas"

def desenhar_confirmacao():
    tela.fill((0,0,0))
    desenhar_nome_canto()
    texto = fonte.render("Deseja voltar ao menu?", True, (255,255,255))
    tela.blit(texto, (tela.get_width()//2 - texto.get_width()//2, tela.get_height()//2 - 120))
    info = fonte_pequena.render("Você está no meio de uma partida.", True, (200,200,200))
    tela.blit(info, (tela.get_width()//2 - info.get_width()//2, tela.get_height()//2 - 70))

    rects_confirmacao.clear()
    rects_confirmacao["sim"] = desenhar_botao("Sim", 0, (0,100,0), (0,150,0))
    rects_confirmacao["nao"] = desenhar_botao("Não", 100, (100,0,0), (150,0,0))
    return "confirmacao"

# -------------------------------------------------------
# Loop principal
# -------------------------------------------------------
rodando = True
while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

        # Entrada de texto na tela de nome
        if estado == "nome":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if entrada_texto.strip():
                        nome_jogador = entrada_texto.strip()
                        estado = "menu"
                elif evento.key == pygame.K_BACKSPACE:
                    entrada_texto = entrada_texto[:-1]
                else:
                    # Adiciona caracteres imprimíveis
                    if len(evento.unicode) == 1 and not evento.unicode.isspace():
                        entrada_texto += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rects_nome.get("confirmar") and rects_nome["confirmar"].collidepoint(evento.pos):
                    if entrada_texto.strip():
                        nome_jogador = entrada_texto.strip()
                        estado = "menu"

        # Cliques nas demais telas
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado == "menu":
                if rects_menu.get("jogar") and rects_menu["jogar"].collidepoint(evento.pos):
                    nova_partida()
                    estado = "mesa"
                elif rects_menu.get("como") and rects_menu["como"].collidepoint(evento.pos):
                    estado = "como_jogar"
                elif rects_menu.get("cartas") and rects_menu["cartas"].collidepoint(evento.pos):
                    estado = "cartas"
                elif rects_menu.get("sair") and rects_menu["sair"].collidepoint(evento.pos):
                    rodando = False

            elif estado == "mesa":
                if rects_mesa.get("acao") and rects_mesa["acao"].collidepoint(evento.pos):
                    if rodada == "resultado":
                        nova_partida()
                    else:
                        avancar_rodada()
                if rects_mesa.get("fechar") and rects_mesa["fechar"].collidepoint(evento.pos):
                    estado = "confirmacao"

            elif estado == "como_jogar":
                if rects_como.get("fechar") and rects_como["fechar"].collidepoint(evento.pos):
                    estado = "menu"

            elif estado == "cartas":
                if rects_cartas.get("fechar") and rects_cartas["fechar"].collidepoint(evento.pos):
                    estado = "menu"

            elif estado == "confirmacao":
                if rects_confirmacao.get("sim") and rects_confirmacao["sim"].collidepoint(evento.pos):
                    estado = "menu"
                elif rects_confirmacao.get("nao") and rects_confirmacao["nao"].collidepoint(evento.pos):
                    estado = "mesa"

    # Desenhar tela atual
    if estado == "nome":
        desenhar_nome()
    elif estado == "menu":
        desenhar_menu()
    elif estado == "mesa":
        desenhar_mesa()
    elif estado == "como_jogar":
        desenhar_como_jogar()
    elif estado == "cartas":
        desenhar_cartas()
    elif estado == "confirmacao":
        desenhar_confirmacao()

    pygame.display.flip()

pygame.quit()
sys.exit()
