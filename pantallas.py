import pygame
negro = (0,0,0)
azul = (0,0,255)
blanco = (255, 255, 255)
amarillo = (255, 255, 0)
rosa = (255, 184, 255)
rojo = (255, 0, 0)
verde = (0, 128, 0)
violeta = (128, 0, 128)
gris = (128, 128, 128)

pacman_foto = pygame.image.load("pacman_abierto.png")
pacman_abierto = pygame.transform.scale(pacman_foto, (30, 30))

def pantalla_main(pantalla, ancho, tiempo, high_score):
    pantalla.fill(negro)
    fuente_titulo = pygame.font.SysFont("comicans", 60, bold = True)
    fuente_subtitulo = pygame.font.SysFont("trebuchetms", 20)
    fuente_score = pygame.font.SysFont("comicans", 24)
    texto_titulo = fuente_titulo.render("PAC-MAN", True, amarillo) 
    texto_instrucciones = fuente_subtitulo.render("presiona ENTER para comenzar", True, blanco)
    texto_high_score = fuente_score.render(f'HIGH SCORE: {high_score}', True, (255, 255, 255))

    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 250)) #centrar el texto
    pantalla.blit(texto_high_score, (ancho // 2 - texto_high_score.get_width() // 2, 80))
    if (tiempo // 500) % 2 == 0: #cada 500ms se cumple, ahí se imprime el texto 
        pantalla.blit (texto_instrucciones, (ancho // 2 - texto_instrucciones.get_width() // 2, 400))
    
def pantalla_fants(pantalla, fants_elegidos, opciones_fants, lista_colores, ind_selecc): 
    pantalla.fill (negro)
    fuente_elegir = pygame.font.SysFont("Courier New", 30, bold = True)
    fuente_fants = pygame.font.SysFont("Courier New", 25, bold = True)
    fuente_fants_d = pygame.font.SysFont("Courier New", 18, bold = True)
    texto_elegir = fuente_elegir.render (f"Elegí los fantasmas: {len(fants_elegidos)}/4", True, amarillo)
    pantalla.blit(texto_elegir, (100, 50))

    texto_inst = fuente_fants_d.render ("flechas para mover opcion -- elegir presione ENTER", True, gris)
    pantalla.blit(texto_inst, (20, 600))
    pos_x = 160
    pos_y = 120

    for i, opcion in enumerate (opciones_fants):
        fantasmas_text = fuente_fants.render (opcion, True, gris)
        descp_text = fuente_fants_d.render (opciones_fants[opcion], True, blanco)
        
        ancho_caja = max(fantasmas_text.get_width(), descp_text.get_width()) + 20 #en vez de usar .rect, como son varios textos, busco el rect de la suma de ambos
        alto_caja = fantasmas_text.get_height() + descp_text.get_height() + 20

        rect_grande = pygame.Rect(pos_x -15, pos_y - 5, ancho_caja, alto_caja)
        
        color_actual = lista_colores[i]
        pygame.draw.circle(pantalla, color_actual, (120, pos_y + 25), 20)

        if i == ind_selecc:
            color_borde = color_actual
            fantasmas_text = fuente_fants.render (opcion, True, amarillo)
            descp_text = fuente_fants_d.render (opciones_fants[opcion], True, amarillo)
        else: 
            color_borde = gris 

        if opcion in fants_elegidos: 
            pygame.draw.rect(pantalla, color_borde, rect_grande, 3)
        
        pantalla.blit(fantasmas_text, (pos_x, pos_y))
        pantalla.blit(descp_text, (pos_x, pos_y + fantasmas_text.get_height()+ 6))
        pos_y += alto_caja + 10 #dar un espacio entre las cajas de las opciones 

def pantalla_game(pantalla, puntaje):
    pantalla.fill(negro)
    fuente_game = pygame.font.SysFont("trebuchetms", 30, bold = True)
    fuente_descp = pygame.font.SysFont("trebuchetms", 20, bold = True)
    text_game = fuente_game.render("GAME OVER", True, rojo)
    text_descp = fuente_descp.render (f"Puntaje final: {puntaje}", True, gris)
    text_descp_1 = fuente_descp.render ("Presione ENTER para volver a la página de inicio", True, gris)
    pantalla.blit(text_game, (220, 250))
    pantalla.blit(text_descp, (240, 300))
    pantalla.blit(text_descp_1, (80, 350)) 

def margen_mapa(pantalla, score, nivel, high_score, vidas): 
    fuente_score = pygame.font.SysFont("comicans", 30, bold = True)
    text_score = fuente_score.render(f"score: {score}", True, amarillo)
    text_high = fuente_score.render (f"best: {high_score}", True, blanco)
    fuente_lvl = pygame.font.SysFont("trebuchetms", 20, bold = True)
    text_lvl = fuente_lvl.render (f"LVL {nivel}", True, blanco)
    pantalla.blit(text_score, (20, 705))
    pantalla.blit(text_high, (20, 685))
    pantalla.blit(text_lvl, (280, 690))

    for i in range(vidas): 
        centro_x = 450 + 45 * i 
        pantalla.blit(pacman_abierto, (centro_x, 690))
    
def pantalla_esquina (pantalla, fantasma_actual, fants_elegidos, ind_fant, colores_fants, opciones_esquina, esquinas_elegidas):
    pantalla.fill(negro)
    fantasma_actual = fants_elegidos[ind_fant] if ind_fant < len(fants_elegidos) else fants_elegidos [-1]
    color_fant = colores_fants [fantasma_actual] 
    fuente_elegir = pygame.font.SysFont("Courier New", 28, bold = True)
    fuente_fants = pygame.font.SysFont("Courier New", 25, bold = True)
    text_elegir = fuente_elegir.render(f"Asigná una esquina a {fantasma_actual} ({ind_fant + 1}/{len(fants_elegidos)})", True, color_fant)
    pantalla.blit(text_elegir, (35, 40))
    pos_y = 120
    for i, opcion in enumerate (opciones_esquina):
        numero = fuente_fants.render(f"{i + 1}", True, color_fant)
        texto = fuente_fants.render(opcion, True, gris)
        pantalla.blit(numero, (160, pos_y))
        pantalla.blit(texto, (200, pos_y))
        pos_y += 60 
    #resumen de lo que va haciendo el usuario para saber si ya eligió la opción
    fuente_resumen = pygame.font.SysFont("Courier New", 18)
    pos_y_resumen = 500
    for nombre, esquina in esquinas_elegidas.items():
        color = colores_fants [nombre]
        texto_resumen= fuente_resumen.render (f"{nombre}: {esquina}", True, color)
        pantalla.blit(texto_resumen, (160, pos_y_resumen))
        pos_y_resumen += 30 

def pantalla_aprender(pantalla, opciones_modo, ind_modo):
    pantalla.fill(negro)
    fuente_elegir = pygame.font.SysFont("Courier New", 28, bold = True)
    text_aprender = fuente_elegir.render("Elija el modo de juego: ", True, rojo) 
    pantalla.blit(text_aprender, (100, 80))
    
    pos_y = 200
    for i, opcion in enumerate(opciones_modo):
        if i == ind_modo:
            color = amarillo
        else: 
            color = gris
        texto = fuente_elegir.render(opcion, True, amarillo)
        rect = texto.get_rect()
        rect.x = 200
        rect.y = pos_y
        rect_grande = rect.inflate(30, 10)
        pygame.draw.rect(pantalla, color, rect_grande, 3)
        pantalla.blit(texto, (200, pos_y))
        pos_y += 100 

def pantalla_preparado(pantalla):
    pantalla.fill(negro)
    fuente_ready = pygame.font.SysFont("trebuchetms", 30, bold = True)
    text_ready = fuente_ready.render("READY?", True, amarillo)
    pantalla.blit(text_ready, (300, 300)) 
